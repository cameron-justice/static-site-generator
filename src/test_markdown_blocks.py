import unittest
from markdown_blocks import markdown_to_blocks, extract_title

class TestMarkdownToBlocks(unittest.TestCase):
    def test_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertEqual(markdown_to_blocks(markdown), ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item'])

class TestExtractTitle(unittest.TestCase):
    def test_single_heading(self):
        markdown = "# Title"
        self.assertEqual(extract_title(markdown), "Title")

    def test_multi_headings(self):
        markdown = "# Title\n\ncontent\n\n## Subtitle"
        self.assertEqual(extract_title(markdown), "Title")

if __name__ == "__main__":
    unittest.main()