import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        bold = TextNode("This is a bold node", TextType.BOLD)
        italic = TextNode("This is an italic node", TextType.ITALIC)
        self.assertNotEqual(bold, italic)

    def test_no_url(self):
        node =TextNode("This node has no url", TextType.BOLD)
        self.assertIsNone(node.url) 


if __name__ == "__main__":
    unittest.main()