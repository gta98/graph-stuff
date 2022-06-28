
from typing import List, Tuple, FrozenSet, Union, Dict
from itertools import chain
from collections.abc import Iterable

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

class Graph: pass