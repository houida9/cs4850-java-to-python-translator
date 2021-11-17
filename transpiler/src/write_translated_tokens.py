from transpiler.src.scanner import *
from transpiler.src.translator import *
from transpiler.src.tokens import *
from pathlib import Path


#######################################
# Write to Python file
#######################################
class WriteTranslatedTokens:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.space_count = 0
        self.line_count = 1
        self.advance()
        self.result = []
        location = Path("../python_output/output.py").resolve()
        location.parent.mkdir(parents=True, exist_ok=True)  # required to create parentdir if it does
        # not exist
        self.file = open(location, "w+")

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
        return self.current_tok_copy

    def write_to_frontend(self):
        close_bracket_count = 0
        while self.current_tok != 'EOF':
            if self.current_tok == 'OPENBRACKET':
                self.result.append(':\n')
                self.space_count += 4
                self.line_count += 1
                self.advance()
            elif self.current_tok == 'NEWLINE':
                self.result.append('\n')
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
                self.result.append(str(self.write_space_count()))
                self.scan_line()
        return self.result

    def write_to_file(self):
        print("\nWriting to an output.py file...\n")
        self.write_to_frontend()
        for line in self.result:
            print(line)
            self.file.write(str(line))
        # close_bracket_count = 0
        # while self.current_tok != 'EOF':
        #     if self.current_tok == 'OPENBRACKET':
        #         self.file.write(':\n')
        #         self.space_count += 4
        #         self.line_count += 1
        #         self.advance()
        #     elif self.current_tok == 'NEWLINE':
        #         self.file.write('\n')
        #         self.line_count += 1
        #         self.advance()
        #     elif self.current_tok == 'CLOSEBRACKET':
        #         close_bracket_count += 1
        #         # if close_bracket_count == 1:
        #         #     self.advance()
        #         # else:
        #         self.space_count -= 4
        #         self.advance()
        #     elif self.current_tok == 'EOF':
        #         break
        #     else:
        #         self.file.write(str(self.write_space_count()))
        #         for line in self.scan_line():
        #             print(line)
        #             self.file.write("houida")
        #             self.file.write(line)
        self.file.close()

    def write_space_count(self):
        if self.space_count == 0:
            self.result.append('')
            return ''
        elif self.space_count == 4:
            self.result.append('\t')
            return ''
        elif self.space_count == 8:
            self.result.append('\t\t')
            return ''
        elif self.space_count == 12:
            self.result.append('\t\t\t')
            return ''
        elif self.space_count == 16:
            self.result.append('\t\t\t\t')
            return ''
        elif self.space_count == 20:
            self.result.append('\t\t\t\t\t')
            return ''
        else:
            return ''

    def scan_line(self):
        while self.current_tok != 'OPENBRACKET' and self.current_tok != 'NEWLINE':
            if self.current_tok == 'EOF':
                break
            elif self.current_tok != 'OPENBRACKET' and self.current_tok != 'NEWLINE':
                self.result.append(str(self.current_tok) + ' ')
                self.advance()
            else:
                break
