def visualize_parse_tree(node, prefix="", is_last=True):
    """
    Generate a string representation of a parse tree using ASCII art.

    Args:
        node: The current node in the parse tree
        prefix: The prefix to use for the current line (for indentation)
        is_last: Whether this node is the last child of its parent

    Returns:
        A string representation of the parse tree
    """
    if not node:
        return ""

    result = ""

    # Print current node
    if node['type'] == 'terminal':
        value = node['value'] if 'value' in node else node['symbol']
        node_str = f"{node['symbol']}: {value}"
    else:
        node_str = node['symbol']

    result += prefix
    result += "└── " if is_last else "├── "
    result += f"{node_str}\n"

    # Print children
    children = node.get('children', [])
    for i, child in enumerate(children):
        new_prefix = prefix + ("    " if is_last else "│   ")
        result += visualize_parse_tree(child, new_prefix, i == len(children) - 1)

    return result