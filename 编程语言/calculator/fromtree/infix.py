class BinOp(object):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
class Num(object):
    def __init__(self, value):
        self.value = value

class prefix(object):
    def __init__(self, root):
        self.root = root
        self.expr = []
        
    def visit(self, node):
        func = getattr(self, 'visit_' + type(node).__name__)
        return func(node)
    
    def visit_BinOp(self, node):
        self.expr.append('(')
        self.visit(node.left)
        self.expr.append(')')
        self.expr.append(node.op)
        self.expr.append('(')
        self.visit(node.right)
        self.expr.append(')')
        
    def visit_Num(self, node):
        self.expr.append(node.value)

    def fix(self):
        self.visit(root)
        
if __name__ == '__main__':
    node1 = BinOp(Num(3), '+', Num(4))
    node1 = BinOp(Num(2), '*', node1)
    node1 = BinOp(Num(1), '+', node1)
    node2 = BinOp(Num(9), '*', Num(10))
    node2 = BinOp(Num(8), '+', node2)
    node2 = BinOp(node2,  '*', Num(4))
    root  = BinOp(node1,  '+', node2)
    root  = BinOp(root,   '-', Num(5))
    
    s = prefix(root)
    s.fix()
    print s.expr