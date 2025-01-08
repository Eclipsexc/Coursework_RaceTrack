#include <cmath>

using namespace std;

extern "C" {

    __declspec(dllexport) void calculate_direction(
        float start_x, float start_y, float end_x, float end_y, float* dx, float* dy
    ) {
        float distance = sqrt((end_x - start_x) * (end_x - start_x) + (end_y - start_y) * (end_y - start_y));
        if (distance == 0.0f) {
            *dx = 0.0f;
            *dy = 0.0f;
        }
        else {
            *dx = (end_x - start_x) / distance;
            *dy = (end_y - start_y) / distance;
        }
    }

    __declspec(dllexport) void move_horizontal(
        float* x, float x_min, float x_max, bool* moving_right, int* animation_counter, int* current_texture
    ) {
        if (*moving_right && *x >= x_max) {
            *moving_right = false;
        }
        else if (!(*moving_right) && *x <= x_min) {
            *moving_right = true;
        }

        *x += *moving_right ? 1.0f : -1.0f;

        *animation_counter = (*animation_counter + 1) % 15;
        if (*animation_counter == 0) {
            *current_texture = (*current_texture + 1) % 3;
        }
    }

    __declspec(dllexport) void move_diagonal(
        float* x, float* y, float start_x, float start_y, float target_x, float target_y,
        bool* moving_to_target, float* dx, float* dy, float speed, bool* moving_right,
        int* animation_counter, int* current_texture
    ) {
        float previous_y = *y;

        if (*moving_to_target) {
            *x += *dx * speed;
            *y += *dy * speed;

            if (abs(*x - target_x) < speed && abs(*y - target_y) < speed) {
                *x = target_x;
                *y = target_y;
                *moving_to_target = false;
                calculate_direction(target_x, target_y, start_x, start_y, dx, dy);
            }
        }
        else {
            *x += *dx * speed;
            *y += *dy * speed;

            if (abs(*x - start_x) < speed && abs(*y - start_y) < speed) {
                *x = start_x;
                *y = start_y;
                *moving_to_target = true;
                calculate_direction(start_x, start_y, target_x, target_y, dx, dy);
            }
        }

        *moving_right = (*y > previous_y);

        *animation_counter = (*animation_counter + 1) % 15;
        if (*animation_counter == 0) {
            *current_texture = (*current_texture + 1) % 3;
        }
    }
}