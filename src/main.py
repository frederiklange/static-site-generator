from textnode import TextNode

def main():
    test_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    
    print(test_node.text)
    print(test_node.text_type)
    print(test_node.url)
    print(test_node.__repr__())
    
    test_node_2 = TextNode("This is a text node", "italic")

    print(test_node.__eq__(test_node_2))

main()