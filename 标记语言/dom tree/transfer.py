from AST import AST
from interpreter import interpreter
from lxml import etree

class AST:
    def __init__(self, name):
        self.name = name
        self.childrens = []

def transfer(eroot):
    root = AST(eroot.tag)
    for echild in eroot.getchildren():
        root.childrens.append(transfer(echild))
    return root

if __name__ == '__main__':
    html = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
    eroot = etree.HTML(html)
    root = transfer(eroot)
    s = interpreter(root)
    print s
