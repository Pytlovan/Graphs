import time
import timeit
from enum import Enum
import numpy as np
import random

class KnightTour:
    def __init__(self, size=8):
        self.size = size
        self.board = [[-1 for _ in range(size)] for _ in range(size)]  # Inicializa o tabuleiro com -1
        self.moves_x = [-2, -1, 1, 2, 2, 1, -1, -2]  # Movimentos possíveis em X
        self.moves_y = [-1, -2, -2, -1, 1, 2, 2, 1]  # Movimentos possíveis em Y
        self.steps = 1

    def reset(self):
        """Reinicia o tabuleiro."""
        self.board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self.steps = 1
        
    def is_valid_move(self, x, y):
        """Verifica se um movimento é válido (dentro dos limites e não visitado)."""
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == -1

    def solve(self, start_x, start_y, pb = True, time_start = time.time()):
        """Inicia a solução do problema do cavalo."""
        self.reset()
        self.board[start_x][start_y] = 1  # Define a posição inicial como 1

        if not self.solve_knight_tour(start_x, start_y, 1, time_start):
            print("Solução não encontrada.")
            return False
        else:
            if pb:
                self.print_board()
            return True
        
    def print_board(self):
        """Imprime o tabuleiro com o caminho do cavalo."""
        for row in self.board:
            print(" ".join(f"{num:3}" for num in row))
        print(f"Steps: {self.steps}\n")


class HeatMap(KnightTour):
    def __init__(self, size=8, tol = 1e5):
        super().__init__(size)
        self.heatmap = self.generate_heatmap()  # Gera a heatmap na inicialização
        self.tol = tol

    def heatmap_function(self, fn):
        if fn == "ln":
            self.heatmap = self.generate_heatmap("ln")
    
    def linear_heatmap(self, x, y):
        N = self.size
        center = (N-1)/2
        return 1/((abs(x-center) + abs(y-center))/center + 1e-5)

    def generate_heatmap(self, fn = "qd"):
        """Cria uma matriz de calor onde valores maiores indicam posições mais prioritárias."""
        N = self.size
        center = (N - 1) / 2
        heatmap = np.empty((N, N))
        
        for i in range(N):
            for j in range(N):
                if fn == "ln":
                    heatmap[i, j] = self.linear_heatmap(i, j)
                else:
                    distance = ((i - center)**2 + (j - center)**2) / (center**2)
                    value = 2 / (distance + 1e-5)  # Pequeno ajuste para evitar divisão por zero
                    heatmap[i, j] = value
        return heatmap
    
    

    def solve_knight_tour(self, x, y, move_count, time_start):
        """Função Recursiva principal"""
        if move_count == self.size * self.size:
            return True

        moves = []
        for i in range(8):
            next_x, next_y = x + self.moves_x[i], y + self.moves_y[i]
            if self.is_valid_move(next_x, next_y):
                priority = self.heatmap[next_x, next_y]
                moves.append((priority, next_x, next_y))

        moves.sort(reverse=False)

        for _, next_x, next_y in moves:
            self.board[next_x][next_y] = move_count + 1
            self.steps += 1

            if self.steps > self.tol: # 100 milhões de steps 
                return False
            
            if self.solve_knight_tour(next_x, next_y, move_count + 1, time_start):
                return True

            self.board[next_x][next_y] = -1

        return False

class BruteForce(KnightTour):
    def __init__(self, size=8, tol = 2e7):
        super().__init__(size)
        self.tolerance = tol

    def solve_knight_tour(self, x, y, move_count, time_start):
        """Tenta resolver o problema do cavalo usando backtracking."""
        # Se todas as casas foram visitadas, terminamos
        if move_count == self.size * self.size:
            return True

        # Tenta todos os 8 movimentos possíveis do cavalo
        for i in range(8):
            next_x = x + self.moves_x[i]
            next_y = y + self.moves_y[i]
            if self.is_valid_move(next_x, next_y):
                self.board[next_x][next_y] = move_count + 1  # Marca como visitado
                self.steps += 1
                
                if self.steps%(self.tolerance/1e2) == 0:
                    time_current = time.time()
                    elapsed_time = time_current - time_start
                    print(f"ElapsedTime: {elapsed_time:10.2f} s\t {int(self.steps/(self.tolerance/1e2)):6}% until fail")

                if self.steps > self.tolerance: # 100 milhões de steps 
                    return False
                
                if self.solve_knight_tour(next_x, next_y, move_count + 1, time_start):
                    return True  # Se encontrou solução, retorna True
                
                self.board[next_x][next_y] = -1

        return False  # Se nenhum movimento funcionou, retorna False

#------------------------------------------------------------
#Main

class KnightTourRunner:
    def __init__(self, size=8, n_iter=100, algorithm="smart", print_board=False, print_squares=False, tolerance=1e6):
        self.N = size
        self.N_ITER = n_iter  
        self.algorithm = algorithm.lower()  # Escolha entre "smart" ou "brute-force"
        self.PRINT_BOARD = print_board
        self.PRINT_SQUARES = print_squares
        
        self.Column = self.create_column_enum(self.N)
        
        self.bruteForce_knight = BruteForce(size=self.N)
        self.smart_knight = HeatMap(size=self.N)
        
        self.steps_list_smart_knight = []
        self.steps_list_brute_force = []
        self.times_list_smart_knight = []
        self.times_list_brute_force = []
        
        self.fail_count_smart_knight = 0
        self.perfect_conversions_count = 0

        self.smart_knight.tol = tolerance
        self.bruteForce_knight.tolerance = tolerance
    
    def create_column_enum(self, n):
        columns = {chr(65 + i): i for i in range(n)}
        return Enum('Column', columns)
    
    def run_smart_knight(self):
        Start_Square = f"{chr(random.randint(65, 65 + self.N - 1))}{random.randint(1, self.N)}"
        
        x = self.N - int(Start_Square[1])
        y = self.Column[Start_Square[0]].value
        
        if self.PRINT_SQUARES:
            print("Start Square: ", Start_Square)
        
        convergiu = self.smart_knight.solve(x, y, pb=self.PRINT_BOARD, time_start = time.time())
        
        if self.smart_knight.steps == self.N * self.N:
            self.perfect_conversions_count += 1
        
        self.times_list_smart_knight.append("")
        
        if not convergiu:
            self.fail_count_smart_knight += 1
        
        self.steps_list_smart_knight.append(self.smart_knight.steps)
    
    def run_brute_force_knight(self):
        Start_Square = "A1" # f"{chr(random.randint(65, 65 + self.N - 1))}{random.randint(1, self.N)}"
        x = self.N - int(Start_Square[1])
        y = self.Column[Start_Square[0]].value

        if self.PRINT_SQUARES:
            print("Start Square: ", Start_Square)
        
        convergiu = self.bruteForce_knight.solve(x, y, pb=self.PRINT_BOARD, time_start = time.time())

        if not convergiu:
            self.fail_count_smart_knight += 1
        
        self.steps_list_smart_knight.append(self.smart_knight.steps)
        self.steps_list_brute_force.append(self.bruteForce_knight.steps)
    
    def execute(self):
        if self.algorithm == "smart":
            exec_time = timeit.timeit(self.run_smart_knight, number=self.N_ITER)
            steps_list = self.steps_list_smart_knight
            fail_count = self.fail_count_smart_knight
            perfect_conversions = self.perfect_conversions_count
        elif self.algorithm == "brute-force":
            exec_time = timeit.timeit(self.run_brute_force_knight, number=self.N_ITER)
            steps_list = self.steps_list_brute_force
            fail_count = 0  # Brute-force always converges
            perfect_conversions = 0  # Brute-force does not use this metric
        else:
            print("Invalid algorithm selected. Choose 'smart' or 'brute-force'.")
            return
        
        exec_results = {
            "NExec": f"{len(steps_list):10}   ",
            "MaxSteps": f"{max(steps_list) if steps_list else 0:10} p.",
            "AvgSteps": f"{int(sum(steps_list) / len(steps_list)) if steps_list else 0:10} p.",
            "Time": f"{exec_time*1000:10.3f} ms",
            "AvgTime": f"{exec_time / len(steps_list)*1000 if steps_list else 0:10.3f} ms",
            "Failed": f"{fail_count:10}   ",
            "Clean_Conv": f"{perfect_conversions/len(steps_list)*100 if steps_list else 0:10.2f} %"

        
        }
        print()
        if self.N_ITER > 1:
            for key, value in exec_results.items():
                print(f"{key:10} {value}")
        else:
            print("Steps    :", f"{max(steps_list) if steps_list else 0:10} p.")
            print("Time     :", f"{exec_time*1000:10.3f} ms")
            
        print()
        

# Main
N = 8
N_ITER = 10
PRINT_BOARD = False
PRINT_SQUARES = False
TOLERANCE = 1e8

if __name__ == "__main__":
    ALGORITHM_CHOICE = input("Choose algorithm (smart/brute-force): ").strip().lower()

    if ALGORITHM_CHOICE == "brute-force":
        N_ITER = 1
        PRINT_BOARD = True
        PRINT_SQUARES = True
    elif N_ITER <= 10:
        PRINT_BOARD = True
        PRINT_SQUARES = True

    runner = KnightTourRunner(size=N, n_iter=N_ITER, algorithm=ALGORITHM_CHOICE, print_board=PRINT_BOARD, print_squares=PRINT_SQUARES, tolerance=TOLERANCE)
    runner.execute()