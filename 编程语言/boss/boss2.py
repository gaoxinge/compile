from boss1 import Lexer
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

class Parser(object):
    def  __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.proc = []
        self.symtb = {}
        self.func = None

    def error(self):
        raise Exception('invalid syntax')
		
    def match(self, type):
        if self.current_token[0] == type: self.current_token = self.lexer.get_next_token()
        else:                             self.error()
	
    def program(self):
        while self.current_token[0] == TYPE:
            self.function_decl()
    
    def function_decl(self):
        self.match(TYPE)
        token = self.current_token
        if token[1] in [key for key in self.symtb]:
            self.error()
        self.symtb[token[1]] = {}
        self.symtb[token[1]]['offset'] = len(self.proc)
        self.symtb[token[1]]['param'] = 0
        self.symtb[token[1]]['var'] = []
        self.func = token[1]
        self.proc.append((token[1] + ':',))
        self.proc.append(('push',))
        self.match(ID)
        self.match(LPAR2)
        self.parameter_decl()
        self.match(RPAR2)
        self.match(LPAR1)
        self.body_decl()
        self.match(RPAR1)
    
    def parameter_decl(self):
        if self.current_token[0] == VOID:
            self.match(VOID)
        else:
            tmp = 0
            self.match(TYPE)
            self.symtb[self.func]['var'].append(self.current_token[1])
            self.proc.append(('mov', '!' + str(tmp), '*' + self.current_token[1]))
            tmp += 1
            self.match(ID)
            while self.current_token[0] == COMMA:
                self.match(COMMA)
                self.match(TYPE)
                if self.current_token[1] in self.symtb[self.func]['var']:
                    self.error()
                self.symtb[self.func]['var'].append(self.current_token[1])
                self.proc.append(('mov', '!' + str(tmp), '*' + self.current_token[1]))
                tmp += 1
                self.match(ID)
            self.symtb[self.func]['param'] = tmp

    def body_decl(self):
        self.variable_decl()
        self.statement_list()

    def variable_decl(self):
        while self.current_token[0] == TYPE:
            self.match(TYPE)
            if self.current_token[1] in self.symtb[self.func]['var']:
                self.error()
            self.symtb[self.func]['var'].append(self.current_token[1])
            self.match(ID)
            self.match(SEMI)
        
    def statement_list(self):
        while self.current_token[0] != RPAR1:
            self.statement()
            
    def statement(self):
        if self.current_token[0] == ID:
            self.assign_statement()
        elif self.current_token[0] == IF:
            self.if_statement()
        elif self.current_token[0] == WHILE:
            self.while_statement()
        elif self.current_token[0] == RETURN:
            self.return_statement()
    
    def assign_statement(self):
        token = self.current_token
        if self.current_token[1] not in self.symtb[self.func]['var']:
            self.error()
        self.match(ID)
        self.match(ASSIGN)
        self.expression()
        self.proc.append(('mov', 'ax', '*' + token[1]))
        self.match(SEMI)
        
    def if_statement(self):
        self.match(IF)
        self.match(LPAR2)
        self.expression()
        token = self.current_token
        tmp1 = len(self.proc)
        if token[0] not in (EQ, NE, LT, LE, GT, GE):
            self.error()
        self.match(token[0])
        if self.current_token[1] != '0':
            self.error()
        self.match(INTEGER)
        self.match(RPAR2)
        self.match(LPAR1)
        self.statement_list()
        tmp2 = len(self.proc)
        self.match(RPAR1)
        self.match(ELSE)
        self.match(LPAR1)
        self.statement_list()
        self.match(RPAR1)
        
        block1 = self.proc[:tmp1]
        block2 = self.proc[tmp1:tmp2]
        block3 = self.proc[tmp2:]
        self.proc = block1
        if token[0] == EQ: self.proc.append(('je',  str(len(self.proc + block3) + 2)))
        if token[0] == NE: self.proc.append(('jne', str(len(self.proc + block3) + 2)))
        if token[0] == LT: self.proc.append(('jl',  str(len(self.proc + block3) + 2)))
        if token[0] == LE: self.proc.append(('jle', str(len(self.proc + block3) + 2)))
        if token[0] == GT: self.proc.append(('jg',  str(len(self.proc + block3) + 2)))
        if token[0] == GE: self.proc.append(('jge', str(len(self.proc + block3) + 2)))
        self.proc.extend(block3)
        self.proc.append(('jmp', str(len(self.proc + block2) + 1)))
        self.proc.extend(block2)
        
    def while_statement(self):
        self.match(WHILE)
        self.match(LPAR2)
        tmp1 = len(self.proc)
        self.expression()
        tmp2 = len(self.proc)
        token = self.current_token
        if token[0] not in (EQ, NE, LT, LE, GT, GE):
            self.error()
        self.match(token[0])
        if self.current_token[1] != '0':
            self.error()
        self.match(INTEGER)
        self.match(RPAR2)
        self.match(LPAR1)
        self.statement_list()
        self.match(RPAR1)
        
        block1 = self.proc[:tmp2]
        block2 = self.proc[tmp2:]
        self.proc = block1
        if token[0] == EQ: self.proc.append(('jne', str(len(self.proc + block2) + 2)))
        if token[0] == NE: self.proc.append(('je',  str(len(self.proc + block2) + 2)))
        if token[0] == LT: self.proc.append(('jge', str(len(self.proc + block2) + 2)))
        if token[0] == LE: self.proc.append(('jg',  str(len(self.proc + block2) + 2)))
        if token[0] == GT: self.proc.append(('jle', str(len(self.proc + block2) + 2)))
        if token[0] == GE: self.proc.append(('jl',  str(len(self.proc + block2) + 2)))
        self.proc.extend(block2)
        self.proc.append(('jmp', str(tmp1)))
        
    def return_statement(self):
        self.match(RETURN)
        self.expression()
        self.proc.append(('pop',))
        self.proc.append(('ret',))
        self.match(SEMI)

    def expression(self):
        self.term()
        while self.current_token[0] in (ADD, SUB):
            self.proc.append(('mov', 'ax', 'hp'))
            if self.current_token[0] == ADD:  
                self.match(ADD)
                self.term()
                self.proc.append(('add',))
            elif self.current_token[0] == SUB: 
                self.match(SUB)
                self.term()
                self.proc.append(('sub',))       
    
    def term(self):
        self.factor()
        while self.current_token[0] in (MUL, DIV):
            self.proc.append(('mov', 'ax', 'hp'))
            if self.current_token[0] == MUL: 
                self.match(MUL)
                self.factor()
                self.proc.append(('mul',))
            elif self.current_token[0] == DIV: 
                self.match(DIV)
                self.factor()
                self.proc.append(('div',))    
    
    def factor(self):
        token = self.current_token
        if token[0] == INTEGER:
            self.proc.append(('mov', token[1], 'ax'))
            self.match(INTEGER)
        elif token[0] == ID and token[1] in self.symtb[self.func]['var']:
            self.proc.append(('mov', '*' + token[1], 'ax'))
            self.match(ID)
        elif token[0] == LPAR2:
            self.match(LPAR2)
            self.expression()
            self.match(RPAR2)
        elif token[0] == ID and token[1] in [key for key in self.symtb]:
            self.match(ID)
            self.match(LPAR2)
            if self.current_token != RPAR2:
                tmp = 0
                self.expression()
                self.proc.append(('mov', 'ax', '!' + str(tmp)))
                tmp += 1
                while self.current_token[0] == COMMA:
                    self.match(COMMA)
                    self.expression()
                    self.proc.append(('mov', 'ax', '!' + str(tmp)))
                    tmp += 1
                self.match(RPAR2)
                if self.symtb[token[1]]['param'] != tmp:
                    self.error()
                self.proc.append(('call', str(self.symtb[token[1]]['offset'])))       

    def parse(self):
        self.program()

def main():
    text = open(sys.argv[1], 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    parser.parse()
    tmp = 0
    for i in parser.proc:
        print tmp,
        for j in i:
            print j,
        print
        tmp += 1
    print 
    for key, value in parser.symtb.items():
        print key + ':'
        print 'var:',
        print value['var']
        print 'param:',
        print value['param']
        print 'offset:',
        print value['offset']
        print
        
if __name__ == '__main__':
    main()