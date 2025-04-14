from graphviz import Digraph

def visualize_parse_tree(parse_tree):
    dot = Digraph(format='png', engine="dot")
    node_count = [0]

    def add_nodes_edges(node, parent_id=None):
        node_id = f"node{node_count[0]}"
        node_count[0] += 1

        # Determine label
        if node['type'] == 'terminal':
            label = f"{node['symbol']}\n{node['value']}"
        else:
            label = node['symbol']

        dot.node(node_id, label)

        if parent_id:
            dot.edge(parent_id, node_id)

        for child in node.get('children', []):
            add_nodes_edges(child, node_id)

    add_nodes_edges(parse_tree)
    return dot
