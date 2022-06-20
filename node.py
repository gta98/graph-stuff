

from typing import List, Tuple, FrozenSet, Union
from base_types import *
from edge import Edge

class NodeKey(BaseKey): pass

class Node(GraphObject):
    def __init__(self, key: NodeKey, edges=[]):
        self._key = key or NodeKey()
        self.edges = []
        self._graph = None

    @property
    def key(self):
        return self._key if (type(self._key) == NodeKey) else NodeKey(self._key)

    def attach(self, graph):
        assert(self._graph is None)
        if self._graph:
            self.detach()
        self._graph = graph
        self._graph[self.key] = self
    
    def detach(self):
        assert(self._graph)
        if self._graph:
            for edge in self.edges:
                edge.detach()
            self._graph.V.pop(self.key)
            self._graph = None