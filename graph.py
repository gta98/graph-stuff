
from typing import List, Tuple

class Edge: pass
class Node: pass

class Edge:
	def __init__(self, node_1: Node, node_2: Node, capacity: int):
		self._node_1 = node_1
		self._node_2 = node_2
		self._capacity = capacity

	def __contains__(self, node: Node):
		return node in self.nodes
	@property
	def capacity(self):
		return self._capacity
	@property
	def nodes(self):
		return [self._node_1, self._node_2]
	@property
	def capacity(self, value):
		raise Exception("Do not modify Edge.capacity")

	@property
	def is_properly_attached(self):
		return (self in self.node_1.edges) and (self in self.node_2.edges)

	@property
	def is_properly_detached(self):
		return (self not in self.node_1.edges) and (self not in self.node_2.edges)

	def attach(self):
		assert(self.is_properly_detached)
		for node in self._nodes:
			if self not in node.edges:
				node.edges += self

	def detach(self):
		assert(self.is_properly_attached)
		for node in self._nodes:
			if self in node.edges:
				node.edges.remove(self)

class Node:
	_count = 0

	def __init__(self, name=None, edges=[]):
		self.name = name or self.__count
		self.edges = []
		Node._count += 1

	@property
	def count(self):
		return self._count

	@property
	def count(self, value):
		raise ValueError("Cannot set property: Node.count")

	def __rshift__(self, node: Node):
		edge = Edge(self, node, 0)

class DirectedGraph:
	def __init__(self, V, E):
		if (type(V) == List[Node]) and (type(E) == List[Edge]):
			self.V = V
			self.E = E
		else:
			raise Exception("Not supported")
	def __add__(self, other):
		if type(other) == Node:
			self.V.append(other)
		elif type(other) == Edge:
			edge = other
			assert(edge.node_1 in self.V)
			assert(edge.node_2 in self.V)
			self.E += edge
			edge.attach()
		elif type(other) == List[Node, Node]:
			self += (*other, 0)
		elif type(other) == List[Node, Node, int]:
			node_1, node_2, capacity = other
			self += Edge(node_1, node_2, capacity)