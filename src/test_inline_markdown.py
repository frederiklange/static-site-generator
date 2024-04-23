import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from inline_markdown import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is a **bold** text node", text_type_text)
        self.assertListEqual(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("This is a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" text node", text_type_text),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is a *italic* text node", text_type_text)
        self.assertListEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("This is a ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" text node", text_type_text),
            ],
        )

    def test_split_nodes_delimiter_multiple_nodes(self):
        node = TextNode("This is a `code block` text node", text_type_text)
        node_2 = TextNode("This is a `code block` text node", text_type_text)
        self.assertListEqual(
            split_nodes_delimiter([node, node_2], "`", text_type_code),
            [
                TextNode("This is a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" text node", text_type_text),
                TextNode("This is a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" text node", text_type_text),
            ],
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
