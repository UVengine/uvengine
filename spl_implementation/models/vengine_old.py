from typing import Any

from flamapy.metamodels.configuration_metamodel.models import Configuration

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Attribute

from spl_implementation.models import (
    MappingModel, 
    VariationPoint, 
    VEngineException, 
    ConfigurationValues
)


class VEngine:

    def __init__(self) -> None:
        self._mapping_models: list[MappingModel] = []
        self._configurations: list[ConfigurationValues] = []

    def load_mapping_model(self, mapping_model: MappingModel) -> None:
        self._mapping_models.append(mapping_model)

    def load_configuration(self, configuration_values: ConfigurationValues) -> None:
        self._configurations.append(configuration_values)

    def get_feature_models(self) -> list[FeatureModel]:
        return [mm.feature_model for mm in self._mapping_models]
    
    def _is_selected_in_a_configuration(self, feature: Feature) -> bool:
        return any(config.is_selected_in_configuration(feature.name) 
                   for config in self._configurations)
    
    def _get_variant_value(self, vp: VariationPoint) -> Any:
        return next((config.get_variant_value(vp) for config in self._configurations), None)

    def _build_template_maps(self) -> None:
        maps = {}
        multi_features_maps = []
        multi_features = []

        # Simple features
        for vp in (variation_point for mm in self._mapping_models 
                   for variation_point in mm.mapping_model.values()):
            if not '.' in vp.handler:  # it is a simple feature (not a multi-feature)
                if self._is_selected_in_a_configuration(vp.feature):
                    if not vp.variants:
                        maps[vp.handler] = True
                    elif not vp.variants[0].identifier:
                        maps[vp.handler] = True
                    else:
                        maps[vp.handler] = self._get_variant_value(vp)
            else:
                multi_feature = vp.feature
                multi_features.append(multi_feature)
        
        # Multi-features:
        i = 0
        for config in self._configurations:
            clonable_children = [f for f in ]
            feature = get_feature_from_fms('DataSet', fms)
            if feature in config.elements and config.elements[feature]:  # it is a instance configuration of the multi-feature
                config_attributes = attributes[i]
                try:
                    while not any('DataSet' in a for a in attributes[i].keys()):
                        i += 1
                        config_attributes = attributes[i]
                except:
                    raise Exception('There is needed one configuration file for the attributes for at least one DataSet.')
                dataset_map = {}
                for vp in mapping_model.values():
                    if '.' in vp.handler:  # it is a multi-feature
                        handler_identifier_in_template = vp.handler[vp.handler.index('.')+1:]
                        if vp.feature in config.elements and config.elements[feature]:
                            if not vp.variants:
                                dataset_map[handler_identifier_in_template] = True
                            else:
                                dataset_map[handler_identifier_in_template] = get_variant_value_in_configuration(fms, vp, config, config_attributes)
                multi_features_maps.append(dataset_map)
                i += 1
        maps['plots'] = multi_features_maps
        return maps



            else:  # it is a multi-feature (clonable)
                clon_handler = vp.handler[:vp.handler.index('.')]
                clon_map = maps.get(clon_handler, None)
                if clon_map is None:
                    clon_map = []
                    maps[clon_handler] = clon_map
                handler_identifier_in_template = vp.handler[vp.handler.index('.')+1:]
                if vp.feature in config.elements and config.elements[feature]:
                    if not vp.variants:
                        clonable_map[handler_identifier_in_template] = True
                    else:
                        clonable_map[handler_identifier_in_template] = get_variant_value(vp, 
                                                                                        self._configurations,
                                                                                        self._attributes,
                                                                                        self.get_feature_models())
                multi_features_maps.append(dataset_map)
        
        # Multi-features:
        i = 0
        for config in self._configurations:
            feature = get_feature_from_fms('DataSet', fms)
            if feature in config.elements and config.elements[feature]:  # it is a instance configuration of the multi-feature
                config_attributes = attributes[i]
                try:
                    while not any('DataSet' in a for a in attributes[i].keys()):
                        i += 1
                        config_attributes = attributes[i]
                except:
                    raise Exception('There is needed one configuration file for the attributes for at least one DataSet.')
                dataset_map = {}
                for vp in mapping_model.values():
                    if '.' in vp.handler:  # it is a multi-feature
                        handler_identifier_in_template = vp.handler[vp.handler.index('.')+1:]
                        if vp.feature in config.elements and config.elements[feature]:
                            if not vp.variants:
                                dataset_map[handler_identifier_in_template] = True
                            else:
                                dataset_map[handler_identifier_in_template] = get_variant_value_in_configuration(fms, vp, config, config_attributes)
                multi_features_maps.append(dataset_map)
                i += 1
        maps['plots'] = multi_features_maps
        return maps





def get_feature_from_fms(feature_name: str, fms: list[FeatureModel]) -> Feature:
    """Return the feature object from all the feature models."""
    for fm in fms:
        feature = fm.get_feature_by_name(feature_name)
        if feature is not None:
            return feature
    raise VEngineException(f"Feature '{feature_name}' does not exist in any feature model.")


def _get_fm_configurations(configurations: list[ConfigurationValues]) -> list[Configuration]:
    return [c.configuration for c in configurations]
    
def _get_attributes_configurations(configurations: list[ConfigurationValues]) -> list[Attribute]:
    return [a for c in configurations for a in c.attributes]
