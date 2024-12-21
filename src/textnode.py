from enum import Enum


class TextType(Enum):
    Text  = 0
    Bold    = 1
    Italic  = 2
    Code    = 3
    Link    = 4
    Image   = 5


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text or self.text_type != other.text_type or self.url != other.url:
            return False
        return True

    def __repr__(self):
        if self.url:
            return f"TextNode('{self.text}', {self.text_type.name}, {self.url})"
        else:
            return f"TextNode('{self.text}', {self.text_type.name})"


