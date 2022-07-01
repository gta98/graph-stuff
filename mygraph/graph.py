
from .base_types import *
from .vertex import *
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
	
	def add_vertex(self, key_or_vertex, **kwargs):
		"""
		Usage Options:
		Add vertex as-is: add_vertex(GraphVertex)
		Initialize and add vertex: add_vertex([key], OPTIONAL: extra_1=value_1, extra_2=value_2, ...)
		"""
		if (type(key_or_vertex) == GraphVertex) and (not kwargs):
			vertex :GraphVertex = key_or_vertex
			if vertex in self:
				raise ValueError() # TODO
			self._V.add(vertex)
			self._E[vertex] = dict()
			return
		elif (type(key_or_vertex)==list) and (len(key_or_vertex)==1):
			wrapped_key = key_or_vertex
			key = wrapped_key[0]
			vertex = GraphVertex(key=key, **kwargs)
			return self.add_vertex(vertex)
		else:
			raise ValueError("Input formatting error") # TODO write informative message
	
	def add_edge(self, tuple_or_edge, **kwargs):
		"""
		Usage Options:
		Add edge as-is: add_edge(GraphEdge)
		Initialize and add edge: add_edge((v_or_[key]_1, v_or_[key]_2), OPTIONAL: extra_1=value_1, extra_2=value_2, ...)
		"""
		if (type(tuple_or_edge) == GraphEdge) and (not kwargs):
			edge :GraphEdge = tuple_or_edge
			if edge in self:
				raise ValueError()
			self._E[edge.source][edge.target] = edge
			self._E[edge.target][edge.source] = edge
			return
		elif (type(tuple_or_edge) ==tuple) and (len(tuple_or_edge)==2):
			source, target :GraphVertex = self[tuple_or_edge[0]], self[tuple_or_edge[0]]
			edge = GraphEdge(source, target)
			return self.add_edge(edge)
		else:
			raise ValueError("Input formatting error") # TODO write informative message

	def __parse_add(self, other):
		if not other:
			raise ValueError("Added object cannot be None")
		elif type(other) == GraphVertex:
			# G += vertex
			vertex :GraphVertex = other
			return vertex
		elif (type(other) == tuple) and (len(other) in {1,2}) and (type(other[0])==list) and (len(other[0])==1):
			# G += ([vertex_key], OPTIONAL: {'extra_1': value_1, ...})
			vertex_key = other[0][0]
			extras = dict() if (len(other)==1) else other[1]
			vertex = GraphVertex(vertex_key, **extras)
			return self.__parse_add( vertex )
		elif (type(other)==list) and (len(other)==1):
			# G += [vertex_key]
			vertex_key = other[0]
			return self.__parse_add( ([vertex_key],) )
		elif type(other) == GraphEdge:
			# G += edge
			edge :GraphEdge = other
			return edge
		elif (type(other)==tuple) and (len(other) in {1,2}) and (type(other[0])==tuple) \
				and implies(len(other)==2, type(other[1])==dict):
			# G += (([key_1], [key_2]), OPTIONAL: {'extra_1': value_1, ...})
			# G += (([key_1], vertex_2), OPTIONAL: {'extra_1': value_1, ...})
			# G += ((vertex_1, [key_2]), OPTIONAL: {'extra_1': value_1, ...})
			# G += ((vertex_1, vertex_2), OPTIONAL: {'extra_1': value_1, ...})
			raw_source, raw_target = other[0]
			extras = dict() if (len(other)==1) else other[1]
			source, target :GraphVertex = self.get(raw_source,None), self.get(raw_target,None)
			if source is None:
				raise ValueError(f"Graph: tried to generate edge, could not find source in {raw_source}")
			if target is None:
				raise ValueError(f"Graph: tried to generate edge, could not find target in {raw_target}")
			edge = GraphEdge(source, target, **extras)
			return self.__parse_add( edge )
		elif (type(other)==tuple) and (len(other) == 2) \
				and ((type(other[0]) == GraphVertex) or (type(other[0])==list and len(other[0])==1)) \
				and ((type(other[1]) == GraphVertex) or (type(other[1])==list and len(other[1])==1)) :
			# G += ([key_1], [key_2])
			# G += ([key_1], vertex_2)
			# G += (vertex_1, [key_2])
			# G += (vertex_1, vertex_2)
			source, target = other
			return self.__parse_add( ((source,target),) )
		else:
			raise TypeError()

	def __add__(self, other):
		try:
			other :GraphObject = self.__parse_add(other)
		except Exception as e:
			raise e
		if type(other) == GraphVertex:
			# G += vertex
			vertex :GraphVertex = other
			if vertex in self:
				raise ValueError() # TODO
			self._V[vertex.key] = vertex
			self._E[vertex.key] = dict()
			return self
		elif type(other) == GraphEdge:
			# G += edge
			edge :GraphEdge = other
			if edge in self:
				raise ValueError()
			if edge.source not in self or edge.target not in self:
				raise ValueError()
			self._E[edge.source.key][edge.target.key] = edge
			self._E[edge.target.key][edge.source.key] = edge
			return self
		else:
			raise AssertionError("This should not have happened")
	
	def __sub__(self, other):
		try:
			other :GraphObject = self.__parse_add(other)
		except Exception as e:
			raise e
		if type(other) == GraphVertex:
			# G -= vertex
			vertex :GraphVertex = other
			if vertex not in self:
				raise ValueError() # TODO
			assert(vertex in self._V)
			assert(vertex in self._E)
			self._V.pop(vertex)
			for neighbor in self._E[vertex]:
				self._E[neighbor].pop(vertex)
			self._E.pop(vertex)
			return self
		elif type(other) == GraphEdge:
			# G -= edge
			edge :GraphEdge = other
			if edge not in self:
				raise ValueError()
			if edge.source not in self or edge.target not in self:
				raise ValueError()
			self._E[edge.source.key].pop(edge.target.key)
			self._E[edge.target.key].pop(edge.source.key)
			return self
		else:
			raise AssertionError("This should not have happened")
	
	def get(self, other, default_value=None):
		if type(other) == GraphVertex:
			vertex = self.V.get(other.key, default_value)
			return vertex
		elif type(other) == GraphEdge:
			source, target = other.vertices
			return self.E.get(source.key, dict()).get(target.key, default_value)
		elif (type(other) == list) and (len(other)==1):
			vertex_key = other[0]
			return self.V.get(vertex_key, default_value)
		elif (type(other) in {list,tuple}) and (len(other)==2):
			source, target = other
			return self.E.get(source, dict()).get(target, default_value)
		else: # fallback - assume that this is a key
			vertex_key = other
			return self.get([vertex_key], default_value)
			
	def __getitem__(self, other):
		result = self.get(other, default_value=None)
		if result is None:
			raise ValueError(f"Invalid key: {other}")
		return result
	
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
		except: return False
	
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