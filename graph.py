
from base_types import *
from node import *
from edge import *


class Graph:
	_V, _E, _C, _W = None, None, None, None
	def __init__(self, V:Iterable = None, E:Iterable = None, C:Dict = {}, F:Dict = {}, W:Dict = {}):
		if type(self) == Graph:
			raise Exception("Cannot initialize Graph directly")
		self.undirected = True if (type(self) == UndirectedGraph) else False
		assert(type(V) in [type(None), set])
		assert(type(E) in [type(None), set])
		assert(type(C) in [type(None), dict])
		assert(type(W) in [type(None), dict])
		V = V or set()
		E = E or set()
		self._V = set()
		for node in V:
			self += node
		for edge in E:
			self += edge
		self._C = C or dict()
		self._W = W or dict()
		self._F = F or dict()


	def __add__(self, other):
		if issubclass(type(other), GraphObject):
			other.attach(self)
		elif (type(other) in [List, Tuple, list, tuple]) and (len(other) in [2]):
			node_1 = other[0] if (type(other[0]) == Node) else Node(key=other[0])
			node_2 = other[1] if (type(other[1]) == Node) else Node(key=other[1])
			edge = Edge(node_1, node_2)
			self += edge
		else:
			#raise ValueError("Unrecognized type")
			self += Node(key=other)
		return self
	
	def __sub__(self, other):
		if issubclass(type(other), GraphObject):
			other.detach(self)
		else:
			other = self[other]
			self -= other
		return self
			
	def __getitem__(self, other):
		if type(other) == Node:
			for node in self.V:
				if node._key == other._key:
					return node
			return None
		elif type(other) == Edge:
			node_1 = self[other.node_1]
			node_2 = self[other.node_2]
			if (not node_1) or (not node_2): return None
			for edge in self.E:
				if (edge.node_1 == node_1) and (edge.node_2 == node_2):
					return edge
			return Edge(node_1, node_2)
		elif (type(other) in [list, tuple]) and (len(other) == 2):
			return self[Edge(other[0], other[1])]
		else:
			return self[Node(key=other)]
	
	def copy(self):
		if type(self) == DirectedGraph: G = DirectedGraph([], [], {}, {})
		elif type(self) == UndirectedGraph: G = UndirectedGraph([], [], {}, {})
		else: raise Exception("Unrecognized type " + str(type(self)))
		for node in self._V:
			G += node.copy()
		for edge in self._E:
			G += edge.copy()
		for edge, value in self._C._d.items():
			G.C[edge] = value
		for edge, value in self._W._d.items():
			G.W[edge] = value
		for edge, value in self._F._d.items():
			G.F[edge] = value

	def __contains__(self, other):
		try: return self[other] is not None
		except: pass
		return False
	
	@property
	def V(self):
		return self._V
	
	@property
	def E(self):
		for node in self.V:
			for edge in node.edges:
				yield edge
	
	@E.setter
	def E(self, edges):
		for node in self.V:
			node.edges.clear()
		for edge in edges:
			self += edge
	
	@property
	def C(self):
		return self._C

	@C.setter
	def C(self, update: Dict):
		self._C = GraphObjectMapper(self, update)
	
	@property
	def W(self):
		return self._W

	@W.setter
	def W(self, update: Dict):
		self._W = GraphObjectMapper(self, update)
	
	@property
	def F(self):
		return self._F

	@W.setter
	def F(self, update: Dict):
		self._F = GraphObjectMapper(self, update)


class DirectedGraph(Graph): pass

class UndirectedGraph(Graph):
	def __init__(self, V:Iterable = None, E:Iterable = None, C:Dict = None):
		Graph.__init__(self, V, E, C)
