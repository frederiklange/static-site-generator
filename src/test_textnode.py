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

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_text, "www.boot.dev")
        node2 = TextNode("This is a text node", text_type_text, "www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq__url_false(self):
        node = TextNode("This is a text node", text_type_text, "www.boot.dev")
        node2 = TextNode("This is a text node2", text_type_text, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a text node, text, www.boot.dev)" )


if __name__ == "__main__":
    unittest.main()
