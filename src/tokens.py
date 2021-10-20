from scanner import *
from translator import *

TT_INT			= 'INT'
TT_STRING       = 'STRING'
TT_FLOAT    	= 'FLOAT'
TT_IDENTIFIER	= 'IDENTIFIER'
TT_KEYWORD		= 'KEYWORD'
TT_PLUS     	= 'PLUS'
TT_MINUS    	= 'MINUS'
TT_MUL      	= 'MUL'
TT_DIV      	= 'DIV'
TT_POW			= 'POW'
TT_EQ			= 'EQ'
TT_LPAREN   	= 'LPAREN'
TT_RPAREN   	= 'RPAREN'
TT_EE			= 'EE'
TT_NE		    = 'NE'
TT_LT		    = 'LT'
TT_GT			= 'GT'
TT_LTE			= 'LTE'
TT_GTE			= 'GTE'
TT_EOF			= 'EOF'
TT_NEWLINE      = 'NEWLINE'
TT_OPENBRACKET  = 'OPENBRACKET'
TT_CLOSEBRACKET = 'CLOSEBRACKET'
TT_QUOTE        = 'QUOTE'
TT_LARRAY       = 'LARRAY'
TT_RARRAY       = 'RARRAY'
TT_COMMA        = 'COMMA'
TT_PLUSPLUS     = '++'
TT_MINUSMINUS     = '--'
TT_PRINT        = 'PRINT'
TT_TAB          = 'TAB'
TT_PLUSEQ       = '+='
TT_MINUSEQ       = '-='
TT_MULEQ        = '*='
TT_DIVEQ        = '/='

KEYWORDS = [
    'double',
    'String',
    'System.out.print',
    'System.out.println',
    'args',
    'main',
    'abstract',
    'continue',
    'for',
    'new',
    'switch',
    'assert',
    'default',
    'goto',
    'package',
    'synchronized',
    'boolean',
    'do',
    'if',
    'private',
    'this',
    'break',
    'double',
    'implements',
    'protected',
    'throw',
    'byte',
    'else',
    'import',
    'public',
    'throws',
    'case',
    'enum',
    'instanceof',
    'return',
    'transient',
    'catch',
    'extends',
    'int',
    'short',
    'try',
    'char',
    'final',
    'interface',
    'static',
    'void',
    'class',
    'finally',
    'long',
    'strictfp',
    'volatile',
    'const',
    'float',
    'native',
    'super',
    'while'
]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}\n'
        return f'{self.type}\n'