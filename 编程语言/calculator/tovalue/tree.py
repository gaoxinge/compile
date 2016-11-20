class BinOp(object):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
class Num(object):
    def __init__(self, value):
        self.value = value
       
class tree(object):
    def __init__(self, root):
        self.root = root
        
    def visit(self, node):
        func = getattr(self, 'visit_' + type(node).__name__)
        return func(node)
        
    def visit_BinOp(self, node):
        if node.op == '+': return self.visit(node.left) + self.visit(node.right)
        if node.op == '-': return self.visit(node.left) - self.visit(node.right)
        if node.op == '*': return self.visit(node.left) * self.visit(node.right)
        if node.op == '/': return self.visit(node.left) / self.visit(node.right)
        
    def visit_Num(self, node):
        return node.value
        
    def value(self):
        return self.visit(self.root)
        
if __name__ == '__main__':
    node1 = BinOp(Num(3), '+', Num(4))
    node1 = BinOp(Num(2), '*', node1)
    node1 = BinOp(Num(1), '+', node1)
    node2 = BinOp(Num(9), '*', Num(10))
    node2 = BinOp(Num(8), '+', node2)
    node2 = BinOp(node2,  '*', Num(4))
    root  = BinOp(node1,  '+', node2)
    root  = BinOp(root,   '-', Num(5))
    
    s = tree(root)
    print s.value()