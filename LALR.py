class LALR:
    def __init__(self, grammar):
        self.grammar = grammar
        self.parsing_table = grammar.action, grammar.goto

    def parse(self, tokens):
        tokens.append('$')
        action_table, goto_table = self.parsing_table

        # Initialize parsing stack
        stack = [0]
        output = []
        symbols = []

        i = 0
        while True:
            state = stack[-1]
            symbol = tokens[i]

            # Look up action
            if (state, symbol) in action_table:
                action = action_table[(state, symbol)]

                if action[0] == 'shift':
                    stack.append(action[1])
                    symbols.append(symbol)
                    i += 1
                    output.append(f"Shift to state {action[1]}")

                elif action[0] == 'reduce':
                    rule_index = action[1]
                    lhs, rhs = self.grammar.rules[rule_index]

                    # Pop |rhs| symbols and states
                    for _ in range(len(rhs)):
                        stack.pop()
                        symbols.pop()

                    # Push the LHS non-terminal
                    state = stack[-1]
                    symbols.append(lhs)

                    # Special case for the start symbol
                    if lhs == "P'" and state == 0:
                        output.append(f"Reduce by {lhs} -> {' '.join(rhs)}")
                        output.append("Accept")
                        break
                    elif (state, lhs) in goto_table:
                        stack.append(goto_table[(state, lhs)])
                        output.append(f"Reduce by {lhs} -> {' '.join(rhs)}")
                    else:
                        output.append(f"Error: No goto entry for state {state} and symbol {lhs}")
                        return None, output

                elif action[0] == 'accept':
                    output.append("Accept")
                    break
            else:
                output.append(f"Error at symbol {symbol}")
                return None, output

        return symbols, output

    def build_parse_tree(self, tokens, lexems):
        tokens_copy = tokens.copy()
        tokens_copy.append('$')
        action_table, goto_table = self.parsing_table

        # Initialize parsing stack and tree nodes
        stack = [0]
        nodes = []
        i = 0

        while True:
            state = stack[-1]
            current_token = tokens_copy[i]

            # Look up action
            if (state, current_token) in action_table:
                action = action_table[(state, current_token)]

                if action[0] == 'shift':
                    stack.append(action[1])
                    # Create leaf node for terminal
                    node = {
                        'type': 'terminal',
                        'symbol': current_token,
                        'value': lexems.get(i, current_token),
                        'children': []
                    }
                    nodes.append(node)
                    i += 1

                elif action[0] == 'reduce':
                    rule_index = action[1]
                    lhs, rhs = self.grammar.rules[rule_index]

                    # Pop |rhs| symbols and states
                    children = []
                    for _ in range(len(rhs)):
                        stack.pop()
                        if nodes:  # Check if there are nodes to pop
                            children.insert(0, nodes.pop())

                    # Create non-terminal node
                    node = {
                        'type': 'non-terminal',
                        'symbol': lhs,
                        'children': children
                    }
                    nodes.append(node)

                    # Push goto state
                    state = stack[-1]

                    # Special case for the start symbol
                    if lhs == "P'" and state == 0:
                        return node  # Return the root of the parse tree
                    elif (state, lhs) in goto_table:
                        stack.append(goto_table[(state, lhs)])
                    else:
                        error_msg = f"No goto entry for state {state} and symbol {lhs}"
                        raise Exception(error_msg)

                elif action[0] == 'accept':
                    return nodes[0]  # Return the root of the parse tree
            else:
                error_msg = f"Syntax error: unexpected token '{current_token}' at position {i}"
                raise Exception(error_msg)

    def print_parse_tree(self, node, depth=0):
        if node['type'] == 'terminal':
            value = node['value'] if 'value' in node else node['symbol']
            print('  ' * depth + f"{node['symbol']}: {value}")
        else:
            print('  ' * depth + f"{node['symbol']}")
            for child in node['children']:
                self.print_parse_tree(child, depth + 1)