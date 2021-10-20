from .scanner import *
from .tokens import *

#######################################
# Translator & Deleted keywords
#######################################
DELETE = [
    'double',
    'String',
    'args',
    'main',
    'continue',
    'new',
    'switch',
    'assert',
    'default',
    'goto',
    'package',
    'synchronized',
    'boolean',
    'this',
    'break',
    'double',
    'implements',
    'protected',
    'throw',
    'byte',
    'public',
    'throws',
    'case',
    'enum',
    'instanceof',
    'transient',
    'extends',
    'int',
    'short',
    'char',
    'final',
    'interface',
    'static',
    'void',
    'finally',
    'long',
    'strictfp',
    'volatile',
    'const',
    'float',
    'native',
    'super',
]
class Translator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        self.translatedToken = []

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def peek(self, peek_idx):
        self.tok_idx_copy = self.tok_idx
        self.tok_idx_copy += peek_idx
        if self.tok_idx_copy < len(self.tokens):
            self.current_tok_copy = self.tokens[self.tok_idx_copy]
        return self.current_tok_copy

    def __repr__(self):
        return f'{self.current_tok}\n'

    def translate(self):
            while self.current_tok != None:
                if self.current_tok.type == TT_PLUS:
                    self.translatedToken.append('+')
                    self.advance()
                elif self.current_tok.type == TT_MINUS:
                    self.translatedToken.append('-')
                    self.advance()
                elif self.current_tok.type == TT_IDENTIFIER:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
                elif self.current_tok.type == TT_EQ:
                    self.translatedToken.append('=')
                    self.advance()
                elif self.current_tok.type == TT_INT:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
                elif self.current_tok.type == TT_FLOAT:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
                elif self.current_tok.type == TT_NEWLINE:
                    self.translatedToken.append('\n')
                    self.advance()
                elif self.current_tok.value == 'System.out.print' or self.current_tok.value == 'System.out.println':
                    self.translatedToken.append('print')
                    self.advance()
                elif self.current_tok.value == 'import':
                    self.peek(1)
                    if self.current_tok_copy.value == 'java.util.Scanner':
                        self.advance()
                        self.advance()
                    else: self.translatedToken.append(self.current_tok)
                    self.advance()
                elif self.current_tok.value == 'void':
                    self.peek(1)
                    if self.current_tok_copy.value == 'main':
                        while self.current_tok.type != TT_OPENBRACKET:
                            self.advance()
                        self.advance()
                    else: self.advance()
                elif self.current_tok.value in DELETE:
                    self.advance()
                elif self.current_tok.value in KEYWORDS:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
                elif self.current_tok.type == TT_OPENBRACKET:
                    self.translatedToken.append(':\n\t')
                    self.advance()
                elif self.current_tok.type == TT_CLOSEBRACKET:
                    self.translatedToken.append('\n')
                    self.advance()
                elif self.current_tok.type == TT_LPAREN:
                    self.translatedToken.append('(')
                    self.advance()
                elif self.current_tok.type == TT_RPAREN:
                    self.translatedToken.append(')')
                    self.advance()
                elif self.current_tok.type == TT_RARRAY:
                    self.translatedToken.append(']')
                    self.advance()
                elif self.current_tok.type == TT_LARRAY:
                    self.translatedToken.append('[')
                    self.advance()
                elif self.current_tok.type == TT_COMMA:
                    self.translatedToken.append(',')
                    self.advance()
                elif self.current_tok.type == TT_STRING:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
                elif self.current_tok.type == TT_MUL:
                    self.translatedToken.append('*')
                    self.advance()
                elif self.current_tok.type == TT_DIV:
                    self.translatedToken.append('/')
                    self.advance()
                elif self.current_tok.type == TT_LT:
                    self.translatedToken.append('<')
                    self.advance()
                elif self.current_tok.type == TT_GT:
                    self.translatedToken.append('>')
                    self.advance()
                elif self.current_tok.type == TT_LTE:
                    self.translatedToken.append('<=')
                    self.advance()
                elif self.current_tok.type == TT_GTE:
                    self.translatedToken.append('>=')
                    self.advance()
                elif self.current_tok.type == TT_PLUSPLUS:
                    self.translatedToken.append('+= 1')
                    self.advance()
                elif self.current_tok.type == TT_MINUSMINUS:
                    self.translatedToken.append('-= 1')
                    self.advance()
                elif self.current_tok.type == TT_MULEQ:
                    self.translatedToken.append('*=')
                    self.advance()
                elif self.current_tok.type == TT_DIVEQ:
                    self.translatedToken.append('/=')
                    self.advance()
                else:
                    self.translatedToken.append('EOF')
                    return self.translatedToken


#######################################
# Translate Keywords
#######################################
class Translate_Keywords:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        self.translatedKeywords = []

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def peek(self):
        self.tok_idx_copy = self.tok_idx
        self.tok_idx_copy += 1
        if self.tok_idx_copy < len(self.tokens):
            self.current_tok_copy = self.tokens[self.tok_idx_copy]
        return self.current_tok_copy

    def __repr__(self):
        return f'{self.current_tok}\n'

    def translate_keywords(self):
            while self.current_tok != None:
                if self.current_tok == 'for':
                    self.translate_for_loop()
                    self.advance()
                elif self.current_tok == 'while':
                    self.translate_while_loop()
                    self.advance()
                elif self.current_tok == TT_EOF:
                    self.translatedKeywords.append(self.current_tok)
                    return self.translatedKeywords
                else:
                    self.translatedKeywords.append(self.current_tok)
                    self.advance()

    def translate_for_loop(self):
        identifier = ''
        start_pos = ''
        end_pos = ''
        increment = ''
        end_pos_identifier = ''
        range = identifier + 'in range(' + start_pos + ', ' + end_pos + ', ' + increment + ')'
        while self.current_tok != ':\n\t':
            if self.current_tok == '(':
                self.advance()
            elif self.current_tok == ')':
                self.advance()
            elif self.current_tok == '':
                self.advance()
            elif self.current_tok in KEYWORDS:
                self.translatedKeywords.append(self.current_tok)
                self.advance()
            elif self.current_tok == '=':
                self.peek()
                if type(self.current_tok_copy) == int:
                    start_pos = self.current_tok_copy
                self.advance()
            elif self.current_tok == '\n':
                self.advance()
            elif self.current_tok == '<':
                self.peek()
                if type(self.current_tok_copy) == int:
                    end_pos = self.current_tok_copy
                elif type(self.current_tok_copy) == str:
                    end_pos = self.current_tok_copy
                self.advance()
            elif self.current_tok == '<=':
                self.peek()
                if type(self.current_tok_copy) == int:
                    end_pos = self.current_tok_copy + 1
                elif type(self.current_tok_copy) == str:
                    end_pos = self.current_tok_copy + ' + 1'
                self.advance()
            elif self.current_tok == '>':
                self.peek()
                if type(self.current_tok_copy) == int:
                    end_pos = self.current_tok_copy
                elif type(self.current_tok_copy) == str:
                    end_pos = self.current_tok_copy
                self.advance()
            elif self.current_tok == '>=':
                self.peek()
                if type(self.current_tok_copy) == int:
                    end_pos = self.current_tok_copy - 1
                elif type(self.current_tok_copy) == str:
                    end_pos = self.current_tok_copy + ' - 1'
                self.advance()
            elif type(self.current_tok) == str:
                self.peek()
                if self.current_tok_copy == '=':
                    identifier = self.current_tok
                elif self.current_tok_copy == '+= 1':
                    increment = 1
                elif self.current_tok_copy == '-= 1':
                    increment = -1
                self.advance()
            elif type(self.current_tok) == int:
                self.advance()
            else:break
        range = identifier + ' in range(' + str(start_pos) + ', ' + str(end_pos) + ', ' + str(increment) + ')'
        self.translatedKeywords.append(range)
        self.translatedKeywords.append(self.current_tok)

    def translate_while_loop(self):
        while self.current_tok != ':\n\t':
            if self.current_tok == '(':
                self.advance()
            elif self.current_tok == ')':
                self.advance()
            elif self.current_tok == '':
                self.advance()
            elif self.current_tok == '<':
                self.translatedKeywords.append(self.current_tok)
                self.advance()
            elif self.current_tok in KEYWORDS:
                self.translatedKeywords.append(self.current_tok)
                self.advance()
            elif type(self.current_tok) == int:
                self.translatedKeywords.append(self.current_tok)
                self.advance()
            elif type(self.current_tok) == str:
                self.translatedKeywords.append(self.current_tok)
                self.advance()
            else:break
        self.translatedKeywords.append(self.current_tok)