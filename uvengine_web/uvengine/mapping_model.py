import csv
from typing import Any
from enum import Enum


class MappingModelException(Exception):
    pass


class FeatureHandlerMap():

    def __init__(self, feature: str, handler: str, value: Any) -> None:
        self.feature: str = feature
        self.handler: str = handler
        self.value: Any = value

    def __repr__(self) -> str:  
        return f'M({self.feature}, {self.handler}, {self.value})'


class MappingModel():
    """A mapping model relates a feature model with the implementation artefacts."""

    class Fieldnames(Enum):
        FEATURE = 'Feature'
        HANDLER = 'Handler'
        VALUE = 'Value'

    def __init__(self) -> None:
        self.maps: dict[str, FeatureHandlerMap] = dict()

    @classmethod
    def load_from_file(cls, filepath: str) -> 'MappingModel': 
        """Load the mapping model with the variation points and variants information."""
        model: dict[str, FeatureHandlerMap] = {}
        with open(filepath, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, skipinitialspace=True)
            if any(head not in [fieldname.value for fieldname in MappingModel.Fieldnames] 
                   for head in csv_reader.fieldnames):
                raise MappingModelException(f"The mapping model '{filepath}' has invalid fieldnames. Use: {[fieldname.value for fieldname in MappingModel.Fieldnames]}")
            for row in csv_reader:
                feature = row[MappingModel.Fieldnames.FEATURE.value]
                handler = row[MappingModel.Fieldnames.HANDLER.value]
                value = row[MappingModel.Fieldnames.VALUE.value]
                model[feature] = FeatureHandlerMap(feature, handler, value)
        mapping_model = cls()
        mapping_model.maps = model
        return mapping_model



