#######################################
# CONSTANTS
#######################################
import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
WEIRD_LETTERS = LETTERS + DIGITS + '.' + '_' + ' ' + '"' + ":" + ";" + ','


#######################################
# ERRORS
#######################################
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

#######################################
# POSITION###########

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx +=1
        self.col += 1
        if current_char =='\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return  Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
#######################################
# TOKENS
#######################################

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
TT_EE			= 'EE' #
TT_NE		    = 'NE' #
TT_LT		    = 'LT' #
TT_GT			= 'GT' #
TT_LTE			= 'LTE' #
TT_GTE			= 'GTE' #
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

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        self.current_char_copy = None

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def peek(self):
        self.current_char_copy = self.current_char
        self.pos.advance(self.current_char_copy)
        self.current_char_copy = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
                if self.current_char == '\n':
                    self.advance()
            elif self.current_char == '\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_print_statement())
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                self.peek()
                if self.current_char_copy == '+':
                    tokens.append(Token(TT_PLUSPLUS, pos_start=self.pos))
                else: tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                self.peek()
                if self.current_char_copy == '-':
                    tokens.append(Token(TT_MINUSMINUS, pos_start=self.pos))
                else: tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '{':
                tokens.append(Token(TT_OPENBRACKET, pos_start=self.pos))
                self.advance()
                if self.current_char == '\n':
                    self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_CLOSEBRACKET, pos_start=self.pos))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LARRAY, pos_start=self.pos))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RARRAY, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '.' + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_print_statement(self):
        id_str = ''
        pos_start = self.pos.copy()
        quoteCount = 0

        while self.current_char != None and self.current_char in WEIRD_LETTERS:
            id_str += self.current_char
            if self.current_char == '"':
                quoteCount += 1
                if quoteCount == 2:
                    break
            self.advance()

        tok_type = TT_STRING
        return Token(tok_type, id_str, pos_start, self.pos)

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
                    self.translatedToken.append('++')
                    self.advance()
                elif self.current_tok.type == TT_MINUSMINUS:
                    self.translatedToken.append('--')
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
                self.advance()
            elif type(self.current_tok) == str:
                self.peek()
                if self.current_tok_copy == '=':
                    identifier = self.current_tok
                elif self.current_tok_copy == '++':
                    increment = 1
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



#######################################
# Write to Python file
#######################################
class write_tranlsated_tokens:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def peek(self):
        self.tok_idx_copy = self.tok_idx
        self.tok_idx_copy += 1
        self.current_tok_copy = self.current_tok
        if self.tok_idx_copy < len(self.tokens):
            self.current_tok_copy = self.tokens[self.tok_idx_copy]
        return  self.current_tok_copy

    def write_to_file(self):
        f = open("C:\cs4850-java-to-python-translator\output_python/output.py", "a")

        while self.current_tok != 'EOF':
            f.write(str(self.current_tok) + ' ')
            self.advance()

        f.close()


#######################################
# RUN
#######################################

def run(fn, text):
    #Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    #Generate AST
    # parser = Parser(tokens)
    # ast = parser.parse()

    #Translate
    translator = Translator(tokens)
    result = translator.translate()
    keywords = Translate_Keywords(result)
    final = keywords.translate_keywords()
    write = write_tranlsated_tokens(final)
    working = write.write_to_file()

    return final, None