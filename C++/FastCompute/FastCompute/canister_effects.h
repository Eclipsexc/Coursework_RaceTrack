#pragma once
#ifndef CANISTER_EFFECTS_H
#define CANISTER_EFFECTS_H

#include <cmath>

extern "C" {
    __declspec(dllexport) void adjust_speed(
        float current_speed, float speed_modifier, float* new_speed
    );

    __declspec(dllexport) void adjust_fuel_level(
        float current_fuel, float fuel_change, float* new_fuel
    );

    __declspec(dllexport) void attempt_repair(
        float current_consumption_rate, float repair_value, float* new_consumption_rate
    );
}

#endif