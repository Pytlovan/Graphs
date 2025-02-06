import time
from enum import Enum
import numpy as np

class KnightTour:
    def __init__(self, size=8):
        self.size = size
        self.board = [[-1 for _ in range(size)] for _ in range(size)]  # Inicializa o tabuleiro com -1
        self.moves_x = [-2, -1, 1, 2, 2, 1, -1, -2]  # Movimentos possíveis em X
        self.moves_y = [-1, -2, -2, -1, 1, 2, 2, 1]  # Movimentos possíveis em Y
        self.steps = 1
        
    def is_valid_move(self, x, y):
        """Verifica se um movimento é válido (dentro dos limites e não visitado)."""
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == -1

    def solve(self, start_x, start_y):
        """Inicia a solução do problema do cavalo."""
        self.board[start_x][start_y] = 1  # Define a posição inicial como 1

        if not self.solve_knight_tour(start_x, start_y, 2):
            print("Solução não encontrada.")
            return False
        else:
            self.print_board()
            return True
        
    def print_board(self):
        """Imprime o tabuleiro com o caminho do cavalo."""
        for row in self.board:
            print(" ".join(f"{num:3}" for num in row))
        print(f"Passos: {self.steps}")


class HeatMap(KnightTour):
    def __init__(self, size=8):
        super().__init__(size)
        self.heatmap = self.generate_heatmap()  # Gera a heatmap na inicialização

    def generate_heatmap(self):
        """Cria uma matriz de calor onde valores maiores indicam posições mais prioritárias."""
        N = self.size
        center = (N - 1) / 2
        heatmap = np.zeros((N, N))
        
        for i in range(N):
            for j in range(N):
                distance = ((i - center)**2 + (j - center)**2) / (center**2)
                value = 2 / (distance + 1e-5)  # Pequeno ajuste para evitar divisão por zero
                heatmap[i, j] = value
        return heatmap

    def solve_knight_tour(self, x, y, move_count):
        """Tenta resolver o problema do cavalo usando backtracking, priorizando posições mais quentes da heatmap."""
        if move_count == self.size * self.size + 1:
            return True

        # Gera os movimentos possíveis e ordena pelo maior valor da heatmap
        moves = []
        for i in range(8):
            next_x, next_y = x + self.moves_x[i], y + self.moves_y[i]
            if self.is_valid_move(next_x, next_y):
                priority = self.heatmap[next_x, next_y]
                moves.append((priority, next_x, next_y))

        # Ordena por maior valor na heatmap (do maior para o menor)
        moves.sort(reverse=False)

        for _, next_x, next_y in moves:
            self.board[next_x][next_y] = move_count  # Marca como visitado
            self.steps += 1
            
            if self.solve_knight_tour(next_x, next_y, move_count + 1):
                return True  # Se encontrou solução, retorna True
            
            self.board[next_x][next_y] = -1  # Backtracking

        return False  # Nenhum movimento válido encontrado

class BruteForce(KnightTour):
    def __init__(self, size=8):
        super().__init__(size)

    def solve_knight_tour(self, x, y, move_count):
        """Tenta resolver o problema do cavalo usando backtracking."""
        # Se todas as casas foram visitadas, terminamos
        if move_count == self.size * self.size + 1:
            return True

        # Tenta todos os 8 movimentos possíveis do cavalo
        for i in range(self.size):
            next_x = x + self.moves_x[i]
            next_y = y + self.moves_y[i]
            if self.is_valid_move(next_x, next_y):
                self.board[next_x][next_y] = move_count  # Marca como visitado
                self.steps += 1
                
                if self.steps > 1e8: # 100 milhões de steps 
                    return False
                
                if self.solve_knight_tour(next_x, next_y, move_count + 1):
                    return True  # Se encontrou solução, retorna True
                
                self.board[next_x][next_y] = -1

        return False  # Se nenhum movimento funcionou, retorna False

#------------------------------------------------------------
#Main

def create_column_enum(n):
    columns = {chr(65 + i): i for i in range(n)} 
    return Enum('Column', columns)

N = 8

Column = create_column_enum(N)

Start_Square = "D4"

x = N - int(Start_Square[1])
y = Column[Start_Square[0]].value

# Creates a KnightProblem object with the size of the board

bruteForce_knight = BruteForce(size = N)
smart_knight = HeatMap(size = N)

start_time = time.time()

smart_knight.solve(x, y)

end_time = time.time()

# Prints the number of steps
print("\nResult of Knight Problem\nIntelligent Path \n")
print(f"Time: {end_time - start_time:.6f}s")
print(f"Number of steps: {smart_knight.steps}")
print("\n")
# print(execution_time)

start_time2 = time.time()

bruteForce_knight.solve(x, y)

end_time2 = time.time()

print("\nResult of Knight Problem\nBacktracking Path\n")
print(f"Time: {end_time2 - start_time2:.6f}s")
print(f"Number of steps: {bruteForce_knight.steps}")
print("\n")