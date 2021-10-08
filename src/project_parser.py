from scanner import *


#######################################
# NODES
#######################################
class NumberNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

class BinaryOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class KeywordNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

class IfThenNode:
    def __init__(self, node, statement ):
        self.node = node 
        self.statement = statement

    def _repr__(self):
        return f'({self.node},{self.statement}) '

class IdentifierNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

#######################################
# PARSER
#######################################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
         res = self.expr()
         if not res.error and self.current_tok.type != TT_EOF:
             return res.failure(InvalidSyntaxError(
                 self.current_tok.pos_start, self.current_tok.pos_end,
                 f'Expected "+", "-", "*", or "/". Got {self.current_tok}'
                 
             ))
         return res
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        #print(self.current_tok)

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())

            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            
            if res.error: 
                return res
            
            res.register(self.advance())
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                if (self.current_tok == TT_NEWLINE):
                    return res.register(self.factor())
                return res.success(self.current_tok)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected ")"'
                ))
#############################################
# This Could Probably be combined into another method to clean this up
#############################################
        elif tok.type == TT_KEYWORD:
            res.register(self.advance())
            return res.register(self.factor())
        
        elif tok.type == TT_IDENTIFIER:
            res.register(self.advance())

            #Process op tokens on identifiers 
            if self.current_tok.type in (TT_PLUS, TT_MINUS, TT_DIV, TT_MUL):
                res.register(self.advance())
                return (res.success(self.current_tok))

            #Process []
            if self.current_tok.type == TT_LARRAY:
                res.register(self.advance())

                if self.current_tok.type == TT_RARRAY:
                    res.register(self.advance())
                    return res.success(self.factor())

            #Process ()
            if self.current_tok.type == TT_LPAREN:
                res.register(self.advance())
                expr = res.register(self.expr())

                if res.error:
                    return res
                
                if self.current_tok.type == TT_RPAREN:
                    res.register(self.advance())

            #Process {, =, and ; 
            if self.current_tok.type == TT_OPENBRACKET:
                res.register(self.advance())
                expr = res.register(self.expr())
    
                if self.current_tok.type == TT_CLOSEBRACKET:
                    res.register(self.advance())
                    return res.success(expr)

            if self.current_tok.type == TT_NEWLINE:
                res.register(self.advance())
                res.register(self.factor())

            if self.current_tok.type == TT_EQ:
                res.register(self.advance())
                factor = res.register(self.factor())
                if res.error:
                    return res

#Need a method that only handles KEYWORDS and another for IDENTIFIERS
#This way we can somehow keep track of what a variable is assigned as or to and make sure 
# that variables are being utilized correctly. 

                #Handle Same-Line Initilization
            if self.current_tok.type == TT_COMMA: 
                res.register(self.advance())
                id = res.register(self.factor())
                if res.error: return res
                return res.success(self.factor())
            
            
            else:
                res.register(self.factor())
                if res.error: return res
 
        elif tok.type == TT_CLOSEBRACKET:
            return res.register(self.advance())
                
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end,
         f"Expected Int or Float. Got {tok}"))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinaryOpNode(left, op_tok, right) 
        return res.success(left)

#######################################
#PARSE RESULT
#######################################
class ParseResult: 
    def __init__ (self):
        self.error = None
        self.node = None
    
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: 
                self.error = res.error
            return res.node
        
        return res

    def success(self, node):
        self.node = node
        return self

    def failure (self, error):
        self.error = error
        return self

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error: return "None, error"

    #Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
