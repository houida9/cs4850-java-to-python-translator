from transpiler.src.scanner import *
from transpiler.src.tokens import *

#######################################
# Translator & Deleted keywords
#######################################
IDS = [
    TT_IDENTIFIER,
    TT_INT,
    TT_FLOAT,
    TT_STRING
]
OPS = [
    TT_PLUS,
    TT_MUL,
    TT_MINUS,
    TT_DIV
]
SCANNER = [
    '.nextLine',
    '.nextFloat',
    '.nextInt'
]
METHOD = [
    "double",
    'int',
    'boolean',
    'float',
    'void',
    'String',
    'char'
]
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
    'Scanner'
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
                elif self.current_tok.type == TT_PLUSEQ:
                    self.translatedToken.append('+=')
                    self.advance()
                elif self.current_tok.value == 'public':
                    self.peek(1)
                    if self.current_tok_copy.value == 'static' or self.current_tok_copy.value == 'void':
                        self.peek(2)
                        if self.current_tok_copy.value in METHOD:
                            self.peek(3)
                            if self.current_tok_copy.value == 'main':
                                self.advance()
                            else : self.make_method()
                        elif self.current_tok_copy.type == TT_IDENTIFIER:
                            self.peek(3)
                            if self.current_tok_copy.type == TT_LPAREN:
                                self.make_method()
                    elif self.current_tok_copy.value in METHOD:
                        self.peek(2)
                        if self.current_tok_copy.type == TT_IDENTIFIER:
                            self.make_method()
                    else: self.advance()
                elif self.current_tok.value == 'static':
                    self.peek(1)
                    if self.current_tok_copy.value in METHOD:
                        if self.current_tok_copy.value == 'void':
                            self.peek(2)
                            if self.current_tok_copy.type == TT_IDENTIFIER and self.current_tok_copy.value != 'main':
                                self.make_method()
                            elif self.current_tok_copy.value == 'main':
                                while self.current_tok.type != TT_OPENBRACKET:
                                    self.advance()
                                self.advance()
                        elif self.current_tok_copy.value in METHOD:
                            self.peek(2)
                            if self.current_tok_copy.type == TT_IDENTIFIER:
                                self.make_method()
                            else: self.advance()
                    else: self.advance()
                elif self.current_tok.value == 'void':
                    self.peek(1)
                    if self.current_tok_copy.type == TT_IDENTIFIER and self.current_tok_copy.value != 'main':
                        self.make_method()
                    elif self.current_tok_copy.value == 'main':
                        while self.current_tok.type != TT_OPENBRACKET:
                            self.advance()
                        self.advance()
                    else: self.advance()
                elif self.current_tok.value in METHOD:
                    self.peek(1)
                    if self.current_tok_copy.type == TT_IDENTIFIER:
                        self.peek(2)
                        if self.current_tok_copy.type == TT_LPAREN:
                            self.make_method()
                        elif self.current_tok_copy.type == TT_EQ:
                            self.advance()
                        elif self.current_tok_copy.type == TT_NEWLINE:
                            self.advance()
                            self.translatedToken.append(self.current_tok.value)
                            self.translatedToken.append('= None')
                            self.advance()
                        elif self.current_tok_copy.type == TT_COMMA:
                            while(self.current_tok.type != 'NEWLINE'):
                                if self.current_tok.value in METHOD:
                                    self.advance()
                                elif self.current_tok.type == TT_IDENTIFIER:
                                    self.peek(1)
                                    if self.current_tok_copy.type == TT_COMMA:
                                        self.translatedToken.append(self.current_tok.value)
                                        self.translatedToken.append('= None\n')
                                        self.advance()
                                    elif self.current_tok_copy.type == 'NEWLINE':
                                        self.translatedToken.append(self.current_tok.value)
                                        self.translatedToken.append('= None\n')
                                        self.advance()
                                    else: self.advance()
                                else: self.advance()
                        else: self.advance()
                elif self.current_tok.type == TT_MINUS:
                    self.translatedToken.append('-')
                    self.advance()
                elif self.current_tok.type == TT_COMMENT:
                    self.translatedToken.append('#' + self.current_tok.value)
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
                    self.translatedToken.append('NEWLINE')
                    self.advance()
                elif self.current_tok.value == 'System.out.print' or self.current_tok.value == 'System.out.println':
                    self.check_print()
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
                    if self.current_tok.value == 'Scanner':
                        self.delete_Scanner()
                    else: self.advance()
                elif self.current_tok.value == 'else':
                    self.peek(1)
                    if self.current_tok_copy.value == 'if':
                        self.translatedToken.append('elif')
                        self.advance()
                        self.advance()
                    else:
                        self.translatedToken.append('else')
                        self.advance()
                elif self.current_tok.type == TT_IDENTIFIER:
                    self.peek(1)
                    if self.current_tok_copy.type == TT_LPAREN:
                        self.peek(2)
                        if self.current_tok_copy.type == TT_RPAREN:
                            self.translatedToken.append(self.current_tok.value)
                            self.translatedToken.append('(')
                            self.translatedToken.append(')')
                            self.advance()
                            self.advance()
                            self.advance()
                        else:
                            self.translatedToken.append(self.current_tok.value)
                            self.advance()
                    elif self.current_tok.value == 'true':
                        self.translatedToken.append("True")
                        self.advance()
                    elif self.current_tok.value == 'false':
                        self.translatedToken.append("False")
                        self.advance()
                    else:
                        self.translatedToken.append(self.current_tok.value)
                        self.advance()
                elif self.current_tok.value in KEYWORDS:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
                elif self.current_tok.type == TT_OPENBRACKET:
                    self.translatedToken.append('OPENBRACKET')
                    self.advance()
                elif self.current_tok.type == TT_CLOSEBRACKET:
                    self.translatedToken.append('CLOSEBRACKET')
                    self.advance()
                elif self.current_tok.type == TT_LPAREN:
                    self.peek(1)
                    if self.current_tok_copy.type == TT_RPAREN:
                        self.advance()
                        self.advance()
                    else:
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
                elif self.current_tok.type == TT_QUOTE:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
                elif self.current_tok.type == TT_MUL:
                    self.translatedToken.append('*')
                    self.advance()
                elif self.current_tok.type == TT_NOTEQ:
                    self.translatedToken.append('!=')
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
                elif self.current_tok.type == TT_EE:
                    self.translatedToken.append('==')
                    self.advance()
                elif self.current_tok.type == TT_METHOD:
                    self.translatedToken.append(self.current_tok.value)
                    self.peek(1)
                    if self.current_tok_copy.type == TT_LPAREN:
                        self.translatedToken.append('(')
                        self.advance()
                        self.advance()
                    else: self.advance()
                else:
                    self.translatedToken.append('EOF')
                    return self.translatedToken

    def check_print(self):
        incrementer = 1
        newlineCount = 0
        inputString = ''
        inputIndicator = False
        typeCast = ''
        self.peek(incrementer)

        #check for scanner
        while newlineCount != 2:
            if self.current_tok_copy.type == TT_METHOD:
                if self.current_tok_copy.value in SCANNER:
                    inputIndicator = True
                    if self.current_tok_copy.value == '.nextFloat':
                        typeCast = 'float'
                    elif self.current_tok_copy.value == '.nextLine':
                        typeCast = ''
                    elif self.current_tok_copy.value == '.nextInt':
                        typeCast = 'int'
                    else:
                        typeCast = ''
                    break
                else:
                    incrementer += 1
                    self.peek(incrementer)
            elif self.current_tok_copy.type == TT_NEWLINE:
                newlineCount += 1
                incrementer += 1
                self.peek(incrementer)
            elif self.current_tok_copy.type == TT_EOF:
                break
            else:
                incrementer += 1
                self.peek(incrementer)

        incrementer = 1
        newlineCount = 0
        ID_count = 0
        identifier = ''
        self.peek(incrementer)
        if inputIndicator == True:
            while newlineCount != 2:
                if self.current_tok.type == TT_NEWLINE:
                    newlineCount += 1
                    incrementer += 1
                    self.advance()
                elif self.current_tok.type == TT_STRING:
                    inputString = self.current_tok.value
                    incrementer += 1
                    self.advance()
                elif self.current_tok.type == TT_IDENTIFIER:
                    if ID_count == 0:
                        identifier = self.current_tok.value
                        ID_count = 1
                        incrementer += 1
                        self.advance()
                    else:
                        incrementer += 1
                        self.advance()
                else:
                    incrementer += 1
                    self.advance()
            if typeCast != '':
                append = identifier + ' = ' + typeCast +'(input(' + inputString + '))'
                self.translatedToken.append(append)
                self.translatedToken.append('NEWLINE')
            else:
                append = identifier + ' = input(' + inputString + ')'
                self.translatedToken.append(append)
                self.translatedToken.append('NEWLINE')


        else:
            self.translatedToken.append('NEWLINE')
            self.make_print()

    def delete_Scanner(self):
        while self.current_tok.type != TT_NEWLINE:
            self.advance()

    def make_print(self):
        lparenCount = 0
        while self.current_tok.type != TT_NEWLINE:
            if self.current_tok.value == 'System.out.print' or self.current_tok.value == 'System.out.println':
                self.translatedToken.append('print')
                self.advance()
            elif self.current_tok.type == TT_PLUS:
                self.translatedToken.append(',')
                self.advance()
            elif self.current_tok.type == TT_LPAREN:
                lparenCount += 1
                if (lparenCount == 1):
                    self.translatedToken.append('(')
                    self.advance()
                else: self.make_string_method()
            elif self.current_tok.type == TT_RPAREN:
                self.translatedToken.append(')')
                self.advance()
            else:
                self.translatedToken.append(self.current_tok.value)
                self.advance()

    def make_string_method(self):
        while self.current_tok.type != TT_RPAREN:
            if self.current_tok.type == TT_LPAREN:
                self.translatedToken.append('(')
                self.advance()
            elif self.current_tok.type in IDS:
                self.peek(1)
                if self.current_tok_copy.type in OPS:
                    self.peek(2)
                    if self.current_tok_copy.type in IDS:
                        self.translatedToken.append(self.current_tok.value)
                        self.advance()
                        if self.current_tok.type == TT_PLUS:
                            self.translatedToken.append('+')
                            self.advance()
                        elif self.current_tok.type == TT_MINUS:
                            self.translatedToken.append('-')
                            self.advance()
                        elif self.current_tok.type == TT_MUL:
                            self.translatedToken.append('*')
                            self.advance()
                        elif self.current_tok.type == TT_DIV:
                            self.translatedToken.append('/')
                            self.advance()
                        else: continue
                        self.translatedToken.append(self.current_tok.value)
                        self.advance()
                else:
                    self.translatedToken.append(self.current_tok.value)
                    self.advance()
            else:
                self.translatedToken.append(self.current_tok.value)
                self.advance()

    def make_method(self):
        identifier = ''
        while self.current_tok != None:
            if self.current_tok.value in DELETE:
                self.advance()
            elif self.current_tok.value in KEYWORDS:
                self.translatedToken.append(self.current_tok.value)
                self.advance()
            elif self.current_tok.type == TT_IDENTIFIER:
                identifier = self.current_tok.value
                self.peek(1)
                if self.current_tok_copy.type == TT_LPAREN:
                    self.advance()
                    break
        self.translatedToken.append('def ' + identifier)

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
        self.peek()
        identifier = ''
        start_pos = ''
        end_pos = ''
        increment = ''
        end_pos_identifier = ''
        range = identifier + 'in range(' + start_pos + ', ' + end_pos + ', ' + increment + ')'
        while self.current_tok != 'OPENBRACKET':
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
            elif self.current_tok == 'NEWLINE':
                self.advance()
            elif self.current_tok == '+=':
                increment = 1
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
            elif self.current_tok == '+= 1':
                increment = 1
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
        self.peek()

    def translate_while_loop(self):
        while self.current_tok != 'OPENBRACKET':
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
