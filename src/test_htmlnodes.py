import unittest

from htmlnode import HtmlNode, HtmlLeafNode, HtmlParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props(self):
        node = HtmlNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected, "test_props failed")

    def test_props_empty(self):
        node = HtmlNode(tag="a", props={})
        expected = ""
        self.assertEqual(node.props_to_html(), expected, "test_props_empty failed")

    def test_props_none(self):
        node = HtmlNode(tag="a")
        expected = ""
        self.assertEqual(node.props_to_html(), expected, "test_props_empty failed")

    def test_leaf_to_html(self):
        node1 = HtmlNode("p", "This is a paragraph of text.")
        expected1 = '<p>This is a paragraph of text.</p>'

        node2 = HtmlNode("a", "Click me!", None,{"href": "https://www.google.com"})  
        expected2 = '<a href="https://www.google.com">Click me!</a>'

        self.assertEqual(node1.to_html().replace("\n","").replace('\t',""), expected1)
        self.assertEqual(node2.to_html(), expected2)
    
    
    def test_parent_to_html(self):
        node = HtmlNode("p", None,
        [
        HtmlNode("b", "Bold text"),
        HtmlNode(None, "Normal text"),
        HtmlNode("i", "italic text"),
        HtmlNode(None, "Normal text"),
        ],
        )
        expected='<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html().replace("\n","").replace('\t',""),expected)

    def test_parent_html_2(self):

        node = HtmlNode("div", None,
        [
        HtmlNode("p", None,
            [
            HtmlNode("b", "Bold text"),
            HtmlNode(None, "Normal text"),
            HtmlNode("i", "italic text"),
            HtmlNode(None, "Normal text"),
            ]),
        HtmlNode("p", None,
            [
            HtmlNode("b", "Bold text"),
            HtmlNode(None, "Normal text"),
            HtmlNode("i", "italic text"),
            HtmlNode(None, "Normal text"),
            ]),
        ])
        expected='<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>'

        self.assertEqual(node.to_html().replace("\n","").replace('\t',""),expected)
