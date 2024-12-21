from textnode import TextNode, TextType
from htmlnode import HtmlNode
from blocknode import BlockNode, BlockType
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.Text:
            return HtmlNode(value = text_node.text)
        case TextType.Bold:
            return HtmlNode("b", text_node.text)
        case TextType.Italic:
            return HtmlNode("i", text_node.text)
        case TextType.Code:
            return HtmlNode("code", text_node.text)
        case TextType.Link:
            return HtmlNode("a", text_node.text, props = {"href": text_node.url})
        case TextType.Image:
            return HtmlNode("img", "", props = {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    pad = len(delimiter)
    for node in old_nodes:
        if node.text_type != TextType.Text:
            new_nodes.append(node)
            continue

        text = node.text
        start_pos = text.find(delimiter)
        if start_pos == -1:
            new_nodes.append(node)
            continue
        end_pos = text.find(delimiter, start_pos+pad)

        if start_pos > 0:
            new_nodes.append(TextNode(text[:start_pos], TextType.Text))
         
        new_nodes.append(TextNode(text[start_pos+pad:len(text) if end_pos == -1 else end_pos], text_type))

        if end_pos != -1 and end_pos + pad != len(text) :
            new_nodes.append(TextNode(text[end_pos+pad:], TextType.Text))

    return new_nodes
# ![rick roll](https://i.imgur.com/aKaOqIh.gif) for image 
#  [rick roll](https://i.imgur.com/aKaOqIh.gif) for link 

def extract_markdown_images_and_links(text):
    # capture [alt](link) and ! if there is one 
    matches = re.findall(r"(?:!|)\[.*?\]\(.*?\)", text)
    found = []
    for entry in matches:
        entry = entry.split("](")
        if entry[0][0] == "!":
            found.append( (entry[0][2:], entry[1][:-1], "i") )
        else:
            found.append( (entry[0][1:], entry[1][:-1], "l") )

    return found


def split_node_links_and_images(node):
    text = node.text
   
    found = extract_markdown_images_and_links(text)
 
    
    nodes = []
    if not found:
        return [node]
    for entry in found:
        if entry[2] == 'l':
            start = text.find(f"[{entry[0]}]({entry[1]})")
            end = start + len(entry[0]) + len(entry[1]) + 4
            nodes.append(TextNode(text[:start],TextType.Text))
            nodes.append(TextNode(entry[0], TextType.Link, entry[1]))
            text = text[end:]
        elif entry[2] == 'i':
            start = text.find(f"![{entry[0]}]({entry[1]})")
            end = start + len(entry[0]) + len(entry[1]) + 5
            nodes.append(TextNode(text[:start],TextType.Text))
            nodes.append(TextNode(entry[0], TextType.Image, entry[1]))
            text = text[end:]
    return nodes




def split_nodes(node):
    nodes = split_node_links_and_images(node)
    nodes = split_nodes_delimiter(nodes,"**",TextType.Bold)
    nodes = split_nodes_delimiter(nodes,"*", TextType.Italic)
    nodes = split_nodes_delimiter(nodes,"`", TextType.Code)
    
    return nodes




        
    

def text_to_nodes(text):
    first_node = TextNode(text, TextType.Text)
    return split_nodes(first_node)


def get_block_type(block_text):
    if re.findall(r"^#{1,6} ", block_text):
        return BlockType.Heading
    
    if re.findall(r"^```.*?```", block_text, re.DOTALL):
        return BlockType.Code
    
    if len(re.findall(r"[*-] .*?\n?", block_text)) == len(block_text.split("\n")) and re.findall(r"^[*-] .*?\n?", block_text):
        return BlockType.UnorderedList

    if len(re.findall(r"\d+. \n?", block_text)) == len(block_text.split("\n")):
        return BlockType.OrderedList

    if re.findall(r">.*?\n?",block_text):
        return BlockType.Quote
    
    return BlockType.Paragraph

 
def markdown_to_blocks(markdown_text):
    blocks_as_text = []
    for block in markdown_text.split("\n\n"):
        block = '\n'.join(line for line in block.split("\n") if line != "")
        blocks_as_text.append(block)

    blocks = []

    for block_text in blocks_as_text:
        block_type = get_block_type(block_text)
        block = BlockNode(block_text, block_type)

        blocks.append(block)
    return blocks




def blocknode_to_htmlnode(block):
    match block.block_type:
        case BlockType.Paragraph:

            text_nodes = text_to_nodes(block.content)
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return HtmlNode('p',children=html_nodes)

        case BlockType.UnorderedList:
            items_text = block.content.split("\n")
            ul_html_items = []
            for item in items_text:
                # just reasures that every item is properly written
                assert re.match(r"^[*-] .*", item), item
                item = item[2:]
                if item.startswith(" "):
                    item = item[1:]
                text_nodes = text_to_nodes(item) # just the item string
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                html_item = HtmlNode("li", children=html_nodes)
                ul_html_items.append(html_item)

            return HtmlNode("ul", children=ul_html_items)

        case BlockType.OrderedList:
            count = 1
            items_text = block.content.split("\n")
            ul_html_items = []
            
            for item in items_text:
                # just reasures that every item is properly written
                assert re.match(r"^"+ str(count) + ". *", item)
                count+=1
                text_nodes = text_to_nodes(item[3:]) # just the item string
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                html_item = HtmlNode("li", children=html_nodes)
                ul_html_items.append(html_item)

   
            return HtmlNode("ol", children=ul_html_items)

        case BlockType.Heading:
            text = block.content
            
            heading_size = text.find(" ")
            assert heading_size <= 6
            text_nodes = text_to_nodes(text[heading_size+1:])
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return HtmlNode(f"h{heading_size}",children=html_nodes)
            
        case BlockType.Code:
            code_text = block.content
            #print(code_text)
            code_node = TextNode("\n".join(code_text.split('\n')[1:-1]), TextType.Code)
            html_code = text_node_to_html_node(code_node)
            
            return HtmlNode("pre", children=[html_code])

        case BlockType.Quote:
            quote = block.content.replace("> ","")

            text_nodes = text_to_nodes(quote)
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]

            return HtmlNode("blockquote", children=html_nodes)

                
                



def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    #print(blocks)
    html_nodes = list(filter(lambda x: x != None, [blocknode_to_htmlnode(block) for block in blocks]))
    return "".join([html.to_html() for html in html_nodes])
    #html = HtmlNode("div", children=html_nodes)
    #return html.to_html()

    

    


