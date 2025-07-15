import pathlib
from typing import Any

import jinja2

from flamapy.metamodels.configuration_metamodel.models import Configuration
from flamapy.metamodels.configuration_metamodel.transformations import (
    UVLSJSONReader,
    ConfigurationJSONReader
)
from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLReader

from uvengine.mapping_model import MappingModel


class UVEngine():

    def __init__(self,
                 feature_model_path: str,
                 configs_path: list[str],
                 templates_paths: list[str],
                 mapping_model_filepath: str = None) -> None:
        self._feature_model: FeatureModel = UVLReader(feature_model_path).transform()
        self._templates_dirpath: str = pathlib.Path(templates_paths[0]).parent
        self._templates_paths: list[str] = templates_paths
        self._configs_path: list[str] = configs_path
        self._mapping_model_file: str | None = mapping_model_filepath
        
        self._configuration: Configuration = load_configurations_from_file(self._configs_path)
        self._mapping_model: MappingModel = MappingModel()
        if self._mapping_model_file is not None:
            self._mapping_model = MappingModel.load_from_file(self._mapping_model_file)

    @property
    def feature_model(self) -> FeatureModel:
        return self._feature_model
    
    @property
    def configuration(self) -> Configuration:
        return self._configuration
    
    @property
    def mapping_model(self) -> MappingModel | None:
        return self._mapping_model
    
    @property
    def templates_dirpath(self) -> str:
        return self._templates_dirpath

    @property
    def templates(self) -> list[str]:
        return self._templates_paths


    def resolve_variability(self) -> dict[str, str]:
        template_loader = jinja2.FileSystemLoader(searchpath=self.templates_dirpath)
        environment = jinja2.Environment(loader=template_loader,
                                         trim_blocks=True,
                                         lstrip_blocks=True,
                                         keep_trailing_newline=False)
        maps = self._build_template_maps(self.configuration)
        resolved_templates: dict[str, str] = {}
        for template_path in self.templates:
            template = environment.get_template(pathlib.Path(template_path).name)
            content = template.render(maps)
            resolved_templates[template_path] = content
        return resolved_templates

    def _build_template_maps(self, configuration: Configuration) -> dict[str, Any]:
        # Initialize the maps with the configuration elements
        maps: dict[str, Any] = dict(configuration.elements)  # dict of 'handler' -> Value
        for element, element_value in configuration.elements.items():  # for each element in the configuration
            feature = self.feature_model.get_feature_by_name(element)
            parent = None
            if feature is not None:
                parent = feature.get_parent()
            handler = element
            value = element_value
            if configuration.is_selected(element) and element_value is not None:  # if the feature is selected or has a valid value (not None for typed features)
                 # The handler is provided in the mapping model, otherwise it is the feature's name.
                if element in self.mapping_model.maps:
                    handler = self.mapping_model.maps[element].handler
                    if '.' in handler:  # case of multi-feature explicitly specified in the mapping model
                        handler = handler[handler.index('.')+1:]
                    value = self._mapping_model.maps[element].value
                if value is None or not value:  # the value is provided in the mapping model, otherwise is got from the configuration
                    value = element_value
                if isinstance(element_value, list):  # Multi-feature in the configuration
                    value = [self._build_template_maps(Configuration(ev)) for ev in element_value]
                # Automatic value for alternative variation points (we use the selected children of alternative features as value of the variation point) 
                # for those elements that are not in the mapping model
                if element not in self.mapping_model.maps:
                    if parent is not None and parent.is_alternative_group():
                        handler = parent.name
                        value = element
                maps[handler] = value
        return maps


def load_configurations_from_file(configs_path: list[str]) -> Configuration:
    elements = {}
    for filepath in configs_path:
        if filepath.endswith('.uvl.json'):
            config = UVLSJSONReader(filepath).transform()
        elif filepath.endswith('.json'):
            config = ConfigurationJSONReader(filepath).transform()
            if 'config' in config.elements:
                # Handle case where the JSON file has a 'config' key and a wrong extension
                config = UVLSJSONReader(filepath).transform()
        else:
            raise ValueError(f"Unsupported configuration file format: {filepath}")
        elements.update(config.elements)
    return Configuration(elements)
