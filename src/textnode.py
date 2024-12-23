from enum import Enum
from typing import Self

TextType = Enum('TextType', ['TEXT', 'BOLD', 'ITALIC', 'CODE', 'LINK', 'IMAGE'])

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: Self) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
