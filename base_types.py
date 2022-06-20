
from typing import List, Tuple, FrozenSet, Union

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
		return issubclass(BaseKey, other) and (self.value == other.value)

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