

from typing import List, Tuple, FrozenSet, Union
from base_types import *
from node import NodeKey

class Node: pass
class DirectedGraph: pass

class EdgeKey(BaseKey): pass

class Edge(Attachable):
    def __init__(self, obj_1: Union[Node, NodeKey], obj_2: Union[Node, NodeKey], capacity: int):
        if type(obj_1) == Node: obj_1 = obj_1.key
        if type(obj_2) == Node: obj_2 = obj_2.key
        assert((type(obj_1) == NodeKey) and (type(obj_2) == NodeKey))
        self._key_1 = obj_1
        self._key_2 = obj_2
        self._capacity = capacity
        self._graph = None

    @property
    def key(self):
        return EdgeKey((self.key_1, self.key_2))
    
    def attach(self, graph):
        assert(self.graph is None)
        assert(self.key_1 in graph.V.keys())
        assert(self.key_2 in graph.V.keys())
        if self.graph:
            self.detach()
        nodes = [graph.V[self.key_1], graph.V[self.key_2]]
        for node in nodes:
            if self not in node.edges:
                node.edges += self
        self._graph = graph
        self._graph.E[self.key] = self

    def detach(self):
        assert(self._graph)
        if self.graph:
            for node in self._nodes:
                if self in node.edges:
                    node.edges.remove(self)
            self.graph.E.pop(self.key)
            self.graph = None

    def __contains__(self, obj: Union[Node, NodeKey]):
        if type(obj) == Node: obj = obj.key
        return obj in self.nodes

    @property
    def capacity(self):
        return self._capacity

    @property
    def key_1(self):
        return self._key_1

    @property
    def key_2(self):
        return self._key_2

    @property
    def nodes(self):
        return [self.key_1, self.key_2]