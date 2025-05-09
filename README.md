# My Picky Compiler

This project implements a compiler for a small hypothetical programming language. It performs **lexical analysis**, **syntax analysis**, and visualizes the **parse tree** as a generated image.

The compiler is designed to process this input code:

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

---

## Project Structure

The compiler is modular and organized into five main components:

1. **`grammar.py`** – Defines grammar rules, computes FIRST/FOLLOW sets, builds the LR(1) parsing table.
2. **`tokenizer.py`** – Splits input into tokens, respecting whitespace and special characters.
3. **`parser.py`** – Builds the parse tree using LR(1) parsing from the token stream.
4. **`visualizer.py`** – Generates a visual parse tree as an image using Graphviz.
5. **`main.py`** – Coordinates all steps, prints token and parse info, and triggers visualization.

---

## Key Features

* Full lexical analysis (with token–lexeme table)
* Generation of:

  * **Goto Table**
  * **Action Table**
  * **Detailed Parsing Steps Table**
* Parse tree image generation using **Graphviz**
* Rich terminal formatting using **rich**

---

## Installation

### Prerequisites

* Python 3.7 or higher
* [Graphviz](https://graphviz.org/download/) (required for image generation)
* pip (Python package installer)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/cd-project.git
   cd cd-project
   ```

2. **Install Python dependencies:**

   ```bash
   pip install numpy rich
   ```

3. **Install Graphviz:**

   * Download from: [https://graphviz.org/download/](https://graphviz.org/download/)
   * Add Graphviz to the system `PATH` (environment variables) so it can be accessed via command line.
   * You can verify it's installed correctly with:

     ```bash
     dot -V
     ```

---

## Usage

To run the compiler with the sample program:

```bash
python main.py
```

The compiler will:

1. Tokenize the input source code
2. Display a formatted **Token–Lexeme Table**
3. Display **Goto Table** and **Action Table**
4. Walk through the **LR(1) parsing steps**
5. Generate a **parse tree image** (saved as `parse_tree.png`)

---

## Output Example

Here's what the output includes:

* **Lexical Analysis Table**
* **Parsing Tables (Goto, Action)**
* **Step-by-step LR(1) Parsing Process**
* **Parse Tree Image** – Saved to the local folder as `parse_tree.png`

---

## Custom Input

To compile a different program:

* Edit the `program_code` string inside `main.py`
* Or modify it to take input from a file or CLI in the future

---

## Extend the Compiler

To add support for more language features:

1. Update grammar rules in `grammar.py`
2. Add new tokens in `tokenizer.py`
3. Adjust parsing logic in `parser.py` as needed
4. Rerun the compiler to test your changes

---

## Troubleshooting

* If the image doesn’t generate, make sure Graphviz is correctly installed and added to your system `PATH`.
* Parsing errors typically mean the input code doesn't conform to the grammar.
* Rich formatting issues can usually be solved by ensuring your terminal supports ANSI escape sequences.
