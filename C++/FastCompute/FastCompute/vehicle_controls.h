#pragma once
#ifndef VEHICLE_FUNCTIONS_H
#define VEHICLE_FUNCTIONS_H

extern "C" {

    __declspec(dllexport) void move_car(
        float* x, float* y, float speed, int* current_texture, bool keys[4]
    );

    __declspec(dllexport) void boost_bolide(
        float* speed, float base_speed, float x, float y, float* last_x, float* last_y, bool single_key_pressed
    );

    __declspec(dllexport) void use_nitro(
        float* speed, float base_speed, float* nitro_level, bool nitro_key_pressed
    );

    __declspec(dllexport) void restore_nitro(float* nitro_level);

    __declspec(dllexport) void slip_wheels(
        float* speed, float default_speed, bool is_good_on_dirt, bool* wheels_slipping
    );

    __declspec(dllexport) void consume_fuel(
        float* fuel_level, float consumption_rate
    );

    __declspec(dllexport) void consume_nitro(
        float* nitro_level, float consumption_rate
    );

}

#endif