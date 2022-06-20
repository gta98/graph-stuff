

from base_types import *
from node import Node

class Edge(GraphObject):

    def __init__(self, obj_1: Union[Node, NodeKey], obj_2: Union[Node, NodeKey]):
        if type(obj_1) == Node: obj_1 = obj_1.key
        if type(obj_2) == Node: obj_2 = obj_2.key
        assert((type(obj_1) == NodeKey) and (type(obj_2) == NodeKey))
        self._key_1 = obj_1
        self._key_2 = obj_2
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
        return EdgeKey((self.key_1, self.key_2))
    
    def attach(self, graph):
        assert(self._graph is None)
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
        if not self._graph:
            return None
        return self._graph.C[self.key]
    
    @property
    def capacity(self, value):
        assert(self._graph)
        self._graph.C[self.key] = value

    @property
    def key_1(self):
        return self._key_1

    @property
    def key_2(self):
        return self._key_2

    @property
    def nodes(self):
        return [self.key_1, self.key_2]