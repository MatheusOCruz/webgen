from enum import Enum


class BlockType(Enum):
    Paragraph       = 0
    Heading         = 1
    Code            = 2
    Quote           = 3
    UnorderedList   = 4
    OrderedList     = 5



class BlockNode:
    def __init__(self, content, block_type):
        self.content = content
        self.block_type = block_type

    def __repr__(self):
        return f"BlockNode({self.block_type.name}, {self.content})"
