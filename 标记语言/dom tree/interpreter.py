from AST import AST

def interpreter(ast, depth = 1, final = False):
    s = ''
    
    if depth == 1:
        s = str(ast.name)
    else:
        s = ' ' * (depth - 2) * 5  + '-----' + str(ast.name) 

    for i in range(0, len(ast.childrens)):
        s += '\n' + ' ' * (depth - 1) * 5 + '|\n' + interpreter(ast.childrens[i], depth + 1)

    return s

if __name__ == '__main__':
    #depth = 1 
    root = AST(1)

    #depth = 2
    b1 = AST(2)
    b2 = AST(3)

    #depth = 3
    c1 = AST(4)
    c2 = AST(5)
    
    d1 = AST(6)
    d2 = AST(7)
    d3 = AST(8)

    #depth = 4
    e1 = AST(9)
    e2 = AST(10)

    f1 = AST(11)
    f2 = AST(12)

    g1 = AST(13)
    
    root.childrens.append(b1)
    root.childrens.append(b2)
    b1.childrens.append(c1)
    b1.childrens.append(c2)
    b2.childrens.append(d1)
    b2.childrens.append(d2)
    b2.childrens.append(d3)
    c1.childrens.append(e1)
    c1.childrens.append(e2)
    d2.childrens.append(f1)
    d2.childrens.append(f2)
    d3.childrens.append(g1)

    s = interpreter(root)
    print s
