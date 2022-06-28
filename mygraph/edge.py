

from .base_types import *
from .node import GraphVertex

class GraphEdge(GraphObject):

    __counter = 0

    def __init__(self, source:GraphVertex, target:GraphVertex, **extras):
        super().__init__(extras=extras)
        assert(source is not None and target is not None)
        assert(type(source)==GraphVertex and type(target)==GraphVertex)
        self._source = source
        self._target = target

    def _validate_extras(self):
        pass
    
    def __eq__(self, other):
        return (type(self)==type(other)) \
                and (self._source == other._source) \
                and (self._target == other._target)

    def __hash__(self):
        return hash(hash(self._source),hash(self._target))

    def __str__(self):
        return f"({str(self._source)},{str(self._target)})"
    
    def copy(self):
        return GraphEdge(self._source.copy(), self._target.copy(), self.extras)

    def __contains__(self, obj: GraphVertex):
        return obj in self.vertices

    def invert(self):
        tmp = self._source
        self._source = self._target
        self._target = tmp
        return self

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def vertices(self):
        return (self.source, self.target)
    
    @property
    def capacity(self):
        return self['capacity']

    @property
    def weight(self):
        return self['weight']

    @property
    def flow(self):
        return self['flow']

    @capacity.setter
    def capacity(self, value):
        self['capacity'] = value

    @weight.setter
    def weight(self, value):
        self['weight'] = value

    @flow.setter
    def flow(self, value):
        self['flow'] = value