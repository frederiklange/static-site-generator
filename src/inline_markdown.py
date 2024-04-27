import re
from typing import Text

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("Invalid Markdown: unmatched delimiter")
            else:
                split_strings = node.text.split(delimiter)
                for index, split_text in enumerate(split_strings):
                    if split_strings[index] == "":
                        continue
                    elif index % 2 == 0:
                        new_nodes.append(TextNode(split_text, text_type_text))
                    else:
                        new_nodes.append(TextNode(split_text, text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        extracted_images = extract_markdown_images(original_text)
        if len(extracted_images) < 1:
            new_nodes.append(node)
            continue
        for image_tup in extracted_images:
            split_strings = original_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if len(split_strings) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_strings[0] == "":
                new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
            else:
                new_nodes.append(TextNode(split_strings[0], text_type_text))
                new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
            original_text = split_strings[1]
        if original_text == "":
            continue
        else:
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        extracted_links = extract_markdown_links(original_text)
        if len(extracted_links) < 1:
            new_nodes.append(node)
            continue
        for link_tup in extracted_links:
            split_strings = original_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if len(split_strings) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split_strings[0] == "":
                new_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
            else:
                new_nodes.append(TextNode(split_strings[0], text_type_text))
                new_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
            original_text = split_strings[1]
        if original_text == "":
            continue
        else:
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
