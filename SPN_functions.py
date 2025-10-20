import networkx as nx
import matplotlib.pyplot as plt
import copy
from scipy.integrate import solve_ivp


# ----- draw SPN graphs -----

def draw_SPN(G, t_disp='rate', t_label=True):
    # INPUT: model graph G; attribute t_disp
    # default: displays rate in transaction boxes
    #          can change by altering t_disp
    
    # OUTPUT: shows figure, returns nothing
    
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
        if 'latex' == t_disp:
            weight = '$'+node_data.get(t_disp, None)+'$'
        else:
            weight = node_data.get(t_disp, None)
            
        if weight is not None:
            plt.text(x, y,      # Same coordinates as node center
                f"{weight}", 
                fontsize=14, 
                ha='center', 
                va='center', 
                color='black', 
                zorder=3)       # Ensure it's above edges

    # Label below the node
        if t_label:
            plt.text(x, y - label_offset,    # Slightly below node
                     n, fontsize=14, ha='center', 
                     va='top', color='black',zorder=3)


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


# ----- rate equation in latex and code -----

# key functions:
#     pdf_rate_eqs(G, filename=False, symbol=True)
#     saves PDF of rate equations using LaTeX
    
#     jupyter_rate_eqs(G, symbol=True)
#     displays LaTeX rate equations in Jupyter Notebook
    
#     python_rate_fun(G, var_names=False)
#     returns code for rate equations using given rates

def transactions(G):
    return [n for n, attr in G.nodes(data=True) if attr.get('type') == 'transaction']

def species(G):
    return [n for n, attr in G.nodes(data=True) if attr.get('type') == 'species']

def species_rate_from_transaction(G, spec, tran, symbol=False, rem_zero=False):
    n = G.number_of_edges(tran, spec)
    ms = {}
    specs = species(G)
    for s in specs:
        ms[s] = G.number_of_edges(s, tran)
    multiple = n - ms[spec]
    if symbol:
        rate = G.nodes[tran]['latex']
    else:
        rate = G.nodes[tran]['rate']
    if rem_zero:
        for s in specs:
            if 0 == ms[s]:
                del ms[s]
    ans = [multiple, rate, ms]
    return ans


def pm_str(n):
    # INPUT: number
    # OUTPUT: string with +/- before number.  0 gets +
    if n<0:
        return str(n)
    else:
        return '+'+str(n)


def latex_species_rate(G, spec, symbol=True, align=True):
    ans = r'\frac{d'+spec+'}{dt}'
    if align:
        ans += "&="
    else:
        ans += "="
    for t in transactions(G):
        l = species_rate_from_transaction(G, spec, t, symbol, rem_zero=True)
        #for l in tlist:
        n_m = l[0]
        if 0 != n_m:
                if 1 == n_m:
                    term = '+'
                elif -1 == n_m:
                    term = '-'
                else:
                    term = pm_str(n_m)
                
                if symbol:
                    term += ' '+l[1]
                else:
                    term += ' '+str(l[1])
                
                for sp,m in l[2].items():
                    if 1==m:
                        term += ' ' + sp
                    else:
                        term += ' ' + sp + '^{' + m + '}'
                ans += term
    if align:
        ans += r'\\'
    return ans


def latex_image_spec(G, spec, symbol=True):
    #plt.figure(figsize=(6,3))
    plt.axis("off")
    code = "$"+latex_species_rate(G, spec, symbol, align=False)+"$"
    plt.text(0.1, 0.5, code, ha='left', va='center', fontsize=14)
    plt.tight_layout()
    plt.show()


def latex_image(G, symbol=True):
    plt.axis("off")
    code = ''
    for s in species(G):
        code += '$'+latex_species_rate(G, s, symbol, align=False)+'$ \n'
    
    plt.text(0.1, 0.5, code, ha='left', va='center', fontsize=14)
    plt.tight_layout()
    plt.show()
    

def latex_code(G, symbol=True):
    code = r'\begin{align*} '
    for s in species(G):
        code += latex_species_rate(G, s, symbol, align=True)
    code = code[:-2] + r'\end{align*}'
    return code


def pdf_rate_eqs(G, filename=False, symbol=True):
    code = r"""
    \documentclass{article}
    \usepackage{amsmath}

    \begin{document}

    """ + latex_code(G, symbol) + r"""
    \end{document}
    """
    if False==filename:
        filename = "equations.tex"
        
    # Write to file
    with open(filename, "w") as f:
        f.write(code)

    # Compile
    subprocess.run(["pdflatex", "equations.tex"])


def jupyter_rate_eqs(G, symbol=True):
    from IPython.display import display, Math
    #display(Math(latex_code(G, symbol)))
    for s in species(G):
        display(Math('$'+latex_species_rate(G, s, symbol, align=False)+'$'))



def python_species_rate(G, spec, var_names=False):
    # idea: if var is false, hard code rates.
    #       if true, use variable names (not coded!!)
    if var_names:
        raise ValueError("Var names implement not coded")
    ans = spec+'prime = '
    for t in transactions(G):
        l = species_rate_from_transaction(G, spec, t, symbol=False, rem_zero=True)
        n_m = l[0]
        if 0 != n_m:
            term = f"+ {l[0]} * {l[1]} "
            for sp,m in l[2].items():
                if 1==m:
                    term += f"* {sp} "
                else:
                    term += f"* pow({sp},m) "
            ans += term
    return ans

def species_with_commas(G):
    # returns string of species names with commas
    ss = species(G)
    ans = ss[0]
    for s in ss[1:]:
        ans += ", " + s
    return ans

def species_prime_with_commas(G):
    # returns string of species names with
    # prime added to each, and with commas
    ss = species(G)
    ans = ss[0]
    for s in ss[1:]:
        ans += "prime, " + s
    return ans + "prime"



def python_rate_code(G, var_names=False):
    #if 'name' not in G.graph:
    #    raise ValueError("Graph needs a name")
    #code = f"def {G.name}_model(t, x0):\n"
    code = "def ratefun(t, x0):\n"
    fs = "    "
    code += fs + species_with_commas(G) + " = x0\n"
    for s in species(G):
        code += fs + python_species_rate(G, s, var_names) + "\n"
    code += fs + "return (" + species_prime_with_commas(G) + ")\n"
    return code

def python_rate_fun(G, var_names=False):
    sandbox = {}
    exec(python_rate_code(G, var_names), sandbox)
    return sandbox['ratefun']


# ----- deep copying graphs -----

# needed because we store data in attributes

def deep_copy_graph(G):
    # Create the same type of graph (MultiDiGraph, DiGraph, etc.)
    H = G.__class__()

    # Copy graph-level attributes
    H.graph = copy.deepcopy(G.graph)

    # Copy nodes and their attributes
    for node, data in G.nodes(data=True):
        H.add_node(node, **copy.deepcopy(data))

    # Copy edges and their attributes (including keys, if a MultiGraph)
    if G.is_multigraph():
        for u, v, k, data in G.edges(data=True, keys=True):
            H.add_edge(u, v, key=k, **copy.deepcopy(data))
    else:
        for u, v, data in G.edges(data=True):
            H.add_edge(u, v, **copy.deepcopy(data))

    return H



# ----- solve rate equations for graph -----

def solve_SPN(G, inits, t0=0, t1=365):
    rate_fun = python_rate_fun(G)
    return solve_ivp(rate_fun, t_span=(t0, t1), 
                     y0=inits, rtol=1e-9, atol=1e-12)


# ----- plot proportions -----

def proportions(G, inits, t0=0, t1=365, fs=(10,5), title="", col_alpha=False, cols=None, alphas=None, key_loc=(0.06, 0.7)):
    sim = solve_SPN(G, inits, t0, t1)
    
    specs = species(G)
    n = len(specs)
    
    backsums = [sim.y[n-1]]
    for i in range(n-1):
        backsums.append(backsums[-1]+sim.y[n-2-i])
    
    plt.figure(figsize=fs) # default (width, height) = (6.4, 4.8)
    
    if col_alpha:
        for i in range(n-1):
            plt.fill_between(sim.t, backsums[n-2-i], backsums[n-1-i], label=specs[i], color=cols[specs[i]], alpha=alphas[specs[i]])
        
        plt.fill_between(sim.t, 0, backsums[0], label=specs[n-1], color=cols[specs[n-1]], alpha=alphas[specs[n-1]])
        
        #raise ValueError("need to get colours working")
        # plt.fill_between(ts, SIRDS_backsums[2], SIRDS_backsums[3], color='black', label='S', alpha=0.1)
    else:
        for i in range(n-1):
            plt.fill_between(sim.t, backsums[n-i-1], backsums[n-i-1], label=specs[i])
        
        plt.fill_between(sim.t, 0, backsums[0], label=specs[n-1])
        
    for i in range(n):
        plt.plot(sim.t, backsums[i], color='black')
        
    plt.xlabel('time (days)')
    plt.ylabel('population proportions')
    plt.legend(loc=key_loc)
    plt.title(title)
    plt.show()

    return None









