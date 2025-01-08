#include <cmath>
#include <cstdlib>
#include <ctime>

using namespace std;

bool initialized = false;

extern "C" {

    __declspec(dllexport) void initialize_random() {
        if (!initialized) {
            srand(static_cast<unsigned>(time(nullptr)));
            initialized = true;
        }
    }

    __declspec(dllexport) int generate_random_canister_x(int y) {
        if (y >= 50 && y <= 300) {
            return rand() % (506 - 225 + 1) + 225;
        }
        else if (y > 300 && y <= 1500) {
            return rand() % (325 - 225 + 1) + 225;
        }
        else if (y > 1500 && y <= 2400) {
            return rand() % (506 - 225 + 1) + 225;
        }
        else {
            return rand() % (506 - 225 + 1) + 225;
        }
    }

    __declspec(dllexport) bool generate_random_coordinates(float probability, int* x, int* y) {
        if ((rand() / static_cast<float>(RAND_MAX)) < probability) {
            *y = rand() % (2400 - 301 + 1) + 301;
            if (*y > 300 && *y <= 1500) {
                *x = rand() % (325 - 225 + 1) + 225;
            }
            else if (*y > 1500 && *y <= 2400) {
                *x = rand() % (506 - 225 + 1) + 225;
            }
            return true;
        }
        return false;
    }

    __declspec(dllexport) int generate_specific_y(const int* choices, int size) {
        if (size <= 0) return -1;
        int index = rand() % size;
        return choices[index];
    }

    __declspec(dllexport) int generate_specific_x(const int* choices, int size) {
        if (size <= 0) return -1;
        int index = rand() % size;
        return choices[index];
    }

    __declspec(dllexport) int generate_random_x(int min_x = 180, int max_x = 570) {
        return rand() % (max_x - min_x + 1) + min_x;
    }

    __declspec(dllexport) int generate_random_y(int min_y = 50, int max_y = 2400) {
        return rand() % (max_y - min_y + 1) + min_y;
    }
}