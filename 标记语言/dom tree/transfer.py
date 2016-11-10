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
    ehtml = etree.parse('index.html')
    eroot = ehtml.getroot()
    root = transfer(eroot)
    s = interpreter(root)
    print s
