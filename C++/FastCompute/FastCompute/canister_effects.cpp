#include <algorithm>
#include <cmath>

using namespace std;

extern "C" {

    __declspec(dllexport) void adjust_speed(
        float current_speed, float speed_modifier, float* new_speed
    ) {
        *new_speed = max(1.0f, current_speed + speed_modifier);
    }

    __declspec(dllexport) void adjust_fuel_level(
        float current_fuel, float fuel_change, float* new_fuel
    ) {
        float temp_fuel = current_fuel + fuel_change;
        if (temp_fuel > 100.0f) {
            *new_fuel = 100.0f;
        }
        else if (temp_fuel < 0.0f) {
            *new_fuel = 0.0f;
        }
        else {
            *new_fuel = temp_fuel;
        }
    }

    __declspec(dllexport) void attempt_repair(
        float current_consumption_rate, float repair_value, float* new_consumption_rate
    ) {
        *new_consumption_rate = max(0.0f, current_consumption_rate - repair_value);
    }
}