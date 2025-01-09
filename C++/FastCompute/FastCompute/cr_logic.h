#pragma once
#ifndef GAME_LOGIC_AND_SORT_H
#define GAME_LOGIC_AND_SORT_H


extern "C" {
    __declspec(dllexport) void check_collision(
        float x, float y, float other_x, float other_y, float prev_x, float prev_y,
        float min_distance, float* new_x, float* new_y
    );

    __declspec(dllexport) bool is_finish_line(float x, float y);

    __declspec(dllexport) void update_checkpoints(
        float x, float y, bool checkpoints[5]
    );

    __declspec(dllexport) void determine_enemy_keys(
        float x, float y,
        bool* key_w, bool* key_a, bool* key_s, bool* key_d
    );

    __declspec(dllexport) bool is_slipping_terrain(float x, float y);

    __declspec(dllexport) bool is_non_slipping_terrain(float x, float y);

}

#endif