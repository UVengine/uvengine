from typing import Any


class Variant:
    """A variant is a representation of a variability object within domain artefacts [Pohl2005].

    A variant identifies a single option of a variation point and can be associated with other 
    artefacts to indicate that those artefacts correspond to a particular option.
    """

    def __init__(self, identifier: str, value: Any = None) -> None:
        """Initialize a variant with a identifier (feature or attribute) and a specific value."""
        self.identifier: str = identifier  # Feature or Attribute
        self.value: Any = value

    def __repr__(self) -> str:  
        return f'V({str(self.identifier)}, {str(self.value)})'


class VariationPoint:
    """A variation point is a representation of a variability subject within domain artefacts 
    enriched by contextual information [Pohl2005].
    """

    def __init__(self, feature: str, handler: str, variants: list['Variant'] = None) -> None:
        """Initialize a variation point with the feature that represents the variation point, 
        the handlers which identifies the variable part in the artefact, and the variants for 
        this variation point.
        """
        self.feature: str = feature
        self.handler: str = handler
        self.variants: list['Variant'] = [] if variants is None else variants

    def __repr__(self) -> str:
        return f'VP({str(self.feature)}, {str(self.handler)}, {str(self.variants)})'
