
from .base_types import *
from .node import *
from .edge import *


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
		self._V = dict()
		self._E = dict()
		for node in V:
			self += node
		for edge in E:
			self += edge
	
	def add_vertex(self, vertex:GraphVertex):
		assert(vertex not in self._V)
		assert(vertex not in self._E)
		self._V.add(vertex)
		self._E[vertex] = dict()

	def add_edge(self, edge:GraphEdge):
		assert(edge.source in self and edge.target in self)
		self._E[edge.source][edge.target] = edge
		self._E[edge.target][edge.source] = edge

	def __add__(self, other):
		if issubclass(type(other), GraphVertex):
			self.add_vertex(other)
		elif issubclass(type(other), GraphEdge):
			self.add_edge(other)
		elif (type(other) in [List, Tuple, list, tuple]) and (len(other) in [2]):
			node_1 = other[0] if (type(other[0]) == GraphVertex) else GraphVertex(key=other[0])
			node_2 = other[1] if (type(other[1]) == GraphVertex) else GraphVertex(key=other[1])
			edge = GraphEdge(node_1, node_2)
			self += edge
		else:
			#raise ValueError("Unrecognized type")
			self += GraphVertex(key=other)
		return self
	
	def __sub__(self, other):
		if issubclass(type(other), GraphObject):
			other.detach(self)
		else:
			other = self[other]
			self -= other
		return self
			
	def __getitem__(self, other):
		if type(other) == GraphVertex:
			for node in self.V:
				if node._key == other._key:
					return node
			return None
		elif type(other) == GraphEdge:
			node_1 = self[other.node_1]
			node_2 = self[other.node_2]
			if (not node_1) or (not node_2): return None
			for edge in self.E:
				if (edge.node_1 == node_1) and (edge.node_2 == node_2):
					return edge
			return GraphEdge(node_1, node_2)
		elif (type(other) in [list, tuple]) and (len(other) == 2):
			return self[GraphEdge(other[0], other[1])]
		else:
			return self[GraphVertex(key=other)]
	
	def copy(self):
		G = None
		if type(self) == DirectedGraph: G = DirectedGraph([], [], {}, {})
		elif type(self) == UndirectedGraph: G = UndirectedGraph([], [], {}, {})
		else: raise Exception("Unrecognized type " + str(type(self)))
		for node in self._V:
			node_copy = GraphVertex(node.key, edges=[])
			node_copy.graph = G
		for edge in self._E:
			edge_copy = GraphEdge(edge.node_1, edge.node_2)
			edge_copy.graph = G
		for edge, value in self._C._d.items():
			G.C[edge] = value
		for edge, value in self._W._d.items():
			G.W[edge] = value
		for edge, value in self._F._d.items():
			G.F[edge] = value
		return G

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
		self._C = EdgeMapper(self, update)
	
	@property
	def W(self):
		return self._W

	@W.setter
	def W(self, update: Dict):
		self._W = EdgeMapper(self, update)
	
	@property
	def F(self):
		return self._F

	@W.setter
	def F(self, update: Dict):
		self._F = EdgeMapper(self, update)


class DirectedGraph(Graph): pass
class UndirectedGraph(Graph): pass