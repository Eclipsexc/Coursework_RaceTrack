import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pygame
import ctypes
import os
from utilities.audio import play_sound_effect

dll_path = r"C:\CourseWork\C++\FastCompute\x64\Release\FastCompute.dll"
logic = ctypes.CDLL(dll_path)

logic.check_collision.argtypes = [
    ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float,
    ctypes.c_float, ctypes.c_float, ctypes.c_float,
    ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)
]
logic.check_collision.restype = None

logic.is_finish_line.argtypes = [ctypes.c_float, ctypes.c_float]
logic.is_finish_line.restype = ctypes.c_bool

logic.update_checkpoints.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_bool)]
logic.update_checkpoints.restype = None

logic.determine_enemy_keys.argtypes = [
    ctypes.c_float, ctypes.c_float,
    ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_bool),
    ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_bool)
]
logic.determine_enemy_keys.restype = None
logic.is_slipping_terrain.argtypes = [ctypes.c_float, ctypes.c_float]
logic.is_slipping_terrain.restype = ctypes.c_bool

logic.is_non_slipping_terrain.argtypes = [ctypes.c_float, ctypes.c_float]
logic.is_non_slipping_terrain.restype = ctypes.c_bool

def check_collision(x, y, other_x, other_y, prev_x, prev_y, min_distance):
    new_x = ctypes.c_float(0)
    new_y = ctypes.c_float(0)
    logic.check_collision(x, y, other_x, other_y, prev_x, prev_y, min_distance, ctypes.byref(new_x), ctypes.byref(new_y))
    return new_x.value, new_y.value

def handle_terrain(entity):
    x, y = entity.get_x(), entity.get_y()

    if logic.is_slipping_terrain(x, y):
        if not entity.wheels.is_wheels_slipping():
            new_speed = entity.wheels.slip(
                entity.get_speed(), entity.get_default_speed(), entity.is_good_on_dirt()
            )
            entity.set_speed(new_speed)
    elif logic.is_non_slipping_terrain(x, y):
        if entity.wheels.is_wheels_slipping():
            entity.set_speed(entity.get_default_speed())
            entity.wheels.set_wheels_slipping(False)

def is_finish_line(x, y):
    return logic.is_finish_line(x, y)

def update_checkpoints(x, y, checkpoints):
    c_checkpoints = (ctypes.c_bool * len(checkpoints))(*checkpoints)
    logic.update_checkpoints(x, y, c_checkpoints)
    for i in range(len(checkpoints)):
        checkpoints[i] = c_checkpoints[i]

def check_lap_completion(car, checkpoints, laps_completed):
    if all(checkpoints) and is_finish_line(car.get_x(), car.get_y()):
        laps_completed[car.get_name()] += 1
        checkpoints[:] = [True] + [False] * (len(checkpoints) - 1)
        if car.get_type() == "Supercar":
            car.nitro.restore_nitro()

        lap_completion_sound = "C:/CourseWork/music/lap_completion.mp3"
        play_sound_effect(lap_completion_sound, volume=0.5)

def determine_leader(player_checkpoints, enemy_checkpoints, player_laps, enemy_laps, previous_leader):
    def score(laps, checkpoints):
        return laps * 100 + sum(checkpoints)

    player_score = score(player_laps, player_checkpoints)
    enemy_score = score(enemy_laps, enemy_checkpoints)

    if player_score > enemy_score:
        return "Гравець"
    elif player_score < enemy_score:
        return "Противник"
    else:
        return previous_leader if previous_leader else "Нічия"

def handle_enemy_ai(enemy, player, enemy_checkpoints, laps_completed):
    handle_terrain(enemy)
    update_checkpoints(enemy.get_x(), enemy.get_y(), enemy_checkpoints)
    check_lap_completion(enemy, enemy_checkpoints, laps_completed)

    prev_x, prev_y = enemy.get_x(), enemy.get_y()
    keys = determine_enemy_keys(enemy.get_x(), enemy.get_y())

    if enemy.get_type() == "Supercar":
        keys[pygame.K_RCTRL] = False

    enemy.move(keys)
    new_x, new_y = check_collision(enemy.get_x(), enemy.get_y(), player.get_x(), player.get_y(), prev_x, prev_y, 25)
    enemy.set_x(new_x)
    enemy.set_y(new_y)

    if enemy.get_type() == "Supercar":
        if not (enemy.get_x() == prev_x and enemy.get_y() == prev_y):
            keys[pygame.K_RCTRL] = True
        enemy.use_nitro(keys)

def determine_enemy_keys(x, y):
    key_w = ctypes.c_bool(False)
    key_a = ctypes.c_bool(False)
    key_s = ctypes.c_bool(False)
    key_d = ctypes.c_bool(False)

    logic.determine_enemy_keys(x, y, ctypes.byref(key_w), ctypes.byref(key_a), ctypes.byref(key_s), ctypes.byref(key_d))

    return {
        pygame.K_w: key_w.value,
        pygame.K_a: key_a.value,
        pygame.K_s: key_s.value,
        pygame.K_d: key_d.value
    }