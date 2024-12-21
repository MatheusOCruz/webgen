import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertEqual(node, node2, "test_eq fail")

    def test_dif_type(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Text)
        self.assertNotEqual(node, node2, "test_dif failed")

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.Link, "www.site.com")
        node2 = TextNode("This is a text node", TextType.Link)
        self.assertNotEqual(node, node2, "test_url failed")

    def test_url_empty(self):
        node = TextNode("This is a text node", TextType.Link, "www.site.com")
        node2 = TextNode("This is a text node", TextType.Link, "")
        self.assertNotEqual(node, node2, "test_url_empty failed")


if __name__ == "__main__":
    unittest.main()
