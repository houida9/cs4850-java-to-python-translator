#!/usr/bin/env python3   

import collections
import re
import sys
from pathlib import Path


source_file = Path("sample.java")  # change to file path

with open(source_file, 'r') as f:
    source = f.read()

Token = collections.namedtuple('Token', "token_type,value,line,offset")


def get_tokens(source, line=1):
    """Function to tokenize sequences of characters in input file. Spaces delimit
    lexemes and have been added to the token specifications. Each occurrence of
    a space cues an attempted pattern match for the next token.

    Keywords are placed inside a set data structure and are subsequently mapped
    to a lowercase version of themselves inside of the named tuple. Other tokens
    are explicitly mapped inside of a dictionary.
    """
    keywords = {
        'DOUBLE',
        'STRING',
        'SYSTEM.OUT.PRINT',
        'SYSTEM.OUT.PRINTLN',
        'ARGS',
        'MAIN',
        'ABSTRACT',
        'CONTINUE',
        'FOR',
        'NEW',
        'SWITCH',
        'ASSERT',
        'DEFAULT',
        'GOTO',
        'PACKAGE',
        'SYNCHRONIZED',
        'BOOLEAN',
        'DO',
        'IF',
        'PRIVATE',
        'THIS',
        'BREAK',
        'DOUBLE',
        'IMPLEMENTS',
        'PROTECTED',
        'THROW',
        'BYTE',
        'ELSE',
        'IMPORT',
        'PUBLIC',
        'THROWS',
        'CASE',
        'ENUM',
        'INSTANCEOF',
        'RETURN',
        'TRANSIENT',
        'CATCH',
        'EXTENDS',
        'INT',
        'SHORT',
        'TRY',
        'CHAR',
        'FINAL',
        'INTERFACE',
        'STATIC',
        'VOID',
        'CLASS',
        'FINALLY',
        'LONG',
        'STRICTFP',
        'VOLATILE',
        'CONST',
        'FLOAT',
        'NATIVE',
        'SUPER',
        'WHILE'
    }

    tok_mappings = {
        'ADD': r'\+(?!\d)',
        'ADDA': r'\+=',
        'BSLASH': r'\\',
        'BOR': r'\|',
        'BXOR': r'\^',
        'COLON': r':',
        'COMMA': r',',
        'COMMENT': r'//.*?(?=\n)|/\*(.|\n)*?\*/',
        'DECREMENT': r'--',
        'DIVA': r'/=',
        'DIVOP': r'/(?!/)',
        'DOT': r'\.',
        'EQOP': r'=',
        'EQUOP': r'==',
        'FLOAT': r'\d+\.\d+',
        'GT': r'>(?= \w)',
        'IDENTIFIER': r'[A-Za-z_][A-Za-z0-9_]*',
        'INCREMENT': r'\+\+',
        'INTEGER': r'\d+',
        'LANGB': r'<(?![ ])',
        'LCURB': r'{(?![ ])',
        'LB': r'\[',
        'LT': r'<(?= \w)',
        'LP': r'\(',
        'MINUS': r'-(?!\d)',
        'MINUSA': r'\-=',
        'MULTA': r'\*=',
        'NEGATE': r'-(?=\d)',
        'PLUS': r'\+(?=\d)',
        'QUOTES': r'(?P<quotes>"|\')(?!.*?(?P=quotes))',
        'RANGB': r'>(?![ ])',
        'RCURB': r'}(?![ ])',
        'RB': r'\]',
        'RP': r'\)',
        'RETURN': r'\n',
        'SCOLON': r';',
        'SPACE': r'[\t ]',
        'STRING': r'(?P<quote_type>"|\')[^"\'\n]*?(?P=quote_type)',
    }

    token_pattern = '|'.join((f'(?P<{group_name}>{match})' for group_name, match in tok_mappings.items()))
    # Uses compile's match method as a first-class object to turn 'next_token' into a callable
    next_token = re.compile(token_pattern).match
    pos = start = 0
    match_object = next_token(source)
    while match_object:
        # 're' Named Groups are preferred here to avoid dictionary key name lookups
        token_type = match_object.lastgroup

        if token_type == 'RETURN':
            start = pos
            line += 1
        elif token_type != 'SPACE':
            value = match_object.group(token_type)
            if token_type == 'IDENTIFIER' and value.upper() in keywords:
                token_type = value.upper()
            # 'start' represents offset start position for a new line and is reset on 'RETURN'.
            # Match_object's 'start' method returns beginning position of each pattern match in entire input.
            # Difference between the two signifies offset relative to each line.
            line_offset = match_object.start() - start
            yield Token(token_type, value, line, line_offset)
            if token_type == 'COMMENT' and (skips := match_object.group().count('\n')):
                start = pos
                line += skips
        # moves pattern match position to start of next token
        pos = match_object.end()
        match_object = next_token(source, pos)

    # Final position should equal the length of the line if entire character sequence was consumed.
    # Otherwise, an unrecognized pattern was identified. Raise runtime error and exit.
    if pos != len(source):
        error_pos = pos - start
        raise RuntimeError(f'The character {source[pos]} caused a lexical error on line {line}, '
                           f'character {error_pos}.')


for token in get_tokens(source):
    print(token)
