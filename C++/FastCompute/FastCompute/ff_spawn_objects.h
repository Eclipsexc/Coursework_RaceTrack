#pragma once
#ifndef RANDOM_GENERATORS_H
#define RANDOM_GENERATORS_H

extern "C" {

    __declspec(dllexport) int generate_random_canister_x(int y);
    __declspec(dllexport) bool generate_random_coordinates(float probability, int* x, int* y);
    __declspec(dllexport) int generate_specific_y(const int* choices, int size);
    __declspec(dllexport) int generate_specific_x(const int* choices, int size);
    __declspec(dllexport) int generate_random_x(int min_x = 180, int max_x = 570);
    __declspec(dllexport) int generate_random_y(int min_y = 50, int max_y = 2400);

}

#endif