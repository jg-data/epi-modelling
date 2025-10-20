import networkx as nx
import matplotlib.pyplot as plt


def draw_SPN(G, t_disp='rate'):
    plt.figure(figsize=G.graph.get('figsize', (12,8)) )
    plt.axis('equal')
    
    pos = G.graph['pos']
    
    # Split nodes by type
    species_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'species']
    transaction_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'transaction']
    
    # Draw nodes on top
    nx.draw_networkx_nodes(G, pos, nodelist=species_nodes, node_color='lightblue', node_shape='o', node_size=1800, edgecolors='black')
    nx.draw_networkx_nodes(G, pos, nodelist=transaction_nodes, node_color='lightgreen', node_shape='s', node_size=1600)

    # Use node size to determine reasonable label offset
    label_offset = G.graph.get('label_offset', 0.1)

    # Draw labels for species nodes (default position)
    species_labels = {n: n for n in species_nodes}
    nx.draw_networkx_labels(G, pos, labels=species_labels, font_size=16)

    # Draw weight and label for transaction nodes
    for n in transaction_nodes:
        node_data = G.nodes[n]
        x, y = pos[n]
    
        # Weight inside the node
        weight = node_data.get('rate', None)
            
        if weight is not None:
            plt.text(x, y,      # Same coordinates as node center
                f"{weight}", 
                fontsize=14, 
                ha='center', 
                va='center', 
                color='black', 
                zorder=3)       # Ensure it's above edges

    # === Draw edges with curvature ===
    for u, v, k in G.edges(keys=True):
        rad = G.graph.get('edge_curvatures', {}).get((u, v, k), 0.0)  # default: straight
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle='-|>',
            arrowsize=20,
            edge_color='black',
            width=2,
            min_source_margin=27,
            min_target_margin=23
        )

    #plt.title("title")
    plt.axis('off')
    plt.show()
