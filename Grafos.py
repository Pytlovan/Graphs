import numpy as np
from tkinter import *

class Graph:
    def __init__(self, graph = None, directed = False):
        if graph is None:
            graph = {}
        self.graph = graph
        self.directed = directed
    
    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []
            return f"Vertex {v} Added"
        return "Vertex Already in Graph"
    
    def add_edge(self, u, v):
        msg = ''
        if u not in self.graph:
            self.add_vertex(u)
            msg += f"\nVertex {u} Added"
        if v not in self.graph:
            self.add_vertex(v)
            msg += f"\nVertex {v} Added"
        if v not in self.graph[u]:
            self.graph[u].append(v)
            if not self.directed:
                if u not in self.graph[v]:
                    self.graph[v].append(u)
                    return f"Edges {u}-{v} and {v}-{u} Added"+msg
            return f"Edge {u}-{v} Added"+msg
        return "Edge Already in Graph"
        
    def remove_vertex(self, v):
        if v not in self.graph.keys():
            return "Invalid Vertex"
        for i in self.graph[v]:
            if v in self.graph[i]:
                self.graph[i].remove(v)
        del self.graph[v]
        return f"Vertex {v} Removed"
    
    def remove_edge(self, u, v):
        if u in self.graph and v in self.graph[u]:
            self.graph[u].remove(v)
            if not self.directed:
                self.graph[v].remove(u)
                return f"Edges {u}-{v} and {v}-{u} Removed"
            return f"Edge {u}-{v} Removed"
        return "Edge(s) not connected!"

    def show_size(self):
        vertices = sorted(self.graph.keys())
        size = len(vertices)
        return size
    
    def adjacency_matrix(self):
        vertices = sorted(self.graph.keys())
        size = len(vertices)
        index_map = {vertices[i]: i for i in range(size)}
        matrix = np.zeros((len(vertices), len(vertices)), dtype = int)
        for v, neighbors in self.graph.items():
            for neighbor in neighbors:
                i, j = index_map[v], index_map[neighbor]
                matrix[i][j] = 1
        return matrix

    def print_matrix(self):
        matrix = self.adjacency_matrix()
        size = len(matrix)
        for i in range(size):
            line = "|"
            for j in range(size):
                line += f' {matrix[i][j]} '
            line += "|"
            print(line)

    def bfs(self, start, search = None):
        vertices = sorted(self.graph.keys())
        if start not in vertices:
            return
        if search is not None and search not in vertices:
            return
        visited = set()
        queue = [start]
        result = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                if search is not None and vertex == search:
                    break

                for v in self.graph[vertex]:
                    if v not in visited:
                        queue.append(v)

        for vertex in vertices:
            if vertex not in visited:
                result.append(vertex)
        
        return result
    
    def dfs(self, start, search = None):
        vertices = sorted(self.graph.keys())
        if start not in vertices:
            return
        if search is not None and search not in vertices:
            return
        visited = set()
        stack = [start]
        result = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                if search is not None and vertex == search:
                    break
                
                for v in reversed(self.graph[vertex]):
                    if v not in visited:
                        stack.append(v)

        for vertex in vertices:
            if vertex not in visited:
                result.append(vertex)
        
        return result

    def ftd(self, start):
        vertices = sorted(self.graph.keys())
        if start not in vertices:
            return "Invalid Vertex"
        visited = set()
        levels = {}
        queue = [start]
        levels[start] = 0

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                
                for v in self.graph[vertex]:
                    if v not in visited:
                        queue.append(v)
                        if v not in levels.keys():
                            levels[v] = levels[vertex] + 1

        for vertex in vertices:
            if vertex not in visited:
                levels[vertex] = -1

        return visited, {k: levels[k] for k in sorted(levels)}
    
    def fti(self, end):
        vertices = sorted(self.graph.keys())
        if end not in vertices:
            return "Invalid Vertex"
        
        # Inversão do grafo (chaves viram dados/dados viram chaves)
        igraph = {v: [] for v in self.graph} 
        for vertex in self.graph:
            for adjacent in self.graph[vertex]:
                igraph[adjacent].append(vertex)
        
        visited = set()
        levels = {}
        queue = [end]
        levels[end] = 0

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)

                for v in igraph[vertex]:
                    if v not in visited:
                        queue.append(v)
                        if v not in levels.keys():
                            levels[v] = levels[vertex] + 1
        
        for vertex in vertices:
            if vertex not in visited:
                levels[vertex] = -1
        
        return visited, {k: levels[k] for k in sorted(levels)}
    
    def connectivity(self, start):
        vertices = set(self.graph.keys())
        fw = self.ftd(start)[0]
        bw = self.fti(start)[0]
        return fw.intersection(bw), True if fw.intersection(bw) == vertices else False
        
    def find_all_subgraphs(self, start):
        vertices = set(self.graph.keys())
        visited = set()
        subgraphs = []
        
        subgraphs.append(self.connectivity(start)[0])
        visited.update(self.connectivity(start)[0])
        if self.connectivity(start)[1] == False:
            for vertex in vertices:
                if vertex not in visited:
                    subgraphs.append(self.connectivity(vertex)[0])
                    visited.update(self.connectivity(vertex)[0])
        return subgraphs

'''
g = Graph(directed=False)
g.add_edge('C', 'D')
g.add_edge('A', 'B')
g.add_edge('D', 'F')
g.add_edge('E', 'F')
print(g.ftd('A'))
print(g.fti('A'))
print(g.dfs('A'))
print(g.dfs('F'))
print(g.connectivity('A')[1])
print(g.find_all_subgraphs('A'))
'''