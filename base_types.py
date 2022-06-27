
from typing import List, Tuple, FrozenSet, Union, Dict
from itertools import chain
from collections.abc import Iterable
from enum import Enum

infinity = float('inf')

class Color(Enum):
	WHITE = 0
	GRAY = 1
	BLACK = 2

WHITE = Color.WHITE
GRAY = Color.GRAY
BLACK = Color.BLACK

class BaseKey:
	_count = 0
	def __init__(self, value=None):
		self._value = value or self._count
		BaseKey._count += 1
	@property
	def value(self):
		return self._value
	@property
	def value(self, _):
		raise ValueError("Cannot set property: BaseKey.value")
	@property
	def __eq__(self, other):
		return issubclass(type(other), BaseKey) and (self._value == other._value)
	@property
	def __key(self):
		return self
	@property
	def key(self):
		return self

class GraphObject:
    def __init__(self):
        raise NotImplementedError()
    @property
    def key(self):
        raise NotImplementedError()
    @property
    def graph(self):
        raise NotImplementedError()
    @graph.setter
    def graph(self, value):
        raise NotImplementedError()


class GraphObjectMapper:
	def __init__(self, graph, d: Dict):
		self._d = d
		self._graph = graph
		self._d = dict()
		for key in d.keys():
			new_key = graph[key]
			assert(new_key)
			self._d[new_key] = d[key]
	def __getitem__(self, key):
		return self._d.get(self._graph[key], None)
	def __setitem__(self, key, value):
		self._d[self._graph[key]] = value
	def __call__(self, key):
		return self[key]

class EdgeMapper(GraphObjectMapper):
	def __call__(self, node_1, node_2):
		return self[(node_1,node_2)]

class NodeKey(BaseKey):
	@property
	def __eq__(self, other):
		return (type(other) == NodeKey) and (self._value == other._value)
	def __hash__(self):
		return hash(self._value)
class EdgeKey(BaseKey):
	def __init__(self, value:Tuple[NodeKey,NodeKey]):
		try:
			assert(len(value)==2)
			assert(value[0] == NodeKey)
			assert(value[1] == NodeKey)
			self._value = (value[0], value[1])
		except:
			raise ValueError("Can only init EdgeKey with two NodeKey's")
	@property
	def __eq__(self, other):
		return (type(other) == EdgeKey) and (self._value == other._value)
	def __hash__(self):
		return hash(hash(self._value[0]), hash(self._value[1]))
class Graph: pass