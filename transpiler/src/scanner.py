from transpiler.src.translator import *
from transpiler.src.tokens import *
from transpiler.src.write_translated_tokens import *

#######################################
# CONSTANTS
#######################################
import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
WEIRD_LETTERS = LETTERS + DIGITS + '.' + '_' + ' ' + '"' + ":" + ";" + ',' + '!' + '\\'


#######################################
# ERRORS
#######################################
class Error(Exception):
    def __init__(self, errno, pos_start, pos_end, error_name, details):
        self.args = (errno, details)
        self.errno = errno
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, errno, pos_start, pos_end, details):
        super().__init__(errno, pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    def __init__(self, errno, pos_start, pos_end, details):
        super().__init__(errno, pos_start, pos_end, 'Expected Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, errno, pos_start, pos_end, details):
        super().__init__(errno, pos_start, pos_end, "Invalid Syntax", details)


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
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text.replace('\r', '')
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
                tokens.append(Token(TT_NEWLINE))
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
                elif self.current_char_copy == '=':
                    tokens.append(Token(TT_PLUSEQ, pos_start=self.pos))
                else:
                    tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                self.peek()
                if self.current_char_copy == '-':
                    tokens.append(Token(TT_MINUSMINUS, pos_start=self.pos))
                elif self.current_char_copy == '=':
                    tokens.append(Token(TT_MINUSEQ, pos_start=self.pos))
                else:
                    tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                self.peek()
                if self.current_char_copy == '=':
                    tokens.append(Token(TT_MULEQ, pos_start=self.pos))
                else:
                    tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                self.peek()
                if self.current_char_copy in ('/*'):
                    tokens.append(self.handle_comments())
                elif self.current_char_copy == '=':
                    tokens.append(Token(TT_DIVEQ, pos_start=self.pos))
                else:
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
                token = self.make_not_equals()
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
                raise IllegalCharError(1, pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens

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
        id_str_copy = ''
        method_indicator = False
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '.' + '_':
            id_str += self.current_char
            self.advance()

        if id_str == 'java.util.Scanner':
            tok_type = TT_IDENTIFIER
            return Token(tok_type, id_str, pos_start, self.pos)
        if id_str in KEYWORDS:
            tok_type = TT_KEYWORD
            return Token(tok_type, id_str, pos_start, self.pos)

        else: #Check for Method call
            for element in range(0, len(id_str)):
                if id_str[element] == '.':
                    self.tokens.append(Token(TT_IDENTIFIER, id_str_copy, pos_start, self.pos))
                    id_str_copy = ''
                    id_str_copy += '.'
                    method_indicator = True
                else:
                    id_str_copy += id_str[element]

        if method_indicator == False:
            tok_type = TT_KEYWORD if id_str_copy in KEYWORDS else TT_IDENTIFIER
            return Token(tok_type, id_str_copy, pos_start, self.pos)
        else:
            tok_type = TT_KEYWORD if id_str_copy in KEYWORDS else TT_METHOD
            return Token(tok_type, id_str_copy, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos)

        self.advance()
        raise ExpectedCharError(2, pos_start, self.pos, "'=' (after '!')")

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

    def handle_comments(self):
        # handle /* */ comments
        comment = ""
        pos_start = self.pos.copy()

        if self.current_char == '/' and self.current_char_copy == '*':
            self.advance()
            while self.current_char != None and not (self.current_char == '*' and self.current_char_copy == '/'):
                comment += self.current_char
                self.advance()
                if (self.current_char == "*"):
                    self.peek()
            self.advance()

        # handle // comments
        elif self.current_char == '/' and self.current_char_copy == "/":
            self.advance()
            while self.current_char != None and self.current_char != '\n':
                comment += self.current_char
                self.advance()

        return Token(TT_COMMENT, comment, pos_start, self.pos)


#######################################
# RUN
#######################################

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens = lexer.make_tokens()

    # Generate AST
    # parser = Parser(tokens)
    # ast = parser.parse()

    # Translate
    translator = Translator(tokens)
    result = translator.translate()
    keywords = Translate_Keywords(result)
    final = keywords.translate_keywords()

    write_file = WriteTranslatedTokens(final)
    write_file.write_to_file()

    write_frontend = WriteTranslatedTokens(final)
    working = write_frontend.write_to_frontend()

    return working
