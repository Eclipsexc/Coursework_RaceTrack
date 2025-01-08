#include <iostream>
#include <cmath>
#include <utility>

using namespace std;

extern "C" {

    __declspec(dllexport) void move_car(
        float* x, float* y, float speed, int* current_texture, bool keys[4]
    ) {
        if (keys[0]) {
            *y -= speed;
            *current_texture = 0;
        }
        if (keys[1]) {
            *x += speed;
            *current_texture = 1;
        }
        if (keys[2]) {
            *y += speed;
            *current_texture = 2;
        }
        if (keys[3]) {
            *x -= speed;
            *current_texture = 3;
        }
    }

    __declspec(dllexport) void boost_bolide(
        float* speed, float base_speed, float x, float y, float* last_x, float* last_y, bool single_key_pressed
    ) {
        if (single_key_pressed && (abs(x - *last_x) >= 300 || abs(y - *last_y) >= 300)) {
            *speed = min(*speed + 1.0f, 7.0f);
            *last_x = x;
            *last_y = y;
        }
        else if (!single_key_pressed) {
            *speed = base_speed;
        }
    }

    __declspec(dllexport) void use_nitro(
        float* speed, float base_speed, float* nitro_level, bool nitro_key_pressed
    ) {
        static bool is_nitro_active = false;

        if (nitro_key_pressed && *nitro_level > 0) {
            *speed = base_speed * 2;
            *nitro_level = max(0.0f, *nitro_level - 0.5f);
            is_nitro_active = true;
        }
        else if (is_nitro_active) {
            *speed = base_speed;
            is_nitro_active = false;
        }
    }

    __declspec(dllexport) void restore_nitro(float* nitro_level) {
        *nitro_level = 100.0f;
    }

    __declspec(dllexport) void slip_wheels(
        float* speed, float default_speed, bool is_good_on_dirt, bool* wheels_slipping
    ) {
        if (is_good_on_dirt) {
            *speed = default_speed * 0.875f;
        }
        else {
            *speed = default_speed * 0.4f;
        }
        *wheels_slipping = true;
    }

    __declspec(dllexport) void consume_fuel(
        float* fuel_level, float consumption_rate
    ) {
        if (*fuel_level > 0) {
            *fuel_level = max(0.0f, *fuel_level - consumption_rate);
        }
    }

    __declspec(dllexport) void consume_nitro(
        float* nitro_level, float consumption_rate
    ) {
        if (*nitro_level > 0) {
            *nitro_level = max(0.0f, *nitro_level - consumption_rate);
        }
    }

}