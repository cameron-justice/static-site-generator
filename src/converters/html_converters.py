from htmlnode import ParentNode
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, block_to_heading, block_to_code, block_to_ordered_list, block_to_paragraph, block_to_quote, block_to_unordered_list

def markdown_to_html_node(markdown: str) -> ParentNode:
    """
        Converts an entire markdown file to an HTML file body.

        Note: Does not include `body` tag, top-level is `div`.

        Input:
            markdown: string, a markdown file text
        Output:
            A `div` HTML node with the parsed file contents as its children
    """
    nodes = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:

        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(block_to_paragraph(block))
                continue
            case BlockType.HEADING:
                nodes.append(block_to_heading(block))
                continue
            case BlockType.CODE:
                nodes.append(block_to_code(block))
                continue
            case BlockType.QUOTE:
                nodes.append(block_to_quote(block))
                continue
            case BlockType.UNORDERED_LIST:
                nodes.append(block_to_unordered_list(block))
                continue
            case BlockType.ORDERED_LIST:
                nodes.append(block_to_ordered_list(block))
                continue
            case _:
                raise NotImplementedError(f"Block type `{block_type}` has not been implemented yet!")
    return ParentNode('div', nodes)