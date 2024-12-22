from enum import Enum
from htmlnode import ParentNode, LeafNode
from converters.text_node_converters import text_node_to_html_node
from parsers import text_to_textnodes
import re

BlockType = Enum("BlockType", ["PARAGRAPH", "HEADING", "CODE", "QUOTE", "UNORDERED_LIST", "ORDERED_LIST"])

def block_to_paragraph(block: str) -> ParentNode:
    text_nodes = text_to_textnodes(block)
    children = list(map(text_node_to_html_node, text_nodes))
    return ParentNode('p', children)

def block_to_heading(block: str) -> ParentNode:
    level = len(block.split(' ')[0]) # Get heading level by number of '#' at start
    remainder = block.lstrip('#').lstrip()
    text_nodes = text_to_textnodes(remainder)
    children = list(map(text_node_to_html_node, text_nodes))
    return ParentNode(f"h{level}", children)

def block_to_code(block: str) -> ParentNode:
    remainder = block.lstrip('```').rstrip('```').strip()
    return ParentNode('pre', [ParentNode('code', [LeafNode(None, remainder)])])

def block_to_quote(block: str) -> ParentNode:
    text = ' '.join(line.lstrip('> ') for line in block.splitlines())
    text_nodes = text_to_textnodes(text)
    children = list(map(text_node_to_html_node, text_nodes))
    return ParentNode('blockquote', children)

def block_to_unordered_list(block: str) -> ParentNode:
    lines = [ line.lstrip('* ') for line in block.splitlines()]
    text_node_lines = [text_to_textnodes(line) for line in lines]
    children = []
    for node_line in text_node_lines:
        children.append(ParentNode('li', [text_node_to_html_node(node) for node in node_line ]))
    return ParentNode('ul', children)

def block_to_ordered_list(block: str) -> ParentNode:
    lines = [ re.split("\d+. ", line, maxsplit=1)[1] for line in block.splitlines() ]
    text_node_lines = [text_to_textnodes(line) for line in lines]
    children = []
    for node_line in text_node_lines:
        children.append(ParentNode('li', [text_node_to_html_node(node) for node in node_line]))
    return ParentNode('ol', children)

def markdown_to_blocks(markdown: str) -> list[str]:
    """
        Parse a markdown file into individual markdown blocks, denoted by empty lines
    """
    blocks = markdown.split('\n\n')
    blocks = [ x.strip() for x in blocks]
    return blocks

def block_to_block_type(block: str) -> BlockType:

    if re.match("^#{1,6} \w+", block):
        return BlockType.HEADING
    if re.match("^```[^`]*```$", block, re.MULTILINE):
        return BlockType.CODE
    if len(re.findall("^>.*", block, re.MULTILINE)) == len(block.splitlines()):
        return BlockType.QUOTE
    if len(re.findall("^\* .*", block, re.MULTILINE)) == len(block.splitlines()):
        return BlockType.UNORDERED_LIST
    if len(re.findall("^\d+\. .*", block, re.MULTILINE)) == len(block.splitlines()):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def extract_title(markdown: str) -> str:
    headings = filter(lambda b: block_to_block_type(b) == BlockType.HEADING, markdown_to_blocks(markdown))
    # heading_nodes = [block_to_heading(block) for block in headings]
    # for node in heading_nodes:
    #     if node.tag == 'h1':
    #         return node.children
    for heading in headings:
        if re.match("^#{1} ", heading):
            return heading.lstrip('#').strip()
        
    raise ValueError("Markdown provided contains no H1-level heading")
