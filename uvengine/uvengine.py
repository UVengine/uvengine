import json
import pathlib
from typing import Any

import jinja2

from uvengine.configuration import Configuration
from uvengine.mapping_model import MappingModel


class UVEngine():

    def __init__(self,
                 template_filepath: str,
                 config_filepath: str,
                 mapping_filepath: str = None) -> None:
        self._template_dirpath: str = pathlib.Path(template_filepath).parent
        self._template_filepath: str = template_filepath
        self._config_file: str = config_filepath
        self._mapping_file: str | None = mapping_filepath
        
        self._configuration: Configuration = load_configuration_from_file(self._config_file)
        self._mapping_model: MappingModel = None
        if self._mapping_file is not None:
            self._mapping_model = MappingModel.load_from_file(self._mapping_file)


    def resolve_variability(self) -> str:
        template_loader = jinja2.FileSystemLoader(searchpath=self._template_dirpath)
        environment = jinja2.Environment(loader=template_loader,
                                         trim_blocks=True,
                                         lstrip_blocks=True)
        print(f'Configuration: {self._configuration}')
        template = environment.get_template(pathlib.Path(self._template_filepath).name)
        maps = self._build_template_maps(self._configuration)
        content = template.render(maps)
        return content

    def _build_template_maps(self, configuration: Configuration) -> dict[str, Any]:
        if self._mapping_file is None:
            return configuration.elements
        maps: dict[str, Any] = {}  # dict of 'handler' -> Value
        for element, element_value in configuration.elements.items():  # for each element in the configuration
            handler = element
            value = element_value
            if configuration.is_selected(element) and element_value is not None:  # if the feature is selected or has a valid value (not None for typed features)
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


def load_configuration_from_file(filepath: str) -> Configuration:
    with open(filepath) as file:
        json_dict = json.load(file)
    config = json_dict['config']
    return Configuration(config)
