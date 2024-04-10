import os
import json
from typing import Any

import jinja2

from spl_implementation.models import Configuration, MappingModel


class VEngine:

    def __init__(self) -> None:
        self._template_file: str = None
        self._configuration: Configuration = None
        self._mapping_model: MappingModel = None

    def resolve_variability(self) -> str:
        if self._template_file is None: 
            raise VEngineException(f'No template has been loaded.')
        if self._configuration is None:
            raise VEngineException(f'No configuration has been loaded.')
        if self._mapping_model is None:
            raise VEngineException(f'No mapping model has been loaded.')
            
        template_loader = jinja2.FileSystemLoader(searchpath=self._template_dirpath)
        environment = jinja2.Environment(loader=template_loader,
                                         trim_blocks=True,
                                         lstrip_blocks=True)
        template = environment.get_template(self._template_file)
        maps = self._build_template_maps(self._configuration.elements)
        print(maps)
        content = template.render(maps)
        return content

    def load_mapping_model(self, mapping_model_filepath: str) -> None:
        self._mapping_model = MappingModel.load_from_file(mapping_model_filepath)

    def load_configuration(self, configuration_filepath: str) -> None:
        self._configuration = load_configuration_from_file(configuration_filepath)

    def load_template(self, template_filepath: str) -> None:
        path, filename = os.path.split(template_filepath)
        self._template_dirpath = path
        self._template_file = filename

    def _build_template_maps(self, config_elements: dict[str, Any]) -> dict[str, Any]:
        maps: dict[str, Any] = {}  # dict of 'handler' -> Value
        for element, element_value in config_elements.items():  # for each element in the configuration
            handler = element
            value = element_value
            if element_value:  # if the feature is selected or has a valid value (not None for typed features)
                # The handler is provided in the mapping model, otherwise it is the feature's name.
                if element in self._mapping_model.maps:
                    handler = self._mapping_model.maps[element].handler
                    if '.' in handler:  # case of multi-feature explicitly specified in the mapping model
                        handler = handler[handler.index('.')+1:]
                    value = self._mapping_model.maps[element].value
                if value is None:  # the value is provided in the mapping model, otherwise is got from the configuration
                    value = element_value
                if isinstance(element_value, list):  # Multi-feature in the configuration
                    value = [self._build_template_maps(ev) for ev in element_value]
                maps[handler] = value
        return maps


class VEngineException(Exception):
    pass


def load_configuration_from_file(filepath: str) -> Configuration:
    with open(filepath) as file:
        json_dict = json.load(file)
    config = json_dict['config']
    return Configuration(config)
