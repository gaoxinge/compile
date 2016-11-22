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

class suffix(object):
    def __init__(self, expr):
        self.expr = expr
     
    # from buttom to top method
    def tree(self):
        stack = []
        
        for i in self.expr:
            if i.isdigit(): stack.append(Num(int(i)))
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(BinOp(a, i, b))
                
        return stack[0]
        
if __name__ == '__main__':
    expr = ['1','2','3','4','+','*','+','8','9','10','*','+','4','*','+','5','-']
    s = suffix(expr)
    root = s.tree()
    
    s = tree(root)
    print s.value()