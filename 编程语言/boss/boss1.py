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

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
		
    def error(self):
        raise Exception('invalid character')
		
    def get_next_token(self):
        match = None
        token = None
        while self.pos < len(self.text):
            for token_expr in token_exprs:
                type, pattern = token_expr
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    if type:
                        token = (type, value)
                    break
            
            if not match:
                self.error()
            else:
                self.pos = match.end(0)

            if token:
                return token
        
        return (EOF, None)
        
def main():
    text = open(sys.argv[1], 'r').read()
    lexer = Lexer(text)
    print lexer.get_next_token()
    while lexer.pos < len(lexer.text):
        print lexer.get_next_token()
 
if __name__ == '__main__':
    main()