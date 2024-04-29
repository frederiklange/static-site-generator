def markdown_to_blocks(markdown):
    blocks = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        if not block.isspace() and block:
            blocks.append(block.strip())
        else:
            continue
    return blocks

