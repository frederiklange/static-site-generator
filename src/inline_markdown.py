import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


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


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
