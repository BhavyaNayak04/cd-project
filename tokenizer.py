# tokenizer.py
import re

def tokenize(pseudocode):
    token_specification = [
        ('procedure', r'[Pp]rocedure'),
        ('if', r'[Ii]f'),
        ('then', r'then'),
        ('elsif', r'[Ee]lsif'),
        ('else', r'else'),
        ('end', r'end'),
        ('integer', r'integer'),
        ('printf', r'printf'),
        ('and', r'and'),
        ('ASSIGN', r':='),
        ('COLON', r':'),
        ('SEMI', r';'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('EQ', r'='), 
        ('id', r'[a-zA-Z_][a-zA-Z_0-9]*'),
        ('num', r'\d+'),
        ('str', r'"[^"]*"'),
        ('WHITESPACE', r'[ \t\n]+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    tokens = []
    lexems = {}

    for mo in re.finditer(tok_regex, pseudocode):
        token_type = mo.lastgroup
        value = mo.group()
        if token_type != 'WHITESPACE':
            tokens.append(token_type)
            lexems[len(tokens) - 1] = value

    return tokens, lexems
