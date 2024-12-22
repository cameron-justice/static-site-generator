import unittest
from parsers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "![alt text](example.com)"
        expected = [("alt text", "example.com")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_multi_image(self):
        alt1 = "obama"
        link1 = "https://en.wikipedia.org/wiki/Barack_Obama#/media/File:President_Barack_Obama.jpg"
        alt2 = "trump"
        link2 = "https://en.wikipedia.org/wiki/File:Donald_Trump_official_portrait.jpg"
        text = f"Here's Obama: ![{alt1}]({link1}) and here's Trump: ![{alt2}]({link2})"
        expected = [(alt1, link1), (alt2, link2)]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_avoid_link(self):
        text = "[alt](link.com)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)
    
class TextExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "[text](link.com)"
        expected = [("text", "link.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_multi_link(self):
        t1 = "python docs"
        link1 = "https://docs.python.org/3/"
        t2 = "c++ docs"
        link2 = "https://devdocs.io/cpp/"
        text = f"You can find docs for lots of languages, like the [{t1}]({link1}) and the [{t2}]({link2})."
        expected = [(t1, link1), (t2, link2)]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_avoid_image(self):
        text = "![alt](link.com)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block_simple(self):
        node = TextNode('code: `1 + 1`', TextType.TEXT)
        actual = split_nodes_delimiter([node], '`', TextType.CODE)
        expected = [TextNode('code: ', TextType.TEXT), TextNode('1 + 1', TextType.CODE)]
        self.assertEqual(actual, expected)

    def test_code_block_multi(self):
        nodes = [
            TextNode('Functions are defined with the `def` keyword.', TextType.TEXT),
            TextNode('Classes are defined with the `class` keyword.', TextType.TEXT)
        ]

        actual = split_nodes_delimiter(nodes, '`', TextType.CODE)
        expected = [
                TextNode('Functions are defined with the ', TextType.TEXT),
                TextNode('def', TextType.CODE),
                TextNode(' keyword.', TextType.TEXT),
                TextNode('Classes are defined with the ', TextType.TEXT),
                TextNode('class', TextType.CODE),
                TextNode(' keyword.', TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

    def test_bold_block(self):
        nodes = [TextNode('This is **bold** text!', TextType.TEXT)]
        actual = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        expected = [
            TextNode('This is ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' text!', TextType.TEXT)
        ]
        self.assertEqual(actual, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        nodes = [TextNode("image: ![alt](link.com)", TextType.TEXT)]
        actual = split_nodes_image(nodes)
        expected = [TextNode("image: ", TextType.TEXT), TextNode("alt", TextType.IMAGE, "link.com")]
        self.assertEqual(actual, expected)

    def test_multi_image(self):
        nodes = [TextNode("Image 1: ![image 1](link.com/image1) and Image 2: ![image 2](link.com/image2)", TextType.TEXT)]
        actual = split_nodes_image(nodes)
        expected = [
            TextNode("Image 1: ", TextType.TEXT),
            TextNode("image 1", TextType.IMAGE, "link.com/image1"),
            TextNode(" and Image 2: ", TextType.TEXT),
            TextNode("image 2", TextType.IMAGE, "link.com/image2")
        ]
        self.assertEqual(actual, expected)

    def test_multi_nodes(self):
        nodes = [
            TextNode("Image 1: ![alt](link.com)", TextType.TEXT),
            TextNode("Image 2: ![alt](link.com)", TextType.TEXT)
        ]
        actual = split_nodes_image(nodes)
        expected = [
            TextNode("Image 1: ", TextType.TEXT), TextNode("alt", TextType.IMAGE, "link.com"),
            TextNode("Image 2: ", TextType.TEXT), TextNode("alt", TextType.IMAGE, "link.com")
        ]
        self.assertEqual(actual, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        nodes = [TextNode("link: [alt](link.com)", TextType.TEXT)]
        actual = split_nodes_link(nodes)
        expected = [TextNode("link: ", TextType.TEXT), TextNode("alt", TextType.LINK, "link.com")]
        self.assertEqual(actual, expected)

    def test_multi_link(self):
        nodes = [TextNode("Link 1: [link 1](link.com/link1) and Link 2: [link 2](link.com/link2)", TextType.TEXT)]
        actual = split_nodes_link(nodes)
        expected = [
            TextNode("Link 1: ", TextType.TEXT),
            TextNode("link 1", TextType.LINK, "link.com/link1"),
            TextNode(" and Link 2: ", TextType.TEXT),
            TextNode("link 2", TextType.LINK, "link.com/link2")
        ]
        self.assertEqual(actual, expected)

    def test_multi_nodes(self):
        nodes = [
            TextNode("Link 1: [alt](link.com)", TextType.TEXT),
            TextNode("Link 2: [alt](link.com)", TextType.TEXT)
        ]
        actual = split_nodes_link(nodes)
        expected = [
            TextNode("Link 1: ", TextType.TEXT), TextNode("alt", TextType.LINK, "link.com"),
            TextNode("Link 2: ", TextType.TEXT), TextNode("alt", TextType.LINK, "link.com")
        ]
        self.assertEqual(actual, expected)

class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        actual = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(
            actual,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

if __name__ == "__main__":
    unittest.main()