import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import random
import pygame
import os
import ctypes
from objects.vehicles import CarWithFuel
from objects.canisters import Canister, RepairKitCanister, SuspiciousCanister
from objects.obstacles import Obstacle
from utilities.audio import play_music, play_sound_effect
from game_logic.bounds_rules import get_bounds_rule_for_map
from game_logic.ff_spawn_objects import (
    generate_random_x,
    generate_random_y,
    generate_minecarts,
    generate_random_obstacles,
    generate_tumbleweeds,
    reset_obstacle_position,
    spawn_suspicious_canisters,
    create_random_canisters,
    spawn_repair_kit_canisters,
    generate_repair_kit_canister,
    generate_suspicious_canister
)
dll_path = r"C:\CourseWork\C++\FastCompute\x64\Release\FastCompute.dll"
logic = ctypes.CDLL(dll_path)

logic.adjust_speed.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float)]
logic.adjust_fuel_level.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float)]
logic.attempt_repair.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float)]

def attempt_repair(car):
    if car.engine.get_consumption_rate() > 0.3:
        current_rate = ctypes.c_float(car.engine.get_consumption_rate())
        repair_value = ctypes.c_float(0.3)
        new_rate = ctypes.c_float()
        logic.attempt_repair(current_rate, repair_value, ctypes.byref(new_rate))
        car.engine.set_consumption_rate(new_rate.value)

def apply_suspicious_canister_effects(car, canister):
    fuel_change = canister.get_fuel_increase()
    speed_modifier = canister.get_speed_change()

    current_speed = ctypes.c_float(car.get_speed())
    speed_mod = ctypes.c_float(speed_modifier)
    new_speed = ctypes.c_float()
    logic.adjust_speed(current_speed, speed_mod, ctypes.byref(new_speed))
    car.set_speed(new_speed.value)

    current_fuel_level = ctypes.c_float(car.fuel_tank.get_fuel_level())
    fuel_mod = ctypes.c_float(fuel_change)
    new_fuel_level = ctypes.c_float()
    logic.adjust_fuel_level(current_fuel_level, fuel_mod, ctypes.byref(new_fuel_level))
    car.fuel_tank.set_fuel_level(new_fuel_level.value)

def collect_canister(car, canister):
    if not canister.get_collected() and (
        abs(car.get_x() - canister.get_x()) < canister.CANISTER_SIZE // 1.5 and
        abs(car.get_y() - canister.get_y()) < canister.CANISTER_SIZE // 1.5
    ):
        canister.collected = True
        canister_type = canister.get_type()

        if canister_type == "repair_kit":
            play_sound_effect("C:/CourseWork/music/repair_kit.mp3", volume=0.3)
            attempt_repair(car)
        elif canister_type == "suspicious":
            play_sound_effect("C:/CourseWork/music/potion.mp3", volume=0.3)
            apply_suspicious_canister_effects(car, canister)
        else:
            play_sound_effect("C:/CourseWork/music/collect_can2.mp3", volume=0.3)

        current_fuel_level = ctypes.c_float(car.fuel_tank.get_fuel_level())
        fuel_increase = ctypes.c_float(canister.get_fuel_increase())
        new_fuel_level = ctypes.c_float()
        logic.adjust_fuel_level(current_fuel_level, fuel_increase, ctypes.byref(new_fuel_level))
        car.fuel_tank.set_fuel_level(new_fuel_level.value)

def update_lap(car, laps, lap_completed):
    laps += 1
    new_consumption_rate = car.engine.get_consumption_rate() + 0.1
    car.engine.set_consumption_rate(new_consumption_rate)
    lap_completed = False
    play_sound_effect("C:/CourseWork/music/lap_completion.mp3", volume=0.5)
    return laps, lap_completed

def switch_map(car, new_map, canisters, obstacles, moving_obstacles, active_rails):
    car.set_y(0)
    car.engine.set_consumption_rate(0)
    canisters.clear()
    obstacles.clear()
    moving_obstacles.clear()
    active_rails.clear()

    bounds_rule = get_bounds_rule_for_map(new_map)
    play_music(new_map.get_music_path(), volume=0.3)

    repair_kit = RepairKitCanister(300, 100)
    canisters.append(repair_kit)

    return new_map, bounds_rule

def update_map_objects(laps, canisters, obstacles, moving_obstacles, active_rails, texture_paths, rail_positions):
    canisters.clear()
    obstacles.clear()
    moving_obstacles.clear()
    active_rails.clear()
    canisters = create_random_canisters(15)

    if laps >= 3:
        moving_obstacles.extend(generate_tumbleweeds(5))
    if laps >= 4:
        spawn_suspicious_canisters(3, canisters)
    if laps >= 6:
        obstacles.extend(generate_random_obstacles(5, texture_paths, 2, "Roadblock"))
    if laps >= 7:
        spawn_repair_kit_canisters(2, canisters)
    if laps >= 8:
        minecarts, new_rails = generate_minecarts(rail_positions)
        moving_obstacles.extend(minecarts)
        active_rails.extend(new_rails)

    return canisters, obstacles, moving_obstacles, active_rails

def check_obstacle_collision(obstacle, car):
    car_x = car.get_x()
    car_y = car.get_y()
    obstacle_x = obstacle.get_x()
    obstacle_y = obstacle.get_y()

    if obstacle.get_obstacle_type() == "Default" and obstacle.get_name() == "Roadblock":
        collision_width = obstacle.get_width() // 2
        collision_height = obstacle.get_height() // 2
    else:
        collision_width = obstacle.get_width()
        collision_height = obstacle.get_height()

    if abs(car_x - obstacle_x) < collision_width and abs(car_y - obstacle_y) < collision_height:
        if not obstacle.get_is_colliding():
            obstacle.set_current_hits(obstacle.get_current_hits() + 1)
            obstacle.set_is_colliding(True)

            if obstacle.get_obstacle_type() == "Moving":
                if obstacle.get_name() == "Minecart":
                    current_fuel = car.fuel_tank.get_fuel_level()
                    car.fuel_tank.set_fuel_level(max(0, current_fuel - 40))
                    play_sound_effect("C:/CourseWork/music/hit_minecart.mp3")
                elif obstacle.get_name() == "Tumbleweed":
                    current_fuel = car.fuel_tank.get_fuel_level()
                    car.fuel_tank.set_fuel_level(max(0, current_fuel - 10))
                    play_sound_effect("C:/CourseWork/music/hit_tumbleweed.mp3")
            elif obstacle.get_obstacle_type() == "Default":
                current_fuel = car.fuel_tank.get_fuel_level()
                car.fuel_tank.set_fuel_level(max(0, current_fuel - 20))
                play_sound_effect("C:/CourseWork/music/hit_roadblock.mp3")

            obstacle.update_texture()

            if obstacle.get_current_hits() >= obstacle.get_hits_required():
                obstacle.set_active(False)
    else:
        obstacle.set_is_colliding(False)