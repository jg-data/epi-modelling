import networkx as nx

# input graphs for our models






# ----- SIR -----

G_SIR = nx.MultiDiGraph()

G_SIR.name = 'SIR'

G_SIR.add_nodes_from(['S', 'I', 'R'], type='species')

#G.add_nodes_from(['infect', 'recover'], type='transaction')

G_SIR.add_node('infect', rate=0.6, type='transaction', latex=r'\beta', var='beta')
G_SIR.add_node('recover', rate=0.2, type='transaction', latex=r'\gamma', var='gamma')

G_SIR.add_edges_from([('S', 'infect'),
                  ('I', 'infect'),
                  ('infect', 'I'),
                  ('infect', 'I'),
                  ('I', 'recover'),
                  ('recover','R')
                  ])

G_SIR.graph['label_offset'] = 0.13
G_SIR.graph['figsize'] = (9, 2)
G_SIR.graph['pos'] = {
    'S': (0, 0),
    'I': (1, 0),
    'R': (2, 0),
    'infect': (0.5, 0),
    'recover': (1.5, 0)
}

G_SIR.graph['edge_curvatures'] = {
    ('I', 'infect', 0): 0.2,
    ('infect', 'I', 0): 0.2,
    ('infect', 'I', 1): 0.5
}



# ----- SIRD -----

G_SIRD = nx.MultiDiGraph()

G_SIRD.name = 'SIRD'


G_SIRD.add_nodes_from(['S', 'I', 'R', 'D'], type='species')

G_SIRD.add_node('infect', rate=0.6, type='transaction', latex=r'\beta', var='beta')
G_SIRD.add_node('recover', rate=0.2, type='transaction', latex=r'\gamma', var='gamma')
G_SIRD.add_node('death', rate=0.003, type='transaction', latex=r'\delta', var='delta')

G_SIRD.add_edges_from([('S', 'infect'),
                  ('I', 'infect'),
                  ('infect', 'I'),
                  ('infect', 'I'),
                  ('I', 'recover'),
                  ('recover','R'),
                  ('I', 'death'),
                  ('death', 'D')
                  ])

G_SIRD.graph['label_offset'] = 0.12
G_SIRD.graph['figsize'] = (9, 3)
G_SIRD.graph['pos'] = {
    'S': (0, 0),
    'I': (1, 0),
    'R': (2, 0.2),
    'D': (2, -0.2),
    'infect': (0.5, 0),
    'recover': (1.5, 0.2),
    'death': (1.5, -0.2)
}

G_SIRD.graph['edge_curvatures'] = {
    ('I', 'infect', 0): 0.2,
    ('infect', 'I', 0): 0.2,
    ('infect', 'I', 1): 0.5
}



# ----- SIRDS -----

G_SIRDS = nx.MultiDiGraph()

G_SIRDS.name = 'SIRDS'

G_SIRDS.add_nodes_from(['S', 'I', 'R', 'D'], type='species')

G_SIRDS.add_node('infect', rate=0.6, type='transaction', latex=r'\beta', var='beta')
G_SIRDS.add_node('recover', rate=0.2, type='transaction', latex=r'\gamma', var='gamma')
G_SIRDS.add_node('death', rate=0.003, type='transaction', latex=r'\delta', var='delta')
G_SIRDS.add_node('waning', rate=0.006, type='transaction', latex=r'\omega', var='omega')

G_SIRDS.add_edges_from([('S', 'infect'),
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

G_SIRDS.graph['label_offset'] = 0.12
G_SIRDS.graph['figsize'] = (9,4)
G_SIRDS.graph['pos'] = {
    'S': (0, 0),
    'I': (1, 0),
    'R': (2, 0.2),
    'D': (2, -0.2),
    'infect': (0.5, 0),
    'recover': (1.5, 0.2),
    'death': (1.5, -0.2),
    'waning': (0.8, 0.4)
}

G_SIRDS.graph['edge_curvatures'] = {
    ('S', 'infect', 0): 0,
    ('I', 'infect', 0): 0.2,
    ('infect', 'I', 0): 0.2,
    ('infect', 'I', 1): 0.5,
    ('I', 'recover', 0): 0,
    ('recover','R', 0): 0,
    ('I', 'death', 0): 0,
    ('death', 'D', 0): 0,
    ('R', 'waning', 0): 0.15,
    ('waning', 'S', 0): 0.15
}



# ----- SIRDS2 (y and o) -----

G_SIRDS2 = nx.MultiDiGraph()

G_SIRDS2.name = 'SIRDS2'

G_SIRDS2.add_nodes_from(['Sy', 'Iy', 'Ry', 'Dy'], type='species')
G_SIRDS2.add_nodes_from(['So', 'Io', 'Ro', 'Do'], type='species')

#G.add_nodes_from(['infect', 'recover'], type='transaction')

G_SIRDS2.add_node('i_oo', rate=0.3, type='transaction', latex=r'\beta_{oo}')
G_SIRDS2.add_node('r_oo', rate=0.2, type='transaction', latex=r'\gamma_{oo}')
G_SIRDS2.add_node('d_oo', rate=0.009, type='transaction', latex=r'\delta_{oo}')
G_SIRDS2.add_node('w_oo', rate=0.006, type='transaction', latex=r'\omega_{oo}')

G_SIRDS2.add_node('i_yy', rate=1.2, type='transaction', latex=r'\beta_{yy}')
G_SIRDS2.add_node('r_yy', rate=0.2, type='transaction', latex=r'\gamma_{yy}')
G_SIRDS2.add_node('d_yy', rate=0.001, type='transaction', latex=r'\delta_{yy}')
G_SIRDS2.add_node('w_yy', rate=0.006, type='transaction', latex=r'\omega_{yy}')

G_SIRDS2.add_node('i_yo', rate=0.2, type='transaction', latex=r'\beta_{yo}')
G_SIRDS2.add_node('i_oy', rate=0.2, type='transaction', latex=r'\beta_{oy}')


SIRDS_edges =    [('S', 'infect'),
                  ('I', 'infect'),
                  ('infect', 'I'),
                  ('infect', 'I'),
                  ('I', 'recover'),
                  ('recover','R'),
                  ('I', 'death'),
                  ('death', 'D'),
                  ('R', 'waning'),
                  ('waning', 'S')
                  ]

def change_add_suffix(s,a):
    if s in ['S', 'I', 'R', 'D']:
        ans = s+a
    else:
        ans = s[0]+'_'+a+a
    return ans

SIRDSo_edges = [(change_add_suffix(x,'o'), change_add_suffix(y,'o'))
                for (x,y) in SIRDS_edges]

SIRDSy_edges = [(change_add_suffix(x,'y'), change_add_suffix(y,'y'))
                for (x,y) in SIRDS_edges]

G_SIRDS2.add_edges_from(SIRDSy_edges+SIRDSo_edges)

cross_edges = [('So', 'i_yo'),
               ('Iy', 'i_yo'),
               ('i_yo', 'Iy'),
               ('i_yo', 'Io'),
               ('Sy', 'i_oy'),
               ('Io', 'i_oy'),
               ('i_oy', 'Iy'),
               ('i_oy', 'Io')
               ]

G_SIRDS2.add_edges_from(cross_edges)


# Useful in console:
#for x in G.nodes:
#    print("'"+str(x)+"'")

G_SIRDS2.graph['pos'] = {
    'Sy': (0,-1),
    'Iy': (2,-1),
    'Ry': (4,-1.4),
    'Dy': (4,-0.6),
    'So': (0,1),
    'Io': (2,1),
    'Ro': (4,1.4),
    'Do': (4,0.6),
    'i_oo': (1, 1),
    'r_oo': (3, 1.4),
    'd_oo': (3, 0.6),
    'w_oo': (1.6, 1.8),
    'i_yy': (1, -1),
    'r_yy': (3, -1.4),
    'd_yy': (3, -0.6),
    'w_yy': (1.6, -1.8),
    'i_yo': (0.5, 0),
    'i_oy': (1.5, 0)
}

G_SIRDS2.graph['edge_curvatures'] = {
    ('Ro', 'w_oo', 0): 0.15,
    ('w_oo', 'So', 0): 0.2,
    ('Ry', 'w_yy', 0): -0.15,
    ('w_yy', 'Sy', 0): -0.2,
    ('i_oo', 'Io', 0): 0.0,
    ('i_oo', 'Io', 1): 0.2,
    ('Io', 'i_oo', 0): 0.2,
    ('i_yy', 'Iy', 0): 0.0,
    ('i_yy', 'Iy', 1): 0.2,
    ('Iy', 'i_yy', 0): 0.2,
    ('i_oy', 'Io', 0): 0.1,
    ('Io', 'i_oy', 0): 0.1,
    ('i_yo', 'Iy', 0): 0,
    ('Iy', 'i_yo', 0): 0.15
    }

G_SIRDS2.graph['label_offset'] = 0.12
G_SIRDS2.graph['figsize'] = (10,9)





# end of graph inputs




