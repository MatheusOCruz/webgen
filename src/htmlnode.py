import functools

class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self, n=0):

        if self.children is not None:
            nl = "\n"
            tab = "\t"
            space = tab * n
            return f"<{self.tag}>{self.props_to_html()}{''.join([child.to_html(n+1) for child in self.children])}</{self.tag}>"

            #return f"{nl if n > 0 else ''}{space}<{self.tag}>{self.props_to_html()}\n{space}{''.join([child.to_html(n+1) for child in self.children])}\n{space}</{self.tag}>"
        # pure text
        if self.tag is None:
            return self.value
        tab = "\t"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

            


    def props_to_html(self):
        if self.props is None:
            return ""

        result = ""
        for k, v in self.props.items():
            result += f' {k}="{v}"' 
        return result
          
        # if you want to be fancy (aka harder to read and slower to execute 10/10 would recomend)
        # functools.reduce(lambda acc, kv: acc+ f' {kv[0]}="{kv[1]}"', self.props.items(), "")


    def __repr__(self):
        return f"\nHtmlNode(tag: <{self.tag}>, value: {self.value}, children:{self.children}, props:{self.props})"

    

# a Leaf node has no children

class HtmlLeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class HtmlParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children, props)

    def to_html(self):
        if self.tag is None or self.children is None:
            raise ValueError
        return f"<{self.tag}{self.props_to_html()}>{''.join([c.to_html() for c in self.children])}</{self.tag}>"





