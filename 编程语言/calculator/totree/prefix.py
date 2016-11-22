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

class prefix(object):
    def __init__(self, expr):
        self.expr = expr
        
    def tree(self, expr):
        if len(expr) == 1: return Num(int(expr[0]))
        
        # from top to buttom method
        index = 0
        count = 0
        
        for i in range(1, len(expr)):
            if expr[i].isdigit(): index += 1
            else:                 index -= 1
            if index == 1:
                count = i
                break
        
        return BinOp(self.tree(expr[1:count+1]), expr[0], self.tree(expr[count+1:]))
        
    def tree_a(self):
        return self.tree(self.expr)
        
if __name__ == '__main__':
     expr = ['+','1','+','*','2','+','3','4','-','*','+','8','*','9','10','4','5']
     s = prefix(expr)
     root = s.tree_a()
     
     s = tree(root)
     print s.value()