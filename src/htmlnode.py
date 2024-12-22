from typing import Self
from enum import Enum

class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[Self] | None = None, props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> None:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return "" if self.props is None else ' ' + ' '.join(map(lambda x: f"{x}=\"{self.props[x]}\"", self.props))
    
    def __repr__(self) -> str:
        if self.tag is None:
            # print(self.tag, self.value)
            return self.value

        content = self.value if not self.value is None else ''.join([child.__repr__() for child in self.children])


        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict | None = None) -> None:
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict | None = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        children = "" if len(self.children) == 0 else ''.join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"