# My Picky Compiler

This project implements a compiler for a hypothetical programming code snippet. The compiler includes lexical analysis (tokenization), syntax analysis (parsing), and visualization of the parse tree.

The compiler is designed to process the code:

```
X: integer;
Procedure foo(b: integer)
  b := 13;
  If x = 12 and b = 13 then
    printf("by copy-in copy-out");
  elseif x = 13 and b = 13 then
    printf("by address");
  else
    printf("A mystery");
  end if;
end foo
```

## Project Structure

The project is divided into five separate files, each responsible for a specific part of the compilation process:

1. **grammar.py**: Contains the `Grammar` class that defines and processes the grammar rules, computes FIRST and FOLLOW sets, and builds the parsing table. Uses tuples for better hashability in LR(1) items.

2. **tokenizer.py**: Contains the `tokenize` function that splits the input pseudocode into tokens with proper handling of whitespace and special tokens.

3. **parser.py**: Contains the `Parser` class that handles the actual parsing process, building parse trees from the token stream using the grammar.

4. **visualizer.py**: Contains the `visualize_parse_tree` function for generating representations of the parse tree. Includes ASCII text visualizations.

5. **main.py**: Contains the `main` function that ties everything together - tokenizes the input, initializes the grammar, parses the tokens, and visualizes the results.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cd-project.git
cd cd-project
```

2. Install the required packages:
```bash
pip install numpy
```

## Usage

To run the compiler on a sample program:

```bash
python main.py
```

This will:
1. Tokenize the input code
2. Parse the tokens using the defined grammar
3. Display the resulting parse tree both as ASCII art in the console

### Customizing Input

To compile a different program, modify the input string in `main.py` or implement command-line argument handling to accept input files.

## Parse Tree Visualization

The project offers two types of parse tree visualization:

1. ASCII Text Visualization (console output)
```
S
└── Program
    ├── Declaration
    │   └── VarDecl
    │       ├── Identifier: X
    │       └── Type: integer
    └── ProcedureDecl
        ├── Identifier: foo
        ├── Parameters
        │   └── Parameter
        │       ├── Identifier: b
        │       └── Type: integer
        └── ...
```
## Extending the Compiler

To extend the compiler for additional language features:

1. Update the grammar rules in `grammar.py`
2. Add any necessary token types in `tokenizer.py`
3. Update the parsing logic in `parser.py` if needed
4. Run the compiler to test your changes

## Troubleshooting

- If you encounter parsing errors, verify that your input code adheres to the language syntax
- Check the console output for any error messages that might help diagnose the problem
