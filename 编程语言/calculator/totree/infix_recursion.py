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
        
class infix(object):
    def __init__(self, expr):
        self.expr = expr
        self.pos = 0
        
    def expression(self):
        node = self.term()
        while self.pos < len(self.expr) and self.expr[self.pos] in ('+', '-'):
            op = self.expr[self.pos]
            self.pos += 1
            node = BinOp(node, op, self.term())
        return node
        
    def term(self):
        node = self.factor()
        while self.pos < len(self.expr) and self.expr[self.pos] in ('*', '/'):
            op = self.expr[self.pos]
            self.pos += 1
            node = BinOp(node, op, self.factor())
        return node
        
    def factor(self):
        if self.expr[self.pos].isdigit():
            node = Num(int(self.expr[self.pos]))
            self.pos += 1
        elif self.expr[self.pos] == '(':
            self.pos += 1
            node = self.expression()
            self.pos += 1
        return node
   
    def tree(self):
        return self.expression()
        
if __name__ == '__main__':
    expr = ['1', '+', '2', '*', '(', '3', '+', '4', ')', '+', '(', '8', '+', '9', '*', '10', ')', '*', '4', '-', '5']
    s = infix(expr)
    root =  s.tree()

    s = tree(root)
    print s.value()