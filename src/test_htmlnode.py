import unittest
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)


class TestHTMLNode(unittest.TestCase):
    # Testing class HTMLNode
    def test_eq_false(self):
        node = HTMLNode(
            tag="p", value="this is a test", props={"href": "https://www.google.com"}
        )
        node2 = HTMLNode(
            tag="p", value="this is a test", props={"href": "https://www.boot.dev"}
        )
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="p",
            value="this is a test",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p", value="this is a test")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", value="this is a test", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(
            tag="p", value="this is a test", props={"href": "https://www.boot.dev"}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(p, this is a test, None, {'href': 'https://www.boot.dev'})",
        )

    # Testing class LeafNode
    def test_to_html_no_props(self):
        leafnode = LeafNode(value="This is a paragraph of text.", tag="p")
        self.assertEqual(leafnode.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        leafnode = LeafNode(
            value="Click me!", tag="a", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            leafnode.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            leafnode = LeafNode(value=None, tag="a")
            leafnode.to_html()

    def test_to_html_empty_value(self):
        leafnode = LeafNode(value="", tag="p")
        self.assertEqual(leafnode.to_html(), "<p></p>")

    # Testing class ParentNode
    def test_to_html_simple_recursion(self):
        parentnode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parentnode.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
        )

    def test_to_html_recursion_with_parentnode(self):
        parentnode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "Italic text"),
                    ],
                ),
            ],
        )
        self.assertEqual(
            parentnode.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text<p><b>Bold text</b>Normal text<i>Italic text</i></p></p>",
        )

    def test_to_html_with_props(self):
        parentnode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", props={"href": "https://www.google.com"}),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parentnode.to_html(),
            '<p><b href="https://www.google.com">Bold text</b>Normal text<i>Italic text</i>Normal text</p>',
        )

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            parentnode = ParentNode(
                None,
                [
                    LeafNode(
                        "b", "Bold text", props={"href": "https://www.google.com"}
                    ),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "Italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            parentnode.to_html()

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            parentnode = ParentNode(
                "p",
                None,
            )
            parentnode.to_html()

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
