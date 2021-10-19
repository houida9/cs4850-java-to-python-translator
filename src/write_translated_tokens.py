from scanner import *
from translator import *
from tokens import *

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