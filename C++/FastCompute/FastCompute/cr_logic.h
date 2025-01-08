#pragma once
#ifndef GAME_LOGIC_AND_SORT_H
#define GAME_LOGIC_AND_SORT_H

struct VehicleData {
    const char* name;
    int laps;
    int current_texture;
};

extern "C" {
    __declspec(dllexport) void check_collision(
        float x, float y, float other_x, float other_y, float prev_x, float prev_y,
        float min_distance, float* new_x, float* new_y
    );

    __declspec(dllexport) bool is_finish_line(float x, float y);

    __declspec(dllexport) void update_checkpoints(
        float x, float y, bool checkpoints[5]
    );

    __declspec(dllexport) const char* determine_leader(
        const bool player_checkpoints[5], const bool enemy_checkpoints[5],
        int player_laps, int enemy_laps, const char* previous_leader
    );

    __declspec(dllexport) void determine_enemy_keys(
        float x, float y,
        bool* key_w, bool* key_a, bool* key_s, bool* key_d
    );

    __declspec(dllexport) bool is_slipping_terrain(float x, float y);

    __declspec(dllexport) bool is_non_slipping_terrain(float x, float y);

    __declspec(dllexport) void sort_vehicle_data(
        VehicleData* vehicles,
        int size,
        const char* leader
    );
}

#endif