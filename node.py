

from typing import List, Tuple, FrozenSet, Union
from base_types import *

class Node(GraphObject):
    def __init__(self, key, edges=[]):
        self._key = key
        self._edges = set()
        self._graph = None
    
    @property
    def key(self):
        self._key

    def attach(self, graph):
        assert(self._graph is None)
        self._graph = graph
        assert(self not in self._graph)
        self._graph.V.add(self)
    
    def detach(self):
        assert(self._graph)
        for edge in self.edges:
            edge.detach()
        self._graph.V.remove(self)
        self._graph = None
        del self
    
    def __eq__(self, other):
        # FIXME - add type check
        return (self._key == other._key)

    def __hash__(self):
        return hash(self._key)
    
    def __str__(self):
        return str(self._key)
    
    @property
    def edges(self):
        return self._edges
    
    @property
    def children(self):
        for edge in self.edges:
            if (edge[0].key == self.key): yield edge[1]
    
    @property
    def parents(self):
        for edge in self.edges:
            if (edge[1].key == self.key): yield edge[0]

    @property
    def neighbors(self):
        assert(self._graph)
        undirected = self._graph.undirected
        for edge in self.edges:
            if undirected or (edge[0].key == self.key):
                yield edge[1] if (edge[0].key == self.key) else edge[0]