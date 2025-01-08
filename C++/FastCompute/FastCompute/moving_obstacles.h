#pragma once
#ifndef MOVING_OBSTACLES_H
#define MOVING_OBSTACLES_H

extern "C" {
    __declspec(dllexport) void move_minecart(
        float* x, float* speed, int current_hits, int hits_required,
        float left_limit, float right_limit, bool* is_active
    );

    __declspec(dllexport) void move_tumbleweed(
        float* x, bool* moving, float speed, float starting_x,
        float left_limit, float right_limit
    );
}

#endif