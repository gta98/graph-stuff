

from base_types import *
from node import Node

class Edge(GraphObject):

    def __init__(self, obj_1: Node, obj_2: Node):
        self._node_1 = obj_1
        self._node_2 = obj_2
        self._graph = None

    @property
    def key(self):
        return (self.node_1, self.node_2)
    
    @property
    def graph(self):
        try:
            return self._graph
        except:
            return None
    
    @graph.setter
    def graph(self, graph):
        if graph is not None:
            assert(self._graph is None)
            node_1, node_2 = graph[self.node_1], graph[self.node_2]
            if node_1 and node_2:
                if self._node_1._graph is None: del self._node_1
                if self._node_2._graph is None: del self._node_2
                self._node_1, self._node_2 = node_1, node_2
            else:
                raise Exception("Cannot attach edge with a nonexisting node")
            for node in [self._node_1, self._node_2]:
                assert(self not in node.edges)
                node.edges.add(self)
            self._graph = graph
        else:
            assert(self._graph is not None)
            for node in self._nodes:
                if self in node.edges:
                    node.edges.remove(self)
            self.graph.E.remove(self)
            self.graph = None
            del self
    
    @property
    def copy(self) -> GraphObject:
        return Edge(self.node_1, self.node_2)

    @property
    def inverse(self):
        edge = self.copy
        edge.invert()
        return edge

    def invert(self) -> None:
        tmp = self._node_1
        self._node_1 = self._node_2
        self._node_2 = tmp

    def __contains__(self, obj: Node):
        return obj in self.nodes

    def __eq__(self, other):
        return (self._node_1 == other._node_1) and (self._node_2 == other._node_2) \
            and (self.capacity == other.capacity) \
            and (self.weight == other.weight)
    
    def __hash__(self):
        return hash((*self.nodes, self.capacity, self.weight))
    
    def __str__(self):
        return f"({str(self._node_1)}, {str(self._node_2)})"
    
    def __iter__(self):
        yield self.node_1
        yield self.node_2

    @property
    def node_1(self):
        return self._node_1

    @property
    def node_2(self):
        return self._node_2

    @property
    def nodes(self):
        return [self.node_1, self.node_2]
    
    @property
    def capacity(self):
        if not self._graph:
            return None
        return self._graph.C[self]
    
    @capacity.setter
    def capacity(self, value):
        assert(self._graph)
        self._graph.C[self] = value

    @property
    def weight(self):
        if not self._graph:
            return None
        return self._graph.W[self]
    
    @weight.setter
    def weight(self, value):
        assert(self._graph)
        self._graph.W[self] = value
    
    @property
    def flow(self):
        if not self._graph:
            return None
        return self._graph.F[self]
    
    @flow.setter
    def flow(self, value):
        assert(self._graph)
        self._graph.F[self] = value