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

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)


class TestInlineMarkdown(unittest.TestCase):
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

    def test_extract_images_two_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertListEqual(
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
            extract_markdown_images(text),
        )

    def test_extract_images_one_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        self.assertListEqual(
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
            ],
            extract_markdown_images(text),
        )

    def test_extract_links_two_links(self):
        text = "This is text with an [link](www.google.com) and [another](www.boot.dev/another)"
        self.assertListEqual(
            [
                (
                    "link",
                    "www.google.com",
                ),
                (
                    "another",
                    "www.boot.dev/another",
                ),
            ],
            extract_markdown_links(text),
        )

    def test_extract_links_one_link(self):
        text = "This is text with an [link](www.boot.dev/another)"
        self.assertListEqual(
            [
                (
                    "link",
                    "www.boot.dev/another",
                ),
            ],
            extract_markdown_links(text),
        )

    def test_split_nodes_images_two(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
            ],
            split_nodes_images([node]),
        )
   
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.com) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.com)",
            text_type_text
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.com"),
                TextNode(" and another ", text_type_text),
                TextNode("second link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.com"),
            ],
            split_nodes_links([node]),
        )

    def test_text_to_test_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )
    
if __name__ == "__main__":
    unittest.main()
