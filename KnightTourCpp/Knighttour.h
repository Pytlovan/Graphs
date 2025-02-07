#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <chrono>
#include <random>
#include <algorithm>

using namespace std;

class KnightTour {
protected:
    int size;
    vector<vector<int>> board;
    vector<int> moves_x;
    vector<int> moves_y;
    int steps;

public:
    KnightTour(int size = 8) : size(size), steps(1) {
        board.resize(size, vector<int>(size, -1));
        moves_x = {-2, -1, 1, 2, 2, 1, -1, -2};
        moves_y = {-1, -2, -2, -1, 1, 2, 2, 1};
    }

    void reset() {
        board.assign(size, vector<int>(size, -1));
        steps = 1;
    }

    bool is_valid_move(int x, int y) {
        return x >= 0 && x < size && y >= 0 && y < size && board[x][y] == -1;
    }

    bool solve(int start_x, int start_y, bool pb = true) {
        reset();
        board[start_x][start_y] = 1;

        if (!solve_knight_tour(start_x, start_y, 1)) {
            cout << "Solução não encontrada." << endl;
            return false;
        } else {
            if (pb) print_board();
            return true;
        }
    }

    void print_board() {
        for (const auto& row : board) {
            for (int num : row) {
                cout << num << " ";
            }
            cout << endl;
        }
        cout << "Steps: " << steps << endl;
    }


    virtual bool solve_knight_tour(int x, int y, int move_count) = 0;

    int get_steps() const { return steps; }
    void set_steps(int s) { steps = s; }
    int get_size() const { return size; }
    void set_size(int s) { size = s; reset(); }
};

class HeatMap : public KnightTour {
private:
    vector<vector<double>> heatmap;
    double tol;

public:
    HeatMap(int size = 8, double tol = 1e5) : KnightTour(size), tol(tol) {
        heatmap = generate_heatmap();
    }

    vector<vector<double>> generate_heatmap() {
        vector<vector<double>> heatmap(size, vector<double>(size));
        double center = (size - 1) / 2.0;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                double distance = ((i - center) * (i - center) + (j - center) * (j - center)) / (center * center);
                heatmap[i][j] = 2 / (distance + 1e-5);
            }
        }
        return heatmap;
    }

    bool solve_knight_tour(int x, int y, int move_count) override {
        if (move_count == size * size) return true;

        vector<pair<double, pair<int, int>>> moves;
        for (int i = 0; i < 8; i++) {
            int next_x = x + moves_x[i];
            int next_y = y + moves_y[i];
            if (is_valid_move(next_x, next_y)) {
                moves.push_back({heatmap[next_x][next_y], {next_x, next_y}});
            }
        }

        sort(moves.begin(), moves.end());

        for (auto& move : moves) {
            int next_x = move.second.first;
            int next_y = move.second.second;
            board[next_x][next_y] = move_count + 1;
            steps++;
            if (steps > tol) return false;
            if (solve_knight_tour(next_x, next_y, move_count + 1)) return true;
            board[next_x][next_y] = -1;
        }
        return false;
    }
};

class BruteForce : public KnightTour {
public:
    BruteForce(int size = 8) : KnightTour(size) {}

    bool solve_knight_tour(int x, int y, int move_count) override {
        if (move_count == size * size) return true;

        for (int i = 0; i < 8; i++) {
            int next_x = x + moves_x[i];
            int next_y = y + moves_y[i];
            if (is_valid_move(next_x, next_y)) {
                board[next_x][next_y] = move_count + 1;
                steps++;


                if (solve_knight_tour(next_x, next_y, move_count + 1)) return true;
                board[next_x][next_y] = -1;
            }
        }
        return false;
    }
};
