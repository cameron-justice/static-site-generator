from textnode import TextNode, TextType
from utilities import format_markdown_image, format_markdown_link
import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
        Extract all markdown image alt text and link from given text string
    """
    image_info = []

    # Expression to capture markdown image
    # Group 1: Alt Text
    # Group 2: Image URL
    expr = "!\[([^\]]*)\]\(([^\)]*)\)"

    matches = re.finditer(expr, text)

    for match in matches:
        alt = match.group(1)
        url = match.group(2)
        image_info.append((alt, url))

    return image_info

def extract_markdown_links(text) -> list[tuple[str, str]]:
    """
        Extract all markdown link text and link from given text string
    """
    link_info = []
    # Expression to capture markdown link
    # Group 1: Anchor Text
    # Group 2: Link Text
    expr = "(?<!!)\[([^\]]*)\]\(([^\)]*)\)"

    matches = re.finditer(expr, text)

    for match in matches:
        anchor = match.group(1)
        link = match.group(2)
        link_info.append((anchor, link))

    return link_info

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
        Split a text node into text and image nodes
    """
    nodes = []

    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            nodes.append(node)
            continue

        sub_nodes = []
        image_info = extract_markdown_images(node.text)

        remainder = node.text

        for (alt, link) in image_info: 
            # Create a text node from the text before the image and extract the remaining string
            image_string = format_markdown_image(alt, link)
            [pre_text, remainder] = remainder.split(image_string, 1)
            
            # Save the text node if it has content
            if len(pre_text) > 0:
                sub_nodes.append(TextNode(pre_text, TextType.TEXT))

            # Save the image node
            sub_nodes.append(TextNode(alt, TextType.IMAGE, link))

        if len(remainder) > 0:
            sub_nodes.append(TextNode(remainder, TextType.TEXT))

        nodes.extend(sub_nodes)

    return nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
        Split a text node into text and link nodes
    """
    nodes = []

    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            nodes.append(node)
            continue

        sub_nodes = []
        image_info = extract_markdown_links(node.text)

        remainder = node.text

        for (alt, link) in image_info: 
            # Create a text node from the text before the image and extract the remaining string
            image_string = format_markdown_link(alt, link)
            [pre_text, remainder] = remainder.split(image_string, 1)
            
            # Save the text node if it has content
            if len(pre_text) > 0:
                sub_nodes.append(TextNode(pre_text, TextType.TEXT))

            # Save the image node
            sub_nodes.append(TextNode(alt, TextType.LINK, link))

        if len(remainder) > 0:
            sub_nodes.append(TextNode(remainder, TextType.TEXT))

        nodes.extend(sub_nodes)
    return nodes
  
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
        Split a text node into the given text_type based on the containing delimeter
    """
    nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            nodes.append(node)
            continue
        
        # Ensure all blocks are closed
        if node.text.count(delimiter) % 2 == 1:
            raise Exception(f"Line \"{node.text}\" contains invalid markdown due to unclosed block")
        
        sub_nodes = []

        substring = node.text

        # Escape to allow delimiters that are also special characters in regex (*, **, etc.)
        escaped_delimiter = re.escape(delimiter)

        # Create expression to capture instance of text within delimiters
        expr = f"{escaped_delimiter}[^{escaped_delimiter}]*{escaped_delimiter}"
        match = re.search(expr, node.text)

        while not match is None:
            pre = TextNode(substring[0:match.start()], TextType.TEXT)
            block = TextNode(match.group().replace(delimiter, ''), text_type)
            sub_nodes.extend([pre, block])
            substring = substring[match.end():] 
            match = re.search(expr, substring)

        if len(substring) > 0:
            sub_nodes.append(TextNode(substring, TextType.TEXT))

        nodes.extend(sub_nodes)
    return nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    """
        Parse a markdown string into TextNodes

        input: markdown string to be parsed
        output: list of TextNodes representing the markdown 
    """
    nodes = [TextNode(text, TextType.TEXT)]

    # Bold
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    # Italic
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    # Code
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    # Images
    nodes = split_nodes_image(nodes)
    # Links
    nodes = split_nodes_link(nodes)

    return nodes