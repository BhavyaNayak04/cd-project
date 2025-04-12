class Grammar:
    def __init__(self):
        # Define the grammar rules with adjusted token names
        self.goto = None
        self.follow = None
        self.first = None
        self.action = None
        self.rules = [
            ("P'", ["P"]),
            ("P", ["Decl", "Proc"]),
            ("Decl", ["id", "COLON", "T", "SEMI"]),
            ("Param", ["id", "COLON", "T"]),
            ("Proc", ["procedure", "id", "LPAREN", "Param", "RPAREN", "S", "end", "id"]),
            ("S", ["St"]),
            ("S", ["S", "St"]),
            ("St", ["A", "SEMI"]),
            ("St", ["I", "SEMI"]),
            ("St", ["F", "SEMI"]),
            ("A", ["id", "ASSIGN", "num"]),
            ("I", ["if", "C", "then", "S", "elsif", "C", "then", "S", "else", "S", "end", "if"]),
            ("C", ["Cmp", "and", "Cmp"]),
            ("Cmp", ["id", "EQ", "num"]),
            ("F", ["printf", "LPAREN", "str", "RPAREN"]),
            ("T", ["integer"])
        ]

        # Define terminals and non-terminals
        self.terminals = {
            "id", "COLON", "integer", "SEMI", "procedure", "LPAREN", "RPAREN",
            "ASSIGN", "num", "if", "then", "elsif", "else", "end", "and", "EQ", "printf", "str", "$"
        }

        self.non_terminals = {
            "P'", "P", "Decl", "Param", "Proc", "S", "St", "A", "I", "C", "Cmp", "F", "T"
        }

        # Compute FIRST and FOLLOW sets
        self.compute_first_sets()
        self.compute_follow_sets()

        # Build the parsing table
        self.build_parsing_table()

    def compute_first_sets(self):
        # Initialize FIRST sets
        self.first = {symbol: set() for symbol in self.terminals | self.non_terminals}

        # FIRST set for terminals is the terminal itself
        for terminal in self.terminals:
            self.first[terminal] = {terminal}

        # Compute FIRST sets for non-terminals
        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.rules:
                if not rhs:  # Empty production
                    if '' not in self.first[lhs]:
                        self.first[lhs].add('')
                        changed = True
                else:
                    all_nullable = True
                    for symbol in rhs:
                        # Add FIRST(symbol) - {''} to FIRST(lhs)
                        first_symbol = self.first[symbol] - {''}
                        if first_symbol - self.first[lhs]:
                            self.first[lhs] |= first_symbol
                            changed = True

                        # If symbol is not nullable, break
                        if '' not in self.first[symbol]:
                            all_nullable = False
                            break

                    # If all symbols in RHS are nullable, add '' to FIRST(lhs)
                    if all_nullable and '' not in self.first[lhs]:
                        self.first[lhs].add('')
                        changed = True

    def compute_follow_sets(self):
        # Initialize FOLLOW sets
        self.follow = {nt: set() for nt in self.non_terminals}

        # Add $ to FOLLOW(S') where S' is the start symbol
        self.follow["P'"] = {'$'}

        # Compute FOLLOW sets
        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.rules:
                for i, symbol in enumerate(rhs):
                    if symbol in self.non_terminals:
                        # For A -> αBβ, add FIRST(β) - {''} to FOLLOW(B)
                        first_beta = set()
                        nullable_beta = True

                        for beta in rhs[i + 1:]:
                            beta_first = self.first[beta] - {''}
                            first_beta |= beta_first
                            if '' not in self.first[beta]:
                                nullable_beta = False
                                break

                        if first_beta - self.follow[symbol]:
                            self.follow[symbol] |= first_beta
                            changed = True

                        # If β is nullable or empty, add FOLLOW(A) to FOLLOW(B)
                        if nullable_beta or i == len(rhs) - 1:
                            if self.follow[lhs] - self.follow[symbol]:
                                self.follow[symbol] |= self.follow[lhs]
                                changed = True

    def build_parsing_table(self):
        self.action = {}
        self.goto = {}

        # Build canonical collection of LR(1) items
        # Using tuples instead of lists for hashability
        start_item = (("P'", (".", "P")), '$')
        state0 = self.closure({start_item})
        states = [state0]
        state_map = {frozenset(state0): 0}

        # Process all states
        for i, state in enumerate(states):
            # For each grammar symbol X
            for X in self.terminals | self.non_terminals:
                if X == '$':
                    continue

                # Compute GOTO(I,X)
                goto_set = self.goto_operation(state, X)

                if not goto_set:
                    continue

                # Check if this state already exists
                goto_set_frozen = frozenset(goto_set)
                if goto_set_frozen in state_map:
                    j = state_map[goto_set_frozen]
                else:
                    j = len(states)
                    state_map[goto_set_frozen] = j
                    states.append(goto_set)

                # Fill action and goto tables
                if X in self.terminals:
                    self.action[(i, X)] = ('shift', j)
                else:
                    self.goto[(i, X)] = j

            # Add reduce actions
            for (lhs, rhs), lookahead in state:
                dot_index = rhs.index('.') if '.' in rhs else -1
                if dot_index == len(rhs) - 1:  # Dot at the end
                    if lhs == "P'" and rhs == (".", "P") and lookahead == '$':
                        self.action[(i, '$')] = ('accept',)
                    else:
                        real_rhs = tuple(s for s in rhs if s != '.')
                        # Find the rule index
                        rule_idx = None
                        for idx, (rule_lhs, rule_rhs) in enumerate(self.rules):
                            if rule_lhs == lhs and list(real_rhs) == rule_rhs:
                                rule_idx = idx
                                break

                        if rule_idx is not None:
                            for term in self.terminals:
                                if term == lookahead or lookahead == '':
                                    self.action[(i, term)] = ('reduce', rule_idx)

    def closure(self, items):
        result = set(items)
        worklist = list(items)

        while worklist:
            item = worklist.pop(0)
            (lhs, rhs), lookahead = item

            # Convert rhs to a list temporarily for easier manipulation
            rhs_list = list(rhs)
            if '.' in rhs_list and rhs_list.index('.') < len(rhs_list) - 1:
                dot_pos = rhs_list.index('.')
                next_symbol = rhs_list[dot_pos + 1]

                if next_symbol in self.non_terminals:
                    # Compute first set of the string after the next_symbol
                    beta = rhs_list[dot_pos + 2:] if dot_pos + 2 < len(rhs_list) else []
                    beta_with_lookahead = beta + [lookahead]

                    first_beta_a = set()
                    for symbol in beta_with_lookahead:
                        if symbol in self.terminals or symbol == '$':
                            first_beta_a.add(symbol)
                            break
                        symbol_first = self.first[symbol] - {''}
                        first_beta_a |= symbol_first
                        if '' not in self.first[symbol]:
                            break
                    else:
                        first_beta_a.add(lookahead)

                    # Add closure items
                    for prod_lhs, prod_rhs in self.rules:
                        if prod_lhs == next_symbol:
                            for term in first_beta_a:
                                new_item = ((prod_lhs, (".",) + tuple(prod_rhs)), term)
                                if new_item not in result:
                                    result.add(new_item)
                                    worklist.append(new_item)

        return result

    def goto_operation(self, items, symbol):
        goto_items = set()

        for (lhs, rhs), lookahead in items:
            # Convert to list for manipulation
            rhs_list = list(rhs)
            if '.' in rhs_list and rhs_list.index('.') < len(rhs_list) - 1:
                dot_pos = rhs_list.index('.')
                next_symbol = rhs_list[dot_pos + 1]

                if next_symbol == symbol:
                    # Move the dot
                    rhs_list[dot_pos], rhs_list[dot_pos + 1] = rhs_list[dot_pos + 1], rhs_list[dot_pos]
                    # Convert back to tuple for hashability
                    new_item = ((lhs, tuple(rhs_list)), lookahead)
                    goto_items.add(new_item)

        return self.closure(goto_items)