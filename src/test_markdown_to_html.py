import unittest
from markdown_to_html import *
from textnode import *
from htmlnode import *

class MarkdownToHtmlTest(unittest.TestCase):
    def test_textNode_to_htmlLeaf_text(self):
         
        node = TextNode("rusbe", TextType.Text)
        html = text_node_to_html_node(node)
        expected = "rusbe"
        self.assertEqual(html.to_html(), expected)

    def test_textNode_to_htmlLeaf_bold(self):
         
        node = TextNode("rusbe", TextType.Bold)
        html = text_node_to_html_node(node)
        expected = "<b>rusbe</b>"
        self.assertEqual(html.to_html(), expected)
    
    def test_textNode_to_htmlLeaf_italic(self):
         
        node = TextNode("rusbe", TextType.Italic)
        html = text_node_to_html_node(node)
        expected = "<i>rusbe</i>"
        self.assertEqual(html.to_html(), expected)

    def test_textNode_to_htmlLeaf_code(self):
         
        node = TextNode("rusbe", TextType.Code)
        html = text_node_to_html_node(node)
        expected = "<code>rusbe</code>"
        self.assertEqual(html.to_html(), expected)

    def test_textNode_to_htmlLeaf_link(self):
         
        node = TextNode("rusbe", TextType.Link, "www.rusbe")
        html = text_node_to_html_node(node)
        expected = '<a href="www.rusbe">rusbe</a>'
        self.assertEqual(html.to_html(), expected)

    def test_textNode_to_htmlLeaf_image(self):
         
        node = TextNode("rusbe", TextType.Image, "www.rusbe")
        html = text_node_to_html_node(node)
        expected = '<img src="www.rusbe" alt="rusbe"></img>'
        self.assertEqual(html.to_html(), expected)


    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is text with a `code block` word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.Code)
        expected = [
        TextNode("This is text with a ", TextType.Text),
        TextNode("code block", TextType.Code),
        TextNode(" word", TextType.Text),
        ]    
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i]) 

    def test_extract_link(self):
        text = "This is text with a link  [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [('to boot dev', 'https://www.boot.dev','l'), ('to youtube', 'https://www.youtube.com/@bootdotdev','l')]
        result = extract_markdown_images_and_links(text)

        self.assertEqual(result, expected)

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif','i'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg','i')]      
        result = extract_markdown_images_and_links(text)

        self.assertEqual(result, expected)

    def text_extract_image_and_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) a[to boot dev](https://www.boot.dev) nd ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) This is text with a link and [to youtube](https://www.youtube.com/@bootdotdev)"
        
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif',"i"), ('to boot dev', 'https://www.boot.dev','l'),
                    ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg','i'), ('to youtube', 'https://www.youtube.com/@bootdotdev','l')] 
        
        result = extract_markdown_images_and_links(text)

        self.assertEqual(result, expected)




