

from base_types import *
from node import Node

class Edge(GraphObject):

    def __init__(self, obj_1: Node, obj_2: Node):
        self._node_1 = obj_1
        self._node_2 = obj_2
        self._graph = None

    """
    def __init__(self, *args):
        if len(args) == 1:
            if type(args[0]) == Edge:
                edge = args[0]
                self._key_1 = edge._key_1
                self._key_2 = edge._key_2
                self._capacity = edge._capacity
                self._graph = edge._graph
                return
            elif type(args[0]) == EdgeKey:
                assert(len(args[0].value) == 2)
                self._key_1 = args[0].value[0]
                self._key_2 = args[0].value[1]
                self._capacity = None
                self._graph = None
                return
        elif len(args) == 2:
            obj_1, obj_2 = args[0], args[1]
            if type(obj_1) == Node: obj_1 = obj_1.key
            if type(obj_2) == Node: obj_2 = obj_2.key
            assert((type(obj_1) == NodeKey) and (type(obj_2) == NodeKey))
            Edge.__init__(self, EdgeKey(obj_1, obj_2))
        elif len(args) == 3:
            Edge.__init__(self, args[0], args[1])
            assert(type(args[2]) in [int,float])
            self._capacity = args[2]
        elif len(args) == 4:
            Edge.__init__(self, args[0], args[1], args[2])
            assert(issubclass(type(args[3]), Graph))
            self._graph = args[3]
        raise ValueError("Invalid input given to Edge.__init__")
    """

    @property
    def key(self):
        return (self.node_1, self.node_2)
    
    def attach(self, graph):
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

    def detach(self):
        assert(self._graph is not None)
        for node in self._nodes:
            if self in node.edges:
                node.edges.remove(self)
        self.graph.E.remove(self)
        self.graph = None
        del self

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