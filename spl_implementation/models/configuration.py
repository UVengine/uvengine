from typing import Any


class Configuration:

    def __init__(self, elements: dict[str, Any] = {}) -> None:
        self.elements = elements

    def is_selected(self, element: str) -> bool:
        return element in self.elements and self.elements[element]
    
    def get_value(self, element: str) -> Any:
        return self.elements[element]
    