import unittest

from converters.html_converters import block_to_block_type, BlockType, markdown_to_html_node
from converters.text_node_converters import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("text", TextType.TEXT)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "text")

    def test_bold(self):
        node = TextNode("text", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<b>text</b>")

    def test_italit(self):
        node = TextNode("text", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<i>text</i>")

    def test_code(self):
        node = TextNode("1 + 1", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<code>1 + 1</code>")

    def test_link(self):
        node = TextNode("anchor", TextType.LINK, "www.link.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<a href=\"www.link.com\">anchor</a>")

    def test_image(self):
        node = TextNode("alt", TextType.IMAGE, "www.image.com/image")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<img src=\"www.image.com/image\" alt=\"alt\"></img>")

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_code(self):
        block = "```\nsome code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> line1\n> line2\n> line3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "* item\n* item\n* item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        block = "1. item\n2. item\n300. item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_single_paragraph(self):
        markdown = "This is a simple *paragraph*! And this text is **bold**!"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode('div', [
            ParentNode('p', [
                LeafNode(None, 'This is a simple '),
                LeafNode('i', 'paragraph'),
                LeafNode(None, '! And this text is '),
                LeafNode('b', 'bold'),
                LeafNode(None, '!')
            ])
        ])
        self.assertEqual(actual.to_html(), expected.to_html())

    def test_headings(self):
        markdown = "# H1\n\n## H2\n\n### H3\n\n#### H4\n\n##### H5\n\n###### H6"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode('div', [
            ParentNode('h1', [LeafNode(None, 'H1')]),
            ParentNode('h2', [LeafNode(None, 'H2')]),
            ParentNode('h3', [LeafNode(None, 'H3')]),
            ParentNode('h4', [LeafNode(None, 'H4')]),
            ParentNode('h5', [LeafNode(None, 'H5')]),
            ParentNode('h6', [LeafNode(None, 'H6')])
        ])
        self.assertEqual(actual.to_html(), expected.to_html())

    def test_code(self):
        markdown = "```\nsum = 1 + 1 + 1\nprint(sum)\n```"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode('div', [ParentNode('pre', [
            ParentNode('code', [
                LeafNode(None, 'sum = 1 + 1 + 1\nprint(sum)')
            ])
        ])])
        self.assertEqual(actual.to_html(), expected.to_html())

    def test_blockquote(self):
        markdown = "> line1\n> *line2*\n> **line3**"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode('div', [
            ParentNode('blockquote', [
                LeafNode(None, 'line1 '),
                LeafNode('i', 'line2'),
                LeafNode(None, ' '),
                LeafNode('b', 'line3')
            ])
        ])
        self.assertEqual(actual.to_html(), expected.to_html())

    def test_unordered_list(self):
        markdown = "* item1\n* item2\n* item3"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode('div', [
            ParentNode('ul', [
                ParentNode('li', [LeafNode(None, 'item1')]),
                ParentNode('li', [LeafNode(None, 'item2')]),
                ParentNode('li', [LeafNode(None, 'item3')])
            ])
        ])
        self.assertEqual(actual.to_html(), expected.to_html())
    
    def test_ordered_list(self):
        markdown = "1. item1\n2. item2\n3. item3"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode('div', [
            ParentNode('ol', [
                ParentNode('li', [LeafNode(None, 'item1')]),
                ParentNode('li', [LeafNode(None, 'item2')]),
                ParentNode('li', [LeafNode(None, 'item3')])
            ])
        ])
        self.assertEqual(actual.to_html(), expected.to_html())

    def test_all_blocks(self):
        markdown = """
# Heading 1

This is an example paragraph to test with!

It has **bold text** and *italic text* to test with!

It even has lists:

* this
* is
* unordered

1. this
2. is
3. ordered

Here's some code:

```
print('Markdown to HTML works great!')
```

Finally, a blockquote:

> See the winds
> go wild
> like children

Goodbye!
"""
        actual = markdown_to_html_node(markdown)
        expected = ParentNode('div', [
            ParentNode('h1', [LeafNode(None, 'Heading 1')]),
            ParentNode('p', [LeafNode(None, 'This is an example paragraph to test with!')]),
            ParentNode('p', [
                LeafNode(None, 'It has '),
                LeafNode('b', 'bold text'),
                LeafNode(None, ' and '),
                LeafNode('i', 'italic text'),
                LeafNode(None, ' to test with!')
            ]),
            ParentNode('p', [LeafNode(None, 'It even has lists:')]),
            ParentNode('ul', [
                ParentNode('li', [LeafNode(None, 'this')]),
                ParentNode('li', [LeafNode(None, 'is')]),
                ParentNode('li', [LeafNode(None, 'unordered')]),
            ]),
            ParentNode('ol', [
                ParentNode('li', [LeafNode(None, 'this')]),
                ParentNode('li', [LeafNode(None, 'is')]),
                ParentNode('li', [LeafNode(None, 'ordered')]),
            ]),
            ParentNode('p', [LeafNode(None, "Here's some code:")]),
            ParentNode('pre', [
                ParentNode('code', [LeafNode(None, "print('Markdown to HTML works great!')")])
            ]),
            ParentNode('p', [LeafNode(None, "Finally, a blockquote:")]),
            ParentNode('blockquote', [LeafNode(None, 'See the winds go wild like children')]),
            ParentNode('p', [LeafNode(None, 'Goodbye!')])
        ])
        self.maxDiff = None
        self.assertEqual(actual.to_html(), expected.to_html())

if __name__ == "__main__":
    unittest.main()