
from curses import A_ALTCHARSET
from base_types import *
from node import *
from edge import *


class DirectedGraph:

	def __init__(self, V=None, E=None):
		if (not V) and (not E):
			self.V = {}
			self.E = {}
		elif (type(V) == List[Node]) and (type(E) == List[Edge]):
			self.V = V
			self.E = E
		else:
			raise Exception("Not supported")

	def __add__(self, other):
		if issubclass(GraphObject, other):
			other.attach(self)
		elif issubclass(BaseKey, other):
			node_key = other
			node = Node(key=node_key, edges=[])
			self += node
		elif (type(other) in [List, Tuple]) and (len(other) in [2,3]) \
				and (issubclass(BaseKey, other[0]) and issubclass(BaseKey, other[1]) \
				and ( (len(other) == 2) or (type(other[2]) in [int,float])) ):
			node_key_1 = other[0] if issubclass(BaseKey, other[0]) else NodeKey(value=other[0])
			node_key_2 = other[1] if issubclass(BaseKey, other[1]) else NodeKey(value=other[1])
			capacity   = None     if (len(other) == 2)             else other[2]
			edge = Edge(node_key_1, node_key_2, capacity)
			self += edge
		else:
			raise ValueError("Unrecognized type")
	
	def __sub__(self, other):
		if issubclass(GraphObject, other):
			other.detach(self)
		else:
			other = self[other]
			self -= other
			
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