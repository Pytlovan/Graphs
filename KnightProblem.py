from Grafos import Graph
import copy

class Board:
    def __init__(self, size):
        self.size = size
        self.matrix = [["" for _ in range(self.size)] for _ in range(self.size)]
        self.connections = Graph

    def valid_jumps(self, x, y):
        connections = {}
        movements = {
            1: (x-2, y-1),
            2: (x-2, y+1),
            3: (x-1, y-2),
            4: (x-1, y+2),
            5: (x+1, y-2),
            6: (x+1, y+2),
            7: (x+2, y-1),
            8: (x+2, y+1)
        }
        for key, jump in movements.items():
            i = jump[0]
            j = jump[1]
            if i >= 0 and i < self.size and j >=0 and j < self.size:
                connections[f"{i}{j}"] = 1
        return connections

    # create_board_connections: 8n => O(n) where n = vertix count (size²) // ex: 64*8
    def create_board_connections(self):
        connections = {}
        for x in range(self.size):
            for y in range(self.size):
                connections[f"{x}{y}"] = self.valid_jumps(x, y)
        self.connections.graph = connections 

class KnightProblem:
    def __init__(self, size=8):
        self.board = Board(size)
        self.size = size
        self.board.create_board_connections() # 8n
        self.matrix = [["" for _ in range(self.size)] for _ in range(self.size)] # n
        
    # find_degrees: O(n) where n = vertix count (size²)
    def create_matrix(self):
        matrix = [["" for _ in range(self.size)] for _ in range(self.size)]
        degrees = self.board.connections.find_degrees(self.board.connections)
        for x in range(self.size):
            for y in range(self.size):
                matrix[x][y] = degrees[f"{x}{y}"]
        return matrix
    
    def create_map(self, start):
        matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
        order = self.intelligent_path(start)
        for key,value in order.items():
            x, y = int(key[0]), int(key[1])
            matrix[x][y] = value
        return matrix
    
    def print_matrix(self, start):
        self.matrix = self.create_map(start)
        for linha in self.matrix:
            print(linha)
    
    def save_board(self):
        self.board.connections.weighted = False
        self.board.connections.saveas_graph(self.board.connections)

    def find_lowest_move_degree(self, neighbours, board_state):
        degrees = self.board.connections.find_degrees(board_state)
        neighbours_size = {}

        for neighbour in neighbours:
            neighbours_size[neighbour] = degrees[neighbour]
        
        print(neighbours_size)
        valid_neighbours = [k for k in neighbours_size if neighbours_size[k] > 0]
        return min(valid_neighbours, key=neighbours_size.get) if valid_neighbours else None

    def intelligent_path(self, start):
        count = 1
        order = {}
        current_pos = start
        current_board_state = copy.deepcopy(self.board.connections)
        current_board_state.directed = False
        keep = True

        while(keep):
            neighbours = list(self.board.connections.graph[current_pos].keys())
            order[current_pos] = count
            for square, jumps in current_board_state.graph.items():
                if current_pos in jumps:
                    x = current_board_state.remove_edge(current_board_state, square, current_pos)
                    print(x)

            lowest_square_degree = self.find_lowest_move_degree(neighbours, current_board_state)
            print(lowest_square_degree)
            if lowest_square_degree:
                current_pos = lowest_square_degree
                count+=1
            else:
                keep = False
            
        return order
            
    


    
n = 10

knight = KnightProblem(size = n)
knight.print_matrix("43")