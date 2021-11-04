from .scanner import *
from .translator import *
from .tokens import *

#######################################
# Write to Python file
#######################################
class write_tranlsated_tokens:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.space_count = 0
        self.line_count = 1
        self.advance()
        self.f = open("C:/Users/hreec/PycharmProjects/Java-to_python_backend/python_output/output.py", "w+")

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
        print("\nWriting to an output.py file...\n")
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
                self.f.write(str(self.write_space_count()))
                self.scan_line()
        self.f.close()

    def write_space_count(self):
        if self.space_count == 0:
            self.f.write('')
            return ''
        elif self.space_count == 4:
            self.f.write('\t')
            return ''
        elif self.space_count == 8:
            self.f.write('\t\t')
            return ''
        elif self.space_count == 12:
            self.f.write('\t\t\t')
            return ''
        elif self.space_count == 16:
            self.f.write('\t\t\t\t')
            return ''
        elif self.space_count == 20:
            self.f.write('\t\t\t\t\t')
            return ''
        else: return ''

    def scan_line(self):
        while self.current_tok != 'OPENBRACKET' and self.current_tok != 'NEWLINE':
            if self.current_tok == 'EOF':
                break
            elif self.current_tok != 'OPENBRACKET' and self.current_tok != 'NEWLINE':
                self.f.write(str(self.current_tok) + ' ')
                self.advance()
            else: break

