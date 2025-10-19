import networkx as nx
import matplotlib.pyplot as plt
import subprocess

G = nx.MultiDiGraph()


G.add_nodes_from(['S', 'I', 'R', 'D'], type='species')

G.add_node('infect', rate=0.6, type='transaction', latex=r'\beta')
G.add_node('recover', rate=0.2, type='transaction', latex=r'\gamma')
G.add_node('death', rate=0.003, type='transaction', latex=r'\delta')
G.add_node('waning', rate=0.006, type='transaction', latex=r'\omega')

G.add_edges_from([('S', 'infect'),
                  ('I', 'infect'),
                  ('infect', 'I'),
                  ('infect', 'I'),
                  ('I', 'recover'),
                  ('recover','R'),
                  ('I', 'death'),
                  ('death', 'D'),
                  ('R', 'waning'),
                  ('waning', 'S')
                  ])


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
                term += ' '+l[1]
                
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
    display(Math(latex_code(G, symbol)))


