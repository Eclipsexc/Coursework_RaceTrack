#include <cmath>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

struct VehicleData {
    const char* name;
    int laps;
    int current_texture;
};

extern "C" {
    __declspec(dllexport) void check_collision(
        float x, float y, float other_x, float other_y, float prev_x, float prev_y,
        float min_distance, float* new_x, float* new_y
    ) {
        float difference_x = fabs(x - other_x);
        float difference_y = fabs(y - other_y);
        if (difference_x < min_distance && difference_y < min_distance) {
            *new_x = prev_x;
            *new_y = prev_y;
        }
        else {
            *new_x = x;
            *new_y = y;
        }
    }

    __declspec(dllexport) bool is_finish_line(float x, float y) {
        return (655 <= x && x <= 665 && 120 <= y && y <= 210);
    }

    __declspec(dllexport) void update_checkpoints(
        float x, float y, bool checkpoints[5]
    ) {
        if (is_finish_line(x, y) && !checkpoints[0]) {
            checkpoints[0] = true;
        }
        if (80 <= x && x <= 90 && 100 <= y && y <= 220 && checkpoints[0] && !checkpoints[1]) {
            checkpoints[1] = true;
        }
        if (500 <= y && y <= 550 && -20 <= x && x <= 80 && checkpoints[1] && !checkpoints[2]) {
            checkpoints[2] = true;
        }
        if (500 <= x && x <= 600 && 630 <= y && y <= 740 && checkpoints[2] && !checkpoints[3]) {
            checkpoints[3] = true;
        }
        if (300 <= y && y <= 320 && 850 <= x && x <= 970 && checkpoints[3] && !checkpoints[4]) {
            checkpoints[4] = true;
        }
    }

    __declspec(dllexport) const char* determine_leader(
        const bool player_checkpoints[5], const bool enemy_checkpoints[5],
        int player_laps, int enemy_laps, const char* previous_leader
    ) {
        auto score = [](int laps, const bool checkpoints[5]) {
            int sum_checkpoints = 0;
            for (int i = 0; i < 5; ++i) {
                if (checkpoints[i]) sum_checkpoints++;
            }
            return laps * 100 + sum_checkpoints;
            };

        int player_score = score(player_laps, player_checkpoints);
        int enemy_score = score(enemy_laps, enemy_checkpoints);

        if (player_score > enemy_score) {
            return "Гравець";
        }
        else if (player_score < enemy_score) {
            return "Противник";
        }
        else {
            return (previous_leader != nullptr) ? previous_leader : "Нічия";
        }
    }

    __declspec(dllexport) void determine_enemy_keys(
        float x, float y,
        bool* key_w, bool* key_a, bool* key_s, bool* key_d
    ) {
        *key_w = false;
        *key_a = false;
        *key_s = false;
        *key_d = false;

        if (120 <= y && y <= 185 && -10 <= x && x <= 960) {
            *key_a = true;
            if (x <= 55) {
                *key_a = false;
                *key_s = true;
            }
        }
        else if (-10 <= x && x <= 70 && 185 < y && y <= 600) {
            *key_s = true;
            if (y >= 565) {
                *key_s = false;
                *key_d = true;
            }
        }
        else if (70 < x && x < 137 && 565 <= y && y <= 600) {
            *key_d = true;
            if (x >= 137) {
                *key_d = false;
                *key_s = true;
            }
        }
        else if (137 <= x && x <= 165 && 555 <= y && y <= 660) {
            *key_s = true;
            if (y >= 650) {
                *key_s = false;
                *key_d = true;
            }
        }
        else if (165 < x && x < 670 && 640 < y && y <= 720) {
            *key_d = true;
            if (x >= 670) {
                *key_d = false;
                *key_w = true;
            }
        }
        else if (670 <= x && x <= 680 && 410 < y && y <= 715) {
            *key_w = true;
            if (y <= 410) {
                *key_w = false;
                *key_d = true;
            }
        }
        else if (670 <= x && x < 900 && 390 <= y && y <= 410) {
            *key_d = true;
            if (x >= 895) {
                *key_d = false;
                *key_w = true;
            }
        }
        else if (895 <= x && x <= 960 && 185 < y && y <= 410) {
            *key_w = true;
        }
    }

    __declspec(dllexport) bool is_slipping_terrain(float x, float y) {
        return (420 <= y && y <= 700 && -7.5 <= x && x <= 190);
    }

    __declspec(dllexport) bool is_non_slipping_terrain(float x, float y) {
        return (
            (640 <= y && y <= 720 && 190 < x && x <= 220) ||
            (400 <= y && y <= 420 && -7.5 <= x && x <= 190)
            );
    }

    __declspec(dllexport) void sort_vehicle_data(
        VehicleData* vehicles,
        int size,
        const char* leader
    ) {
        string leader_name(leader);

        sort(vehicles, vehicles + size, [&leader_name](const VehicleData& a, const VehicleData& b) {
            if (a.name == leader_name) return true;
            if (b.name == leader_name) return false;
            return a.laps > b.laps;
            });
    }
}