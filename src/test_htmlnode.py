import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_p_tag_simple(self):
        node = HTMLNode('p', 'This is a p tag!')
        self.assertEqual(node.__repr__(), "<p>This is a p tag!</p>")

    def test_props(self):
        node = HTMLNode('p', 'This is a p tag!', props={ "color": "blue" })
        self.assertEqual(node.__repr__(), "<p color=\"blue\">This is a p tag!</p>")

    def test_children(self):
        node = HTMLNode('div', children=[HTMLNode('p', 'Child 1'), HTMLNode('p', 'Child 2')])
        expected = """<div><p>Child 1</p><p>Child 2</p></div>"""
        self.assertEqual(node.__repr__(), expected)

    def test_children_with_props(self):
        node = HTMLNode('div', children=[HTMLNode('p', 'Child 1', props={ "color": "blue" }), HTMLNode('p', 'Child 2', props={"color": "red"})])
        expected = """<div><p color="blue">Child 1</p><p color="red">Child 2</p></div>"""
        self.assertEqual(node.__repr__(), expected)

    def test_multi_layer_children(self):
        node = HTMLNode('div', children=[HTMLNode('div', children=[HTMLNode('p', 'second layer!')]), HTMLNode('p', 'first layer!')])
        expected = """<div><div><p>second layer!</p></div><p>first layer!</p></div>"""

class TestLeafNode(unittest.TestCase):
    def test_no_tag(self):
        node = LeafNode(None, 'Leaf!')
        self.assertEqual(node.to_html(), 'Leaf!')

    def test_with_tag(self):
        node = LeafNode('p', 'Leaf!')
        self.assertEqual(node.to_html(), '<p>Leaf!</p>')

    def test_with_props(self):
        node = LeafNode('p', 'Leaf!', props={ "color": "blue" })
        self.assertEqual(node.to_html(), "<p color=\"blue\">Leaf!</p>")

    def test_without_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode('p', None)
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_with_children(self):
        node = ParentNode("div", [LeafNode('p', 'leaf 1'), LeafNode('p', 'leaf 2')])
        expected = """<div><p>leaf 1</p><p>leaf 2</p></div>"""
        self.assertEqual(node.to_html(), expected)

    def test_with_props(self):
        children = [
            LeafNode("p", "blue leaf", props={ "color": "blue" }),
            LeafNode("p", "red leaf", props={ "color": "red"})
        ]
        node = ParentNode("div", children, props={ "width": "100%" })
        expected="""<div width="100%"><p color="blue">blue leaf</p><p color="red">red leaf</p></div>"""
        self.assertEqual(node.to_html(), expected)

    def test_without_tag(self):
        with self.assertRaises(ValueError) as ctx:
            node = ParentNode(None, [LeafNode('p', 'leaf')])
            node.to_html()
        self.assertEqual("ParentNode must have a tag", str(ctx.exception))

    def test_without_children(self):
        with self.assertRaises(ValueError) as ctx:
            node = ParentNode('div', None)
            node.to_html()
        self.assertEqual("ParentNode must have children", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()