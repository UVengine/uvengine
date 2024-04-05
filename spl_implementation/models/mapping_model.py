import csv
from enum import Enum

from spl_implementation.models import VariationPoint, Variant


class MappingModel:
    """A mapping model relates a feature model with the variation points and variants of the 
    implementation artefacts.
    """

    class Fieldnames(Enum):
        VARIATION_POINT = 'VariationPointFeature'
        HANDLER = 'TemplateHandler'
        VARIANT = 'VariantIdentifier'
        VALUE = 'VariantValue'

    def __init__(self) -> None:
        self._model: dict[str, VariationPoint] = dict()

    @classmethod
    def load_from_file(cls, filepath: str) -> 'MappingModel': 
        """Load the mapping model with the variation points and variants information."""
        model: dict[str, 'VariationPoint'] = {}
        with open(filepath, mode='r') as file:
            csv_reader = csv.DictReader(file, skipinitialspace=True)
            if any(head not in [fieldname.value for fieldname in MappingModel.Fieldnames] 
                   for head in csv_reader.fieldnames):
                raise MappingModelException(f"The mapping model '{filepath}' has invalid \
                                            fieldnames. Use: \
                                            {[fieldname.value 
                                              for fieldname in MappingModel.Fieldnames]}")
            for row in csv_reader:
                vp_feature = row[MappingModel.Fieldnames.VARIATION_POINT]
                vp_handler = row[MappingModel.Fieldnames.HANDLER]
                variant_feature = row[MappingModel.Fieldnames.VARIANT]
                variant_value = row[MappingModel.Fieldnames.VALUE]
                if not vp_feature in model:
                    model[vp_feature] = VariationPoint(vp_feature, vp_handler)
                if not variant_value:
                    variant_value = None
                variant = Variant(variant_feature, variant_value)
                model[vp_feature].variants.append(variant)
        mapping_model = cls()
        mapping_model._model = model
        return mapping_model
    
    def get_variation_points(self) -> list[VariationPoint]:
        return list(self._model.values())


class MappingModelException(Exception):
    pass
