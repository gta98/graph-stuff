
from base_types import *
from graph import DirectedGraph, Node, Edge

def get_augmenting_graph(G: DirectedGraph) -> DirectedGraph:
    G = G.copy()
    for e in G.E:
        e_copy = e.copy()
        new_capacity = e.capacity - e.flow
        inverse_capacity_addition = e.flow
        if new_capacity > 0:
            e.capacity = new_capacity
            e.flow = 0
        else:
            e.detach()
        e_inverse = e_copy.copy().invert()
        e_inverse_in_G = G[e_inverse]
        if inverse_capacity_addition > 0:
            if not e_inverse_in_G:
                e_inverse.attach(G)
                e_inverse_in_G = e_inverse
                e_inverse_in_G.capacity = 0
            e_inverse_in_G.capacity += inverse_capacity_addition
            e_inverse_in_G.flow = 0

def DFS(G: DirectedGraph, s: Node):
    for v in G.V:
        setattr(v, "pi", None)
    def DFS_inner(v: Node):
        for neighbor in v.neighbors:
            if not neighbor.pi:
                neighbor.pi = v
                DFS_inner(v)
    DFS_inner(s)

def find_path(G: DirectedGraph, s: Node, t: Node) -> List[Node]:
    DFS(G, s)
    if t.pi is None: return None
    l = []
    v_next = t
    while v_next:
        l.append(v_next)
        v_next = v_next.prev
    return l[::-1]

def find_augmenting_path(G: DirectedGraph, s: Node, t: Node) -> List[Edge]:
    vertices = find_path(get_augmenting_graph(G), s, t)
    edges = [Edge(p[i], p[i+1]) for i in range(len(p)-1)]
    for edge in edges:
        edge.attach(G)
    return edges

def get_path_capacity(p: List[Edge]) -> int:
    return min([e.capacity for e in p])

def augment_path(G: DirectedGraph, augmenting: List[Edge], capacity):
    for e in G.E:
        e_copy = e.copy()
        new_capacity = e.capacity - capacity
        inverse_capacity_addition = e.capacity
        if new_capacity > 0:
            e.capacity = new_capacity
            e.flow = 0
        else:
            e.detach()
        e_inverse = e_copy.copy().invert()
        e_inverse_in_G = G[e_inverse]
        if inverse_capacity_addition > 0:
            if not e_inverse_in_G:
                e_inverse.attach(G)
                e_inverse_in_G = e_inverse
                e_inverse_in_G.capacity = 0
            e_inverse_in_G.capacity += inverse_capacity_addition
            e_inverse_in_G.flow = 0

def ff(G: DirectedGraph, s: Node, t: Node):