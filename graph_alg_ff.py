
from base_types import *
from graph import DirectedGraph, Node, Edge
from g_queue import Queue

def BFS(G:Graph, s:Node) -> None:
    for v in G.V:
        v.color = WHITE
        v.d[s] = infinity
        v.pi[s] = None
    s.color = Color.GRAY
    s.d[s] = 0
    s.pi[s] = None
    Q = Queue()
    Q.enqueue(s)
    while not Q.empty:
        u = Q.dequeue()
        for v in u.neighbors:
            if v.color == WHITE:
                v.color = GRAY
                v.d[s] = u.d[s] + 1
                v.pi = u
                Q.enqueue(v)
        u.color = BLACK

def DFS(G:Graph) -> None:
    t:int = 0
    s:Node = None
    def DFS_inner(u:Node) -> None:
        nonlocal t, s
        t += 1
        u.d[s] = t
        u.color = GRAY
        for v in u.neighbors:
            if v.color == WHITE:
                v.pi[s] = u
                DFS_inner(v)
        t += 1
        u.color = BLACK
        #u.f[s] = t
        pass
    for u in G.V:
        u.color = WHITE
    for s in G.V:
        if s.color == WHITE:
            DFS_inner(u)

def get_augmenting_graph(G:DirectedGraph) -> DirectedGraph:
    Gf = DirectedGraph()
    for v in G.V: Gf += v
    for edge in G.E:
        if (edge.flow < edge.capacity) and (edge not in Gf):
            Gf += edge.copy
        if (edge.flow > 0) and (edge.inverse not in Gf):
            Gf += edge.copy.inverse
    for edge in Gf.E:
        if edge in G:
            edge.capacity = G.E[edge].capacity - G.E[edge].flow
        else:
            edge.capacity = G.E[edge.inverse].flow
        edge.flow = 0
    return Gf

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