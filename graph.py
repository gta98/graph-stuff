
from base_types import *
from node import *
from edge import *


class Graph:
	def __init__(self, directed, V:Iterable = None, E:Iterable = None, C:Dict = {}):
		if type(self) == Graph:
			raise Exception("Cannot initialize Graph directly")
		self.directed = directed
		assert(type(V) in [dict, Iterable, list, List, FrozenSet, set, Tuple])
		assert(type(E) in [dict, Iterable, list, List, FrozenSet, set, Tuple])
		assert((C is None) or (type(C) in [dict]))
		if type(V) == dict:
			self.V = V
		else:
			self.V = {}
			for node in V:
				if type(node) not in (Node, NodeKey):
					node = NodeKey(node)
				self + node
		if type(E) == dict:
			self.E = E
		else:
			self.E = {}
			for edge in E:
				self + edge
		if C:
			self._C = C
		else:
			self._C = {}


	def __add__(self, other):
		if issubclass(type(other), GraphObject):
			other.attach(self)
		elif issubclass(type(other), NodeKey):
			node_key = other
			node = Node(key=node_key, edges=[])
			self + node
		elif issubclass(type(other), EdgeKey):
			edge_key = other
			edge = Edge(obj_1=edge_key.value[0], obj_2=edge_key.value[1])
			self + edge
		elif (type(other) in [List, Tuple, list, tuple]) and (len(other) in [2]):
			node_key_1 = other[0] if issubclass(type(other[0]), NodeKey) else NodeKey(value=other[0])
			node_key_2 = other[1] if issubclass(type(other[1]), NodeKey) else NodeKey(value=other[1])
			edge = Edge(node_key_1, node_key_2)
			self + edge
		else:
			raise ValueError("Unrecognized type")
	
	def __sub__(self, other):
		if issubclass(type(other), GraphObject):
			other.detach(self)
		else:
			other = self[other]
			self - other
			
	def __getitem__(self, other):
		if type(other) == NodeKey:
			return self.V.get(other, None)
		elif type(other) == EdgeKey:
			return self.E.get(other, None)
		elif (type(other) in [List, Tuple]) and (len(other) == 2):
			(node_1, node_2) = (self[other[0]], self[other[1]])
			if node_1 and node_2:
				return self[EdgeKey(value=(node_1.key, node_2.key))]
			else:
				return None
		else:
			try_node = self[NodeKey(value=other)]
			try_edge = self[EdgeKey(value=other)]
			if try_node and not try_edge:
				return try_node
			elif try_edge and not try_node:
				return try_edge
			else:
				raise ValueError("Unrecognized key")
	
	def __contains__(self, other):
		other = self[other]
		return other is not None
	
	@property
	def C(self):
		return self._C

	@property
	def C(self, update: Dict):
		for edge, capacity in update:
			edge = self[edge]
			assert(edge)
			edge.capacity = capacity


class DirectedGraph(Graph):
	def __init__(self, V:Iterable = None, E:Iterable = None, C:Dict = None):
		Graph.__init__(self, True, V, E, C)

class UndirectedGraph(Graph):
	def __init__(self, V:Iterable = None, E:Iterable = None, C:Dict = None):
		Graph.__init__(self, False, V, E, C)
