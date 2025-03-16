import re

# List of keywords
KEYWORDS = {"Procedure", "if", "elseif", "else", "end", "printf", "scanf", "integer"}

# Define token types
TOKEN_SPEC = [
    ('ASSIGN', r':='),
    ('EQUAL', r'='),
    ('AND', r'and'),
    ('SEMICOLON', r';'),
    ('COLON', r':'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('STRING', r'\".*?\"'),
    ('INTEGER', r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('WHITESPACE', r'\s+'),
]

# Compile regex
TOKEN_REGEX = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPEC)
token_re = re.compile(TOKEN_REGEX)

def lexer(input_code):
    tokens = []
    for match in token_re.finditer(input_code):
        token_type = match.lastgroup
        token_value = match.group(token_type)

        if token_type == 'WHITESPACE':
            continue  # Ignore whitespace
        
        if token_type == 'IDENTIFIER' and token_value in KEYWORDS:
            token_type = 'KEYWORD'  # Treat predefined words as keywords
        
        tokens.append((token_type, token_value))
    
    return tokens

# Test input
input_code = '''
X: integer;
Procedure foo( b : integer )
b := 13;
If x = 12 and b = 13 then
printf( "by copy-in copy-out" );
elseif x = 13 and b = 13 then
printf( "by address" );
else
printf( "A mystery" );
end if;
'''

# Run lexer
tokens = lexer(input_code)

# Print tokens
for token in tokens:
    print(token)
