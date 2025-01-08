#pragma once
#ifndef PEDESTRIANS_H
#define PEDESTRIANS_H

extern "C" {

    __declspec(dllexport) void calculate_direction(
        float start_x, float start_y, float end_x, float end_y, float* dx, float* dy
    );

    __declspec(dllexport) void move_horizontal(
        float* x, float x_min, float x_max, bool* moving_right, int* animation_counter, int* current_texture
    );

    __declspec(dllexport) void move_diagonal(
        float* x, float* y, float start_x, float start_y, float target_x, float target_y,
        bool* moving_to_target, float* dx, float* dy, float speed, bool* moving_right,
        int* animation_counter, int* current_texture
    );

}

#endif