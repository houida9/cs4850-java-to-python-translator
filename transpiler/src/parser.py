from transpiler.src.scanner import *

basicTypes = [
    "int",
    "double",
    "float"
]

ops = [
    TT_EQ,
    TT_LT,
    TT_GT,
    TT_DIV,
    TT_MUL,
    TT_MINUS,
    TT_MINUS

]


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


class IdentifierNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class BracketNode:
    def __init__(self, opn, body, close):
        self.open = opn
        self.body = body
        self.close = close

    def __repr__(self):
        return f'({self.open}, {self.body}, {self.close})'


class NewLineNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class InitilizationNode:
    def __init__(self, basicType, tok, op_tok, eqTo):
        self.basicType = basicType
        self.tok = tok
        self.op_tok = op_tok
        self.eqTo = eqTo

    def __repr__(self):
        return f'({self.basicType}, {self.tok}, {self.op_tok}, {self.eqTo})'


class KeywordNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class StringNode:
    def __init__(self, lquote, tok, rquote):
        self.lquote = lquote
        self.tok = tok
        self.rquote = rquote

    def __repr__(self):
        return f'({self.lquote}, {self.tok}, {self.rquote})'


class ObjectNode:
    def __init__(self, className, lparen, param, rparen):
        self.className = className
        self.lparen = lparen
        self.param = param
        self.rparen = rparen

    def __repr__(self):
        return f'({self.className}, {self.lparen}, {self.param}, {self.rparen})'


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

    def peek(self, peek_idx):
        self.tok_idx_copy = self.tok_idx
        self.tok_idx_copy += peek_idx
        if self.tok_idx_copy < len(self.tokens):
            self.current_tok_copy = self.tokens[self.tok_idx_copy]
        return self.current_tok_copy

    def parse(self):
        # res = self.expr()
        res = self.java_prog()
        #  if not res.error and self.current_tok.type != TT_EOF:
        #    return res.failure(InvalidSyntaxError(
        #       self.current_tok.pos_start, self.current_tok.pos_end,
        #      'Expected "+", "-", "*", or "/". Token Returned: {} '.format(self.current_tok)
        #  ))
        return res

    ####################
    # MATH 
    ####################
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

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

            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    3, self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected ")"'
                ))

        return res.failure(InvalidSyntaxError(3, tok.pos_start, tok.pos_end,
                                              "Expected Int or Float"))

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

    ################
    # Identifiers and Keywords
    ################
    def paren(self):
        res = ParseResult()
        binaryOp = []
        if self.current_tok.type == TT_LPAREN:
            binaryOp.append(self.current_tok)
            res.register(self.advance())

            while self.current_tok.type != TT_RPAREN:
                binaryOp.append(self.current_tok)
                res.register(self.advance())

                if self.current_tok.type == TT_EOF:
                    return res.error(InvalidSyntaxError(3, self.current_tok.pos_start, self.current_tok.pos_end,
                                                        ' Expected )'))

        binaryOp.append(self.current_tok)
        res.register(self.advance())
        return binaryOp

    def initilize(self, basicType):
        res = ParseResult()
        nodes = []
        while self.current_tok.type != TT_NEWLINE:
            op = TT_EQ
            eqTo = None
            # iden = None
            binaryOp = []
            binary = False

            if self.current_tok.type == TT_IDENTIFIER:
                peek = self.peek(1)
                if peek.type == TT_LPAREN:
                    binary = True
                    className = self.current_tok
                    res.register(self.advance())
                    values = self.paren()
                    binaryOp.append(ObjectNode(className, values[0], values[1], values[2]))
                else:
                    print("NOT CAUGHT")
                    iden = self.current_tok
                    res.register(self.advance())

            if self.current_tok.type == TT_EQ:
                res.register(self.advance())
                if self.current_tok.type == TT_LPAREN:
                    binary = True
                    binaryOp = self.paren()
                else:
                    eqTo = self.current_tok
                    binaryOp.append(eqTo)
                    res.register(self.advance())

                while self.current_tok.type in (TT_PLUS, TT_MINUS, TT_MUL, TT_DIV):
                    binary = True
                    binaryOp.append(self.current_tok)
                    res.register(self.advance())
                    binaryOp.append(self.current_tok)
                    res.register(self.advance())

            if self.current_tok.type == TT_LPAREN:
                binary = True
                values = self.paren()
                binaryOp.append(values)

            if binary: eqTo = binaryOp
            node = InitilizationNode(basicType, iden, op, eqTo)
            nodes.append(node)
            # Handle same line declarations
            if self.current_tok.type == TT_COMMA:
                res.register(self.advance())

            if self.current_tok.type == TT_EOF:
                return res.error(InvalidSyntaxError(3, self.current_tok.pos_start, self.current_tok.pos_end,
                                                    'Not a statement. ; Expected.'))

        return nodes

    def read_program(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type == TT_KEYWORD:
            # initialize variables
            if tok.value in ('int', 'double', 'float', 'String', 'boolean'):
                basicType = tok.value
                res.register(self.advance())
                values = self.initilize(basicType)
                res.register(self.advance())
                return res.success(values)
            else:
                res.register(self.advance())
                return res.success(KeywordNode(tok))

        elif tok.type == TT_IDENTIFIER:
            peek = self.peek(1)
            if peek.type == TT_EQ:
                values = self.initilize('int')
                res.register(self.advance())
                return res.success(values)
            if peek.type == TT_PLUS:
                op = []
                id1 = IdentifierNode(tok)
                op.append(id1)
                res.register(self.advance())
                op.append(self.current_tok)
                res.register(self.advance())
                id2 = IdentifierNode(self.current_tok)
                op.append(id2)
                res.register(self.advance())
                return res.success(op)
            else:
                res.register(self.advance())
                return res.success(IdentifierNode(tok))

        elif tok.type in TT_OPENBRACKET:
            opn = tok
            body = []
            res.register(self.advance())
            while self.current_tok.type != TT_CLOSEBRACKET:
                body.append(res.register(self.read_program()))

                if self.current_tok.type == TT_EOF:
                    return res.failure(InvalidSyntaxError(3, self.current_tok.pos_start, self.current_tok.pos_end,
                                                          "Expected }"))

            close = self.current_tok
            res.register(self.advance())
            return res.success(BracketNode(opn, body, close))

        elif tok.type == TT_LPAREN:
            opn = tok
            res.register(self.advance())

            body = []
            while self.current_tok.type != TT_RPAREN:
                body.append(res.register(self.read_program()))

                if self.current_tok.type == TT_EOF:
                    return res.failure(InvalidSyntaxError(3, self.current_tok.pos_start, self.current_tok.pos_end,
                                                          "Expected )"))

            close = self.current_tok
            res.register(self.advance())
            return res.success(BracketNode(opn, body, close))

        elif tok.type == TT_LARRAY:
            opn = tok
            res.register(self.advance())
            body = []

            while self.current_tok.type != TT_RARRAY:
                body.append(res.register(self.read_program()))

                if self.current_tok.type == TT_EOF:
                    return res.failure(InvalidSyntaxError(3, self.current_tok.pos_start, self.current_tok.pos_end,
                                                          "Expected )"))

            close = self.current_tok
            res.register(self.advance())
            return res.success(BracketNode(opn, body, close))

        elif tok.value == '"':
            lquote = tok
            res.register(self.advance())
            words = []
            while self.current_tok.value != '"':
                words.append(self.current_tok)
                res.register(self.advance())

                if self.current_tok.type == TT_EOF:
                    return res.failure(InvalidSyntaxError(3, self.current_tok.pos_start, self.current_tok.pos_end,
                                                          'Expected "'))

            rquote = self.current_tok
            res.register(self.advance())
            return res.success(StringNode(lquote, words, rquote))

        elif tok.type == TT_NEWLINE:
            res.register(self.advance())
            return res.success(NewLineNode(tok))

        # Implement some type of error handling here
        else:
            print(self.current_tok, tok)
            return None
            # return res.failure(InvalidSyntaxError(3, tok.pos_start, tok.pos_end,
            # 'Expected something here but got {}'.format(tok)))

    def java_prog(self):
        nodes = []
        while self.current_tok != None and self.current_tok.type != TT_EOF:
            res = self.read_program()
            if res.error: return res
            nodes.append(res)

        return nodes

    #######################################


# PARSE RESULT
#######################################
class ParseResult:
    def __init__(self):
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

    def failure(self, error):
        self.error = error
        return self


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens = lexer.make_tokens()

    # Generate AST
    parser = Parser(tokens)
    values = []
    while parser.current_tok != None and parser.current_tok.type != TT_EOF:
        res = parser.read_program()
        if res.error:
            print(res.error.as_string())
            values = []
            break
        values.append(res)

    # get nodes
    nodes = []
    for value in values:
        nodes.append(value.node)

    return nodes, None
