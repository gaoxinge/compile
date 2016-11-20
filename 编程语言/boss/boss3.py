from boss1 import Lexer
from boss2 import Parser
import sys
import re

ADD     = '+'
SUB     = '-'
MUL     = '*'
DIV     = '/'
EQ      = '=='
NE      = '!='
LT      = '<'
LE      = '<='
GT      = '>'
GE      = '>='
LPAR1   = '{'
RPAR1   = '}'
LPAR2   = '('
RPAR2   = ')'
SEMI    = ';'
COMMA   = ','
ASSIGN  = '='
TYPE    = 'int'
VOID    = 'void'
IF      = 'if'
ELSE    = 'else'
WHILE   = 'while'
RETURN  = 'return'
INTEGER = 'INTEGER'
ID      = 'ID'
EOF     = 'EOF'

token_exprs = [
    (None,    r'[ \n\t]+'),
    (None,    r'//[^\n]*'),
    (ADD,     r'\+'),
    (SUB,     r'-'),
    (MUL,     r'\*'),
    (DIV,     r'/'),
    (EQ,      r'=='),
    (NE,      r'!='),
    (LT,      r'<'),
    (LE,      r'<='),
    (GT,      r'>'),
    (GE,      r'>='),
    (LPAR1,   r'{'),
    (RPAR1,   r'}'),
    (LPAR2,   r'\('),
    (RPAR2,   r'\)'),
    (SEMI,    r';'),
    (COMMA,   r','),
    (ASSIGN,  r'='),
    (TYPE,    r'int'),
    (VOID,    r'void'),
    (IF,      r'if'),
    (ELSE,    r'else'),
    (WHILE,   r'while'),
    (RETURN,  r'return'),
    (INTEGER, r'[0-9]+'),
    (ID,      r'[A-Za-z][A-Za-z0-9_]*'),
]

class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser
        self.ax = 0
        self.pc = 0
        self.heap = []
        self.stack = []
    
    def mov(self, s1, s2):
        if s1.isdigit():   self.ax = int(s1)
        elif s1[0] == '!': self.stack[-1]['var'][s2[1:]] = self.stack[-2]['param'][int(s1[1:])]
        elif s1[0] == '*': self.ax = self.stack[-1]['var'][s1[1:]]
        elif s2 == 'hp':   self.heap.append(self.ax)
        elif s2[0] == '!': self.stack[-1]['param'].append(self.ax)
        elif s2[0] == '*': self.stack[-1]['var'][s2[1:]] = self.ax
        self.pc += 1
        
    def push(self):
        tmp = {}
        tmp['var'] = {}
        tmp['param'] = []
        tmp['pc'] = -1
        self.stack.append(tmp)
        self.pc += 1
        
    def pop(self):
        self.stack.pop()
        self.stack[-1]['param'] = []
        self.pc += 1
        
    def add(self):
        self.ax = self.heap.pop() + self.ax
        self.pc += 1
        
    def sub(self):
        self.ax = self.heap.pop() - self.ax
        self.pc += 1
        
    def mul(self):
        self.ax = self.heap.pop() * self.ax
        self.pc += 1
        
    def div(self):
        self.ax = self.heap.pop() / self.ax
        self.pc += 1
    
    def jmp(self, s):
        self.pc = int(s)
    
    def je(self, s):
        if(self.ax == 0): self.pc = int(s)
        else:             self.pc += 1
    
    def jne(self, s):
        if(self.ax != 0): self.pc = int(s)
        else:             self.pc += 1
    
    def jl(self, s):
        if(self.ax < 0):  self.pc = int(s)
        else:             self.pc += 1
    
    def jle(self, s):
        if(self.ax <= 0): self.pc = int(s)
        else:             self.pc +=1
    
    def jg(self, s):
        if(self.ax > 0):  self.pc = int(s)
        else:             self.pc += 1
    
    def jge(self):
        if(self.ax >= 0): self.pc = int(s)
        else:             self.pc += 1
    
    def call(self, s):
        self.stack[-1]['pc'] = self.pc + 1
        self.pc = int(s)
        
    def ret(self):
        self.pc = self.stack[-1]['pc']
        
    def run(self):
        self.parser.parse()
        self.pc = self.parser.proc.index(('main:',)) + 1
        self.fi = self.parser.proc.index(('ret',), self.pc) - 2
        while self.pc <= self.fi:
            tmp = self.parser.proc[self.pc][0]
            if tmp == 'mov':    self.mov(self.parser.proc[self.pc][1], self.parser.proc[self.pc][2])
            elif tmp == 'push': self.push()
            elif tmp == 'pop':  self.pop()
            elif tmp == 'add':  self.add()
            elif tmp == 'sub':  self.sub()
            elif tmp == 'mul':  self.mul()
            elif tmp == 'div':  self.div()
            elif tmp == 'jmp':  self.jmp(self.parser.proc[self.pc][1])
            elif tmp == 'je':   self.je(self.parser.proc[self.pc][1])
            elif tmp == 'jne':  self.jne(self.parser.proc[self.pc][1])
            elif tmp == 'jl':   self.jl(self.parser.proc[self.pc][1])
            elif tmp == 'jle':  self.jle(self.parser.proc[self.pc][1])
            elif tmp == 'jg':   self.jg(self.parser.proc[self.pc][1])
            elif tmp == 'jge':  self.jge(self.parser.proc[self.pc][1])
            elif tmp == 'call': self.call(self.parser.proc[self.pc][1])
            elif tmp == 'ret':  self.ret()
            else:               self.pc += 1

def main():
    text = open(sys.argv[1], 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.run()
    print 'main:'
    for key, value in interpreter.stack[0]['var'].items():
        print key + ' = ' + str(value)
    
if __name__ == '__main__':
    main()