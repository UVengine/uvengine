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
        environment = jinja2.Environment(loader=template_loader)
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
        for element, element_value in config_elements.items():
            if element in self._mapping_model.maps:
                if element_value:
                    handler = self._mapping_model.maps[element].handler
                    key = handler
                    if '.' in handler:
                        key = handler[handler.index('.')+1:]
                    value = self._mapping_model.maps[element].value
                    if value is None:
                        value = element_value
                    if isinstance(element_value, list):
                        value = [self._build_template_maps(ev) for ev in element_value]
                    maps[key] = value
        return maps


class VEngineException(Exception):
    pass


def load_configuration_from_file(filepath: str) -> Configuration:
    with open(filepath) as file:
        json_dict = json.load(file)
    config = json_dict['config']
    return Configuration(config)
