#include "KnightTour.h"  // Assumindo que as classes BruteForce e HeatMap estão nesse arquivo
#include <numeric>

using namespace std;

class KnightTourRunner {
private:
    int N;
    int N_ITER;
    string algorithm;
    bool PRINT_BOARD;
    bool PRINT_SQUARES;
    double tolerance;

    BruteForce bruteForce_knight;
    HeatMap smart_knight;

    vector<int> steps_list_smart_knight;
    vector<int> steps_list_brute_force;
    vector<double> times_list_smart_knight;
    vector<double> times_list_brute_force;

    int fail_count_smart_knight;
    int perfect_conversions_count;

public:
    KnightTourRunner(int size = 8, int n_iter = 100, string algo = "smart", bool print_board = false, bool print_squares = false, double tol = 1e6)
        : N(size), N_ITER(n_iter), algorithm(algo), PRINT_BOARD(print_board), PRINT_SQUARES(print_squares), tolerance(tol),
          bruteForce_knight(size), smart_knight(size, tol), fail_count_smart_knight(0), perfect_conversions_count(0) {}

     pair<int, int> get_random_start_square() {
        // Usar o tempo atual como semente
        unsigned seed = chrono::system_clock::now().time_since_epoch().count();
        mt19937 gen(seed);
        uniform_int_distribution<> dis(0, N - 1);

        int x = dis(gen);
        int y = dis(gen);

        return {x, y};
     }

    void run_smart_knight() {
        auto [x, y] = get_random_start_square();

        if (PRINT_SQUARES) {
            cout << "Start Square: " << char('A' + y) << (N - x) << endl;
        }

        auto start_time = chrono::high_resolution_clock::now();
        bool convergiu = smart_knight.solve(x, y, PRINT_BOARD);
        auto end_time = chrono::high_resolution_clock::now();
        double elapsed_time = chrono::duration<double, milli>(end_time - start_time).count();

        if (smart_knight.get_steps() == N * N) {
            perfect_conversions_count++;
        }
        if (!convergiu) {
            fail_count_smart_knight++;
        }

        steps_list_smart_knight.push_back(smart_knight.get_steps());
        times_list_smart_knight.push_back(elapsed_time);
    }

    void run_brute_force_knight() {
        auto [x, y] = get_random_start_square();

        if (PRINT_SQUARES) {
            cout << "Start Square: " << char('A' + y) << (N - x) << endl;
        }

        auto start_time = chrono::high_resolution_clock::now();
        bruteForce_knight.solve(x, y, PRINT_BOARD);
        auto end_time = chrono::high_resolution_clock::now();
        double elapsed_time = chrono::duration<double, milli>(end_time - start_time).count();

        steps_list_brute_force.push_back(bruteForce_knight.get_steps());
        times_list_brute_force.push_back(elapsed_time);
    }

    void execute() {
        vector<int> *steps_list;
        int fail_count = 0;
        int perfect_conversions = 0;
        double exec_time;

        if (algorithm == "smart") {
            auto start_time = chrono::high_resolution_clock::now();
            for (int i = 0; i < N_ITER; i++) {
                run_smart_knight();
            }
            auto end_time = chrono::high_resolution_clock::now();
            exec_time = chrono::duration<double, milli>(end_time - start_time).count();
            steps_list = &steps_list_smart_knight;
            fail_count = fail_count_smart_knight;
            perfect_conversions = perfect_conversions_count;
        } else if (algorithm == "brute-force") {
            auto start_time = chrono::high_resolution_clock::now();
            for (int i = 0; i < N_ITER; i++) {
                run_brute_force_knight();
            }
            auto end_time = chrono::high_resolution_clock::now();
            exec_time = chrono::duration<double, milli>(end_time - start_time).count();
            steps_list = &steps_list_brute_force;
        } else {
            cout << "Invalid algorithm selected. Choose 'smart' or 'brute-force'." << endl;
            return;
        }

        int max_steps = steps_list->empty() ? 0 : *max_element(steps_list->begin(), steps_list->end());
        int avg_steps = steps_list->empty() ? 0 : accumulate(steps_list->begin(), steps_list->end(), 0) / steps_list->size();
        double avg_time = steps_list->empty() ? 0.0 : exec_time / steps_list->size();

        cout << endl;
        if (N_ITER > 1) {
            cout << "NExec        " << steps_list->size() << endl;
            cout << "MaxSteps     " << max_steps << " p." << endl;
            cout << "AvgSteps     " << avg_steps << " p." << endl;
            cout << "Time         " << exec_time << " ms" << endl;
            cout << "AvgTime      " << avg_time << " ms" << endl;
            cout << "Failed       " << fail_count << endl;
            cout << "Clean_Conv   " << (steps_list->empty() ? 0 : (perfect_conversions * 100.0 / steps_list->size())) << " %" << endl;
        } else {
            cout << "Steps    : " << max_steps << " p." << endl;
            cout << "Time     : " << exec_time << " ms" << endl;
        }
        cout << endl;
    }
};

int main() {
    int N = 8;
    int iter = 100;
    string algorithm = "brute-force";  // "brute-force" para testar força bruta
    bool print_board = false;
    bool print_squares = false;
    double tolerance = 1e6;

    if (algorithm == "brute-force" || iter == 1){
        iter = 1;
        print_board = true;
        print_squares = true;
    }
    else{
        iter = iter;
    }

    KnightTourRunner runner(N, iter, algorithm, print_board, print_squares, tolerance);
    runner.execute();

    return 0;
}
