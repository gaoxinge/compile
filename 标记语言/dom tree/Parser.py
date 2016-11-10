from AST import AST
from Lexer import Lexer
from interpreter import interpreter

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.stack = [AST('root')]
        self.symbol = ['img', 'br', 'hr', 'col', 'area', 'link', 'meta', 'frame', 'input', 'param']

    def eat(self):
        self.current_token = self.lexer.get_next_token()

    def parser(self):
        while self.current_token is not None:
            if self.current_token == '<':
                self.eat()
                if self.current_token[0] == '!':
                    self.stack[-1].childrens.append(AST(self.current_token))
                elif self.current_token.split(' ')[0] in self.symbol:
                    self.stack[-1].childrens.append(AST(self.current_token.slit(' ')[0]))
                elif self.current_token[0] != '/':
                    node = AST(self.current_token.split(' ')[0])
                    self.stack[-1].childrens.append(node)
                    self.stack.append(node)
                else:
                    if self.current_token.split('/')[1] == self.stack[-1].name:
                        self.stack.pop()
                self.eat()
            else:
                self.stack[-1].childrens.append(AST(self.current_token))
                self.eat()
        return self.stack[0]

if __name__ == '__main__':
    html = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
 '''

    lexer = Lexer(html)
    parser = Parser(lexer)
    s = interpreter(parser.parser())
    print s


    
