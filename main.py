from grammar import Grammar
from tokenizer import tokenize
from LALR import LALR
from visualizer import visualize_parse_tree
import traceback

def main():
    # Example input code
    code = """X: integer ;
Procedure foo( b : integer ) 
b := 13; 
If x = 12 and b = 13 then 
    printf( "by copy-in copy-out" ); 
elsif x = 13 and b = 13 then 
    printf( "by address" ); 
else 
    printf( "A mystery" ); 
end if; 
end foo"""

    # Tokenize input
    tokens, lexems = tokenize(code)
    print("Tokens:", tokens)
    print("Lexems:", lexems)

    # Print the tokenized form directly
    token_str = ' '.join(tokens)
    print("\nTokenized string format:")
    print(token_str)

    # Initialize grammar and parser
    try:
        print("\nInitializing grammar and parser...")
        grammar = Grammar()
        parser = LALR(grammar)

        # Parse the input
        print("\nParsing the input...")
        result, parse_output = parser.parse(tokens.copy())

        # Print parsing output
        print("\nParsing Output:")
        for step in parse_output:
            print(step)

        # Check if parsing was successful
        if "Accept" in parse_output:
            print("\nParsing Successful!")

            # Build and visualize parse tree
            print("\nBuilding parse tree...")
            try:
                parse_tree = parser.build_parse_tree(tokens.copy(), lexems)

                if parse_tree:
                    print("\nParse Tree:")
                    print(visualize_parse_tree(parse_tree))
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