import csv
from enum import Enum
from typing import Any

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Attribute
from flamapy.metamodels.configuration_metamodel.models import Configuration

from spl_implementation.models import MappingModelException, ConfigurationValueException


class Variant:
    """A variant is a representation of a variability object within domain artefacts [Pohl2005].

    A variant identifies a single option of a variation point and can be associated with other 
    artefacts to indicate that those artefacts correspond to a particular option.
    """

    def __init__(self, identifier: str, value: Any = None) -> None:
        """Initialize a variant with a identifier (feature or attribute) and a specific value."""
        self.identifier = identifier  # Feature or Attribute
        self.value = value

    def __repr__(self) -> str:  
        return f'V({str(self.identifier)}, {str(self.value)})'


class VariationPoint:
    """A variation point is a representation of a variability subject within domain artefacts 
    enriched by contextual information [Pohl2005].
    """

    def __init__(self, feature: Feature, handler: str, variants: list['Variant'] = None) -> None:
        """Initialize a variation point with the feature that represents the variation point, 
        the handlers which identifies the variable part in the artefact, and the variants for 
        this variation point.
        """
        self.feature = feature
        self.handler = handler
        self.variants = [] if variants is None else variants

    def __repr__(self) -> str:
        return f'VP({str(self.feature)}, {str(self.handler)}, {str(self.variants)})'


class MappingModel:
    """A mapping model relates a feature model with the variation points and variants of the 
    implementation artefacts.
    """

    class Fieldnames(Enum):
        VARIATION_POINT = 'VariationPointFeature'
        HANDLER = 'Handler'
        VARIANT = 'VariantIdentifier'
        VALUE = 'VariantValue'

    def __init__(self, feature_model: FeatureModel, mapping: str) -> None:
        self.feature_model = feature_model
        self.mapping_model = self._load_mapping_model(feature_model, mapping)

    def _load_mapping_model(self, 
                            feature_model: FeatureModel, 
                            mapping_filepath: str) -> dict[str, 'VariationPoint']:
        """Load the mapping model with the variation points and variants information."""
        variation_points: dict[str, 'VariationPoint'] = {}
        with open(mapping_filepath, mode='r') as file:
            csv_reader = csv.DictReader(file, skipinitialspace=True)
            if any(head not in [fieldname.value for fieldname in MappingModel.Fieldnames] 
                   for head in csv_reader.fieldnames):
                raise MappingModelException(f"The mapping model '{mapping_filepath}' has invalid 
                                            fieldnames. Use: 
                                            {[fieldname.value 
                                              for fieldname in MappingModel.Fieldnames]}")
            for row in csv_reader:
                vp_feature = row[MappingModel.Fieldnames.VARIATION_POINT]
                vp_handler = row[MappingModel.Fieldnames.HANDLER]
                variant_feature = row[MappingModel.Fieldnames.VARIANT]
                variant_value = row[MappingModel.Fieldnames.VALUE]
                if '.' in variant_feature:  # it is an attribute
                    key = variant_feature
                    feature = feature_model.get_feature_by_name(vp_feature)
                    if feature is None:
                        raise MappingModelException(f"Feature '{vp_feature} does not exist in the given feature model.'")
                    variation_points[variant_feature] = VariationPoint(feature, vp_handler)
                elif not vp_feature in variation_points:
                    key = vp_feature
                    feature = feature_model.get_feature_by_name(vp_feature)
                    if feature is None:
                        raise MappingModelException(f"Feature '{vp_feature} does not exist in the given feature model.'")
                    variation_points[vp_feature] = VariationPoint(feature, vp_handler)
                else:
                    key = vp_feature
                if not variant_value:
                    variant_value = None
                variant = Variant(variant_feature, variant_value)
                variation_points[key].variants.append(variant)
        return variation_points


class ConfigurationValues:

    def __init__(self, configuration: Configuration, attributes: list[Attribute]) -> None:
        self.configuration = configuration
        self.attributes = attributes

    def get_variant_value(self, variation_point: VariationPoint) -> Any:
        """Return the value of the variant according to the provided configurations/attributes."""
        for variant in variation_point.variants:
            identifier = variant.identifier
            if '.' in identifier:  # it is an attribute
                feature = identifier[:identifier.index('.')]
                value = self.get_attribute_value(identifier)
            else:
                feature = identifier
                value = variant.value
            if self.is_selected_in_configuration(feature):
                return value
        return None

    def get_attribute_value(self, identifier: str) -> Any:
        attribute_name = identifier[identifier.index('.')+1:]
        attribute = next((a for a in self.attributes if a.name == attribute_name), None)
        if attribute is None:
            raise ConfigurationValueException(f"Attribute '{attribute_name}' not valid.")
        return attribute.get_default_value()

    def is_selected_in_configuration(self, feature_name: str) -> bool:
        return any(feature.name == feature_name and self.configuration.elements[feature] 
                   for feature in self.configuration.elements)
