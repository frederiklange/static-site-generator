import unittest
from htmlnode import (
    HTMLNode,
    LeafNode,
)

class TestHTMLNode(unittest.TestCase):
    def test_eq_false(self):
        node = HTMLNode(tag="p", value="this is a test", props={"href": "https://www.google.com"})
        node2 = HTMLNode(tag="p", value="this is a test", props={"href": "https://www.boot.dev"})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="p", value="this is a test", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p", value="this is a test")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", value="this is a test", props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode(tag="p", value="this is a test", props={"href": "https://www.boot.dev"})
        self.assertEqual(repr(node), "HTMLNode(p, this is a test, None, {'href': 'https://www.boot.dev'})")

    def test_to_html_no_props(self):
        leafnode = LeafNode(value="This is a paragraph of text.", tag="p")
        self.assertEqual(leafnode.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        leafnode = LeafNode(value="Click me!", tag="a", props={"href": "https://www.google.com"})
        self.assertEqual(leafnode.to_html(), '<a href="https://www.google.com">Click me!</a>') 

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            leafnode = LeafNode(value=None, tag="a")
            leafnode.to_html()
    
    def test_to_html_empty_value(self):
        leafnode = LeafNode(value="", tag="p")
        self.assertEqual(leafnode.to_html(), '<p></p>')

if __name__ == "__main__":
    unittest.main()
