import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import ctypes
import random
from objects.obstacles import Obstacle, Tumbleweed, Minecart
from objects.canisters import Canister, RepairKitCanister, SuspiciousCanister


spawn_objects_lib = ctypes.CDLL(r"C:\CourseWork\C++\FastCompute\x64\Release\FastCompute.dll")

spawn_objects_lib.generate_random_canister_x.argtypes = [ctypes.c_int]
spawn_objects_lib.generate_random_canister_x.restype = ctypes.c_int

spawn_objects_lib.generate_random_coordinates.argtypes = [ctypes.c_float, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
spawn_objects_lib.generate_random_coordinates.restype = ctypes.c_bool

spawn_objects_lib.generate_specific_y.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
spawn_objects_lib.generate_specific_y.restype = ctypes.c_int

spawn_objects_lib.generate_specific_x.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
spawn_objects_lib.generate_specific_x.restype = ctypes.c_int

spawn_objects_lib.generate_random_x.argtypes = [ctypes.c_int, ctypes.c_int]
spawn_objects_lib.generate_random_x.restype = ctypes.c_int

spawn_objects_lib.generate_random_y.argtypes = [ctypes.c_int, ctypes.c_int]
spawn_objects_lib.generate_random_y.restype = ctypes.c_int

try:
    spawn_objects_lib.initialize_random()
except AttributeError:
    pass  

def generate_random_canister_x(y):
    return spawn_objects_lib.generate_random_canister_x(y)

def generate_random_coordinates(probability):
    x = ctypes.c_int()
    y = ctypes.c_int()
    success = spawn_objects_lib.generate_random_coordinates(ctypes.c_float(probability), ctypes.byref(x), ctypes.byref(y))
    return (x.value, y.value) if success else None

def generate_specific_y(choices):
    if not choices:
        raise ValueError("choices cannot be empty")
    arr = (ctypes.c_int * len(choices))(*choices)
    return spawn_objects_lib.generate_specific_y(arr, len(choices))

def generate_specific_x(choices):
    if not choices:
        raise ValueError("choices cannot be empty")
    arr = (ctypes.c_int * len(choices))(*choices)
    return spawn_objects_lib.generate_specific_x(arr, len(choices))

def generate_random_x(min_x=180, max_x=570):
    return spawn_objects_lib.generate_random_x(min_x, max_x)

def generate_random_y(min_y=50, max_y=2400):
    return spawn_objects_lib.generate_random_y(min_y, max_y)

def generate_tumbleweeds(count):
    obstacles = []
    for _ in range(count):
        x = generate_specific_x([180, 570])
        y = generate_random_y()
        obstacles.append(Tumbleweed(x, y, 3, 1, "Tumbleweed"))
    return obstacles

def generate_minecarts(rail_positions, min_count=2, max_count=5):
    count = random.randint(min_count, max_count)
    minecarts = []
    chosen_positions = random.sample(rail_positions, count)

    for y in chosen_positions:
        x = generate_specific_x([180, 570]) 
        minecarts.append(Minecart(x, y, 4, 2, "Minecart"))

    return minecarts, chosen_positions

def generate_random_obstacles(count, texture_paths, hits_required, name, min_distance=200):
    y_ranges = list(range(0, 301)) + list(range(1501, 2401))
    obstacles = []

    for _ in range(count):
        attempts = 0
        max_attempts = 100

        while attempts < max_attempts:
            x = generate_random_x(225, 500)
            y = generate_specific_y(y_ranges)

            too_close = any(
                abs(obstacle.get_x() - x) < min_distance and abs(obstacle.get_y() - y) < min_distance
                for obstacle in obstacles
            )

            if not too_close:
                obstacles.append(Obstacle(texture_paths, x, y, hits_required, name))
                break

            attempts += 1

    return obstacles

def reset_obstacle_position(obstacle):
    x = generate_specific_x([180, 570])
    y = generate_random_y()
    obstacle.set_x(x)
    obstacle.set_y(y)
    obstacle.reset_moving()

def spawn_suspicious_canisters(max_canisters, canisters):
    for _ in range(max_canisters):
        suspicious_canister = generate_suspicious_canister()
        if suspicious_canister:
            canisters.append(suspicious_canister)
        else:
            max_canisters -= 1
            if max_canisters <= 0:
                break

def create_random_canisters(count):
    canisters = []
    y_start = 0
    step = 2400 // count

    for i in range(count):
        y_start += step
        x = generate_random_canister_x(y_start)

        random_choice = random.random()
        if random_choice < 0.2:
            n = 0
        elif random_choice < 0.5:
            n = 1
        else:
            n = 2

        canisters.append(Canister(x, y_start, n))

    return canisters

def spawn_repair_kit_canisters(count, canisters):
    for _ in range(count):
        repair_kit_canister = generate_repair_kit_canister()
        if repair_kit_canister:
            canisters.append(repair_kit_canister)

def generate_repair_kit_canister():
    coordinates = generate_random_coordinates(0.15)
    if coordinates:
        x, y = coordinates
        return RepairKitCanister(x, y)
    return None

def generate_suspicious_canister():
    coordinates = generate_random_coordinates(0.2)
    if coordinates:
        x, y = coordinates
        fuel_increase, speed_change, fuel_quality = (
            (10, 1, "Good") if random.random() < 0.5 else (-10, -1, "Bad")
        )
        return SuspiciousCanister(x, y, fuel_increase, speed_change, fuel_quality)
    return None