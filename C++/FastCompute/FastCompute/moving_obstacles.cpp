#include <cmath>

using namespace std;

extern "C" {

    __declspec(dllexport) void move_minecart(
        float* x, float* speed, int current_hits, int hits_required,
        float left_limit, float right_limit, bool* is_active
    ) {
        if (current_hits == 0) {
            if (*x >= right_limit) {
                *speed = -abs(*speed);
            }
            else if (*x <= left_limit) {
                *speed = abs(*speed);
            }
            *x += *speed;
        }
        if (current_hits >= hits_required) {
            *is_active = false;
        }
    }

    __declspec(dllexport) void move_tumbleweed(
        float* x, bool* moving, float speed, float starting_x,
        float left_limit, float right_limit
    ) {
        if (!*moving) {
            return;
        }

        if (*x >= right_limit && starting_x == left_limit) {
            *moving = false;
        }
        else if (*x <= left_limit && starting_x == right_limit) {
            *moving = false;
        }

        if (*moving) {
            *x += (starting_x == left_limit) ? speed : -speed;
        }
    }
}