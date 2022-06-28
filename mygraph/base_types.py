
from typing import Counter, List, Tuple, FrozenSet, Union, Dict
from itertools import chain
from collections.abc import Iterable
from abc import abstractproperty, abstractmethod

class GraphObject:
	NONE = None
	__counter = 0
	def __init__(self, extras=None, uid=None):
		self._extras = extras or dict()
		self._validate_extras()
		self._uid = uid or GraphObject.__counter
		GraphObject.__counter += 1
	def __getitem__(self, key):
		return self._extras.get(key, GraphObject.NONE)
	def __setitem__(self, key, value):
		self.extras[key] = value
		self._validate_extras()
	@abstractmethod
	def _validate_extras(self):
		raise NotImplementedError()
	@abstractmethod
	def __eq__(self):
		raise NotImplementedError()
	@abstractmethod
	def __hash__(self):
		raise NotImplementedError()
	@abstractmethod
	def __str__(self):
		raise NotImplementedError()
	@abstractmethod
	def copy(self):
		raise NotImplementedError()
	@abstractproperty
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