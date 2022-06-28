

from ast import Assert
from typing import List, Tuple, FrozenSet, Union
from .base_types import *

class GraphVertex(GraphObject):

    def __init__(self, key, **extras):
        super().__init__(extras=extras)
        self._key = key
    
    def _validate_extras(self):
        pass
    
    def __eq__(self, other):
        # FIXME - add type check
        return (self._key == other._key)

    def __hash__(self):
        return hash(self._key)

    def __str__(self):
        return str(self._key)
    
    def copy(self):
        return GraphVertex(self._key, self._extras)
 
    @property
    def graph(self):
        return self['graph']

    @property
    def edges(self):
        for other in self.graph.E[self]:
            yield self.graph.E[self][other]
    
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
        for edge in self.edges:
            if self == edge.node_1:
                yield edge.node_2
            elif self == edge.node_2:
                if (not self.graph) or self.graph.undirected: yield edge.node_1
            else:
                raise Exception(f"Node {self} contains an invalid edge: {edge}")