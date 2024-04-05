import json
from typing import Any

import jinja2

from spl_implementation.models import MappingModel, Configuration


class VEngine:

    def __init__(self) -> None:
        self._template_file: str = None
        self._configuration: Configuration = None
        self._mapping_model: MappingModel = None

    def resolve_variability(self) -> str:
        if self._template_file is None: 
            raise VEngineException(f'No template has been loaded.')
        if self._configuration:
            raise VEngineException(f'No configuration has been loaded.')
        if self._mapping_model is None:
            raise VEngineException(f'No mapping model has been loaded.')
            
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        environment = jinja2.Environment(loader=template_loader)
        template = environment.get_template(self._template_file)
        content = template.render(None)  # maps
        return content

    def load_mapping_model(self, mapping_model_filepath: str) -> None:
        self._mapping_model = MappingModel.load_from_file(mapping_model_filepath)

    def load_configuration(self, configuration_filepath: str) -> None:
        self._configuration = load_configuration_from_file(configuration_filepath)

    def _build_template_maps(self) -> dict[str, Any]:
        maps: dict[str, Any] = {}  # dict of 'handler' -> Value
        for vp in self._mapping_model.get_variation_points():
            if not '.' in vp.handler:  # it is a simple feature (not a multi-feature)
                if self._configuration.is_selected(vp.feature):
                    if not vp.variants:
                        maps[vp.handler] = self._configuration.get_value(vp.feature)
                    elif not vp.variants[0].identifier:
                        maps[vp.handler] = True
                    else:
                        maps[vp.handler] = self._get_variant_value(vp)
            else:
                multi_feature = vp.feature
                multi_features.append(multi_feature)
            maps[vp.handler] = 
        self._configuration.elements


class VEngineException(Exception):
    pass


def load_configuration_from_file(filepath: str) -> Configuration:
    with open(filepath) as file:
        json_dict = json.load(file)
    return Configuration(json_dict)
