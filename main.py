from grammar import Grammar
from tokenizer import tokenize
from LALR import LALR
from visualizer import visualize_parse_tree
from rich.console import Console
from rich.table import Table
import traceback

def display_tokens_by_line(code, tokens, lexems):
    lines = code.strip().split('\n')
    token_index = 0
    lexeme_items = list(lexems.items())

    print("\nFormatted Tokens & Lexemes Per Line:\n")

    for line_num, line in enumerate(lines):
        print(f"Code Line {line_num+1}: {line.strip()}")

        token_line = []
        lexeme_line = []

        while token_index < len(lexeme_items):
            _, lexeme = lexeme_items[token_index]

            if lexeme in line:
                token_line.append(tokens[token_index])
                lexeme_line.append(lexeme)
                token_index += 1
            else:
                break

        print(f"  Tokens : {' '.join(token_line)}")
        print(f"  Lexems : {' | '.join(lexeme_line)}\n")

def display_parsing_steps_table(parse_output):
    console = Console()
    table = Table(title="Parsing Steps", show_lines=True)

    table.add_column("Step #", justify="right", style="cyan", no_wrap=True)
    table.add_column("Action", style="magenta")

    for i, step in enumerate(parse_output):
        table.add_row(str(i + 1), step)

    console.print(table)

def main():
    # Example input code
    code = """X: integer ;
Procedure foo( b : integer ) 
b := 13; 
If x = 12 and b = 13 then 
    printf( "by copy-in copy-out" ); 
elseif x = 13 and b = 13 then 
    printf( "by address" ); 
else 
    printf( "A mystery" ); 
end if; 
end foo"""

    # Tokenize input
    tokens, lexems = tokenize(code)

    # Pretty print tokens and lexems
    def display_token_lexem_table(tokens, lexems):
        console = Console()
        table = Table(title="Formatted Tokens and Lexems")

        table.add_column("Index", justify="right", style="cyan", no_wrap=True)
        table.add_column("Token", style="magenta")
        table.add_column("Lexem", style="green")

        for idx, token in enumerate(tokens):
            lex = lexems.get(idx, "")
            table.add_row(str(idx), token, lex)

        console.print(table)

    # Call the new table-rendering function
    display_token_lexem_table(tokens, lexems)

    # Line-by-line visual token & lexeme output ---
    display_tokens_by_line(code, tokens, lexems)

    # Initialize grammar and parser
    try:
        print("\nInitializing grammar and parser...")
        grammar = Grammar()
        parser = LALR(grammar)
        grammar.print_parse_table()

        # Parse the input
        print("\nParsing the input...")
        result, parse_output = parser.parse(tokens.copy())

        # Print parsing output
        print("\nParsing Output:")
        display_parsing_steps_table(parse_output)

        if "Accept" in parse_output:
            print("\nParsing Successful!")

            # Build and visualize parse tree
            print("\nBuilding parse tree...")
            try:
                parse_tree = parser.build_parse_tree(tokens.copy(), lexems)

                if parse_tree:
                    print("\nParse Tree:")
                    tree_visual = visualize_parse_tree(parse_tree)
                    tree_visual.render('parse_tree', format='png', cleanup=True)
                    print("\nParse tree image generated: parse_tree.png")
                else:
                    print("\nFailed to build parse tree.")
            except Exception as e:
                print(f"\nError building parse tree: {e}")
        else:
            print("\nParsing Failed.")

    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()