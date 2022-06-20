
from typing import List, Tuple, FrozenSet, Union, Dict
from collections.abc import Iterable

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
    def attach(self, graph):
        raise NotImplementedError()
    def detach(self):
        raise NotImplementedError()
    @property
    def key(self):
        raise NotImplementedError()

class NodeKey(BaseKey):
	@property
	def __eq__(self, other):
		return issubclass(type(other), NodeKey) and (self._value == other._value)
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
		return issubclass(type(other), EdgeKey) and (self._value == other._value)
	def __hash__(self):
		return hash(hash(self._value[0]), hash(self._value[1]))
class Graph: pass