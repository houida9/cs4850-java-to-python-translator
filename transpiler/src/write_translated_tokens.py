from transpiler.src.scanner import *
from transpiler.src.translator import *
from transpiler.src.tokens import *
from pathlib import Path


class WriteTranslatedTokens:
    def __init__(self, tokens, file_path):
        self.tokens = tokens
        self.tok_idx = -1
        self.space_count = 0
        self.line_count = 1
        self.advance()
        self.spaceTracker = ''
        self.f = open(file_path, "w+")

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
        close_bracket_count = 0
        while self.current_tok != 'EOF':
            if self.current_tok == 'OPENBRACKET':
                self.f.write(':\n')
                self.space_count += 4
                self.line_count += 1
                self.advance()
            elif self.current_tok == 'NEWLINE':
                self.f.write('\n')
                self.line_count += 1
                self.advance()
            elif self.current_tok == 'CLOSEBRACKET':
                close_bracket_count += 1
                # if close_bracket_count == 1:
                #     self.advance()
                # else:
                self.space_count -= 4
                self.advance()
            elif self.current_tok == 'EOF':
                break
            else:
                # if self.current_tok == 'class':
                #     self.space_count = 0
                self.f.write(str(self.write_space_count()))
                self.scan_line()
        self.f.close()

    def write_space_count(self):
        if self.space_count < 0:
            self.space_count = 0
            self.f.write('')
            self.spaceTracker = ''
            return ''
        elif self.space_count == 0:
            self.f.write('')
            self.spaceTracker = ''
            return ''
        elif self.space_count == 4:
            self.f.write('    ')
            self.spaceTracker = '    '
            return ''
        elif self.space_count == 8:
            self.f.write('        ')
            self.spaceTracker = '        '
            return ''
        elif self.space_count == 12:
            self.f.write('            ')
            self.spaceTracker = '            '
            return ''
        elif self.space_count == 16:
            self.f.write('                ')
            self.spaceTracker = '                '
            return ''
        elif self.space_count == 20:
            self.f.write('                    ')
            self.spaceTracker = '                    '
            return ''
        else: return ''

    def scan_line(self):
        while self.current_tok != 'OPENBRACKET' and self.current_tok != 'NEWLINE':
            if self.current_tok == 'EOF':
                break
            elif self.current_tok == '= None\n':
                self.f.write(str(self.current_tok) + '\n')
                self.f.write(self.spaceTracker)
                self.advance()
            elif self.current_tok != 'OPENBRACKET' and self.current_tok != 'NEWLINE':
                self.f.write(str(self.current_tok) + ' ')
                self.advance()
            else: break
