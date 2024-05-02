block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

from htmlnode import(
    HTMLNode,
    LeafNode,
    ParentNode,
    ) 

def markdown_to_blocks(markdown):
    blocks = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        if not block.isspace() and block:
            blocks.append(block.strip())
        else:
            continue
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph    
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph    
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_htmlnode(markdown):
    return None

def paragraph_to_html(block):
    return HTMLNode(tag="p", value=block)

def heading_to_html(block):
    heading_size = len(block.split()[0])
    return HTMLNode(tag=f"h{heading_size}", value=block[heading_size+1:])

def code_to_html(block):
    return HTMLNode(tag="code", value=block)

def quote_to_html(block):
    return HTMLNode(tag="blockquote", value=block)

def ulist_to_html(block):
    html_lines = []
    lines = block.split("\n")
    for line in lines:
        html_line = f"<li>{" ".join(line.split()[1:])}</li>"
        html_lines.append(html_line)
    return HTMLNode(tag="ul", value="".join(html_lines))

def olist_to_html(block):
    html_lines = []
    lines = block.split("\n")
    for line in lines:
        html_line = f"<li>{" ".join(line.split()[1:])}</li>"
        html_lines.append(html_line)
    return HTMLNode(tag="ol", value="".join(html_lines))



    
