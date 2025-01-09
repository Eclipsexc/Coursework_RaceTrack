import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import pygame
import os
from objects.maps import MapCR
from objects.vehicles import Car, Bolide, Supercar
from objects.pedestrians import Pedestrian, StandingPedestrian, DiagonalPedestrian
from display.car_selector import create_car_selection
from utilities.audio import play_music
from utilities.rendering import draw_cr_screen, draw_car, draw_nitro_indicator, show_end_screen, show_traffic_light
from game_logic.bounds_rules import get_bounds_rule_for_map
from game_logic.cr_logic import (
    handle_terrain,
    update_checkpoints,
    check_lap_completion,
    determine_leader,
    handle_enemy_ai,
    check_collision,
)

def classic_race():
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Гараж")

    forbidden_choices = []
    mode = "classic race"
    car = create_car_selection(screen, mode, "player", forbidden_choices)
    enemy = create_car_selection(screen, mode, "enemy", forbidden_choices)
    pygame.display.quit()
    SCREEN_WIDTH = 1300
    SCREEN_HEIGHT = 800
    BLACK_SPACE_WIDTH = 300
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Класична гонка")

    game_map = MapCR(
        texture_path="C:/CourseWork/Map/Classic_map.png",
        music_path="C:/CourseWork/music/classic_race1.mp3",
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        black_space_width=BLACK_SPACE_WIDTH,
        name="Classic Race"
    )

    game_map.load_texture()
    game_map_texture = game_map.get_texture()

    pedestrians = [
        Pedestrian(
            "C:/CourseWork/Pedestrians/Cop (32 x 32).png",
            "C:/CourseWork/Pedestrians/Cop_inverse (32 x 32).png",
            "Cop",
            x=240,
            y=585,
            x_min=235,
            x_max=390
        ),
        Pedestrian(
            "C:/CourseWork/Pedestrians/Slime (32 x 32).png",
            "C:/CourseWork/Pedestrians/Slime_inverse (32 x 32).png",
            "Slime",
            x=430,
            y=585,
            x_min=400,
            x_max=600
        ),
        Pedestrian(
            "C:/CourseWork/Pedestrians/Lemon (32 x 32).png",
            "C:/CourseWork/Pedestrians/Lemon_inverse (32 x 32).png",
            "Lemon",
            x=815,
            y=710,
            x_min=710,
            x_max=940
        ),
        DiagonalPedestrian(
            "C:/CourseWork/Pedestrians/Red_Cop (32 x 32).png",
            "C:/CourseWork/Pedestrians/Red_Cop_inverse (32 x 32).png",
            "Red Cop",
            x=520,
            y=50,
            target_x=470,
            target_y=32
        ),
        StandingPedestrian(
            "C:/CourseWork/Pedestrians/Carrot (32 x 32).png",
            "Carrot",
            x=50,
            y=710
        ),
        StandingPedestrian(
            "C:/CourseWork/Pedestrians/Cherry_inverse (32 x 32).png",
            "Cherry",
            x=20,
            y=710
        )
    ]

    max_lap = 3 
    player_checkpoints = [False, False, False, False, False]
    enemy_checkpoints = [False, False, False, False, False]
    laps_completed = {car.get_name(): 0, enemy.get_name(): 0}
    previous_leader = None

    show_traffic_light(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    play_music(game_map.get_music_path(), volume=0.3)

    clock = pygame.time.Clock()
    running = True

    bounds_rule = get_bounds_rule_for_map(game_map)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        prev_x, prev_y = car.get_x(), car.get_y()

        car.move(keys)

        if car.get_type() == "Supercar":
            car.use_nitro(keys)

        handle_terrain(car)
        
        new_x, new_y = check_collision(car.get_x(), car.get_y(), enemy.get_x(), enemy.get_y(), prev_x, prev_y, 25)
        car.set_x(new_x)
        car.set_y(new_y)

        bounds_rule.apply_bounds(car, prev_x, prev_y)

        update_checkpoints(car.get_x(), car.get_y(), player_checkpoints)
        check_lap_completion(car, player_checkpoints, laps_completed)
        handle_enemy_ai(enemy, car, enemy_checkpoints, laps_completed)

        for pedestrian in pedestrians:
            pedestrian.move()

        previous_leader = draw_cr_screen(
            screen, game_map_texture, car, enemy, pedestrians,
            BLACK_SPACE_WIDTH, SCREEN_HEIGHT, laps_completed, player_checkpoints, enemy_checkpoints, previous_leader, max_lap
        )

        if laps_completed[car.get_name()] >= max_lap or laps_completed[enemy.get_name()] >= max_lap:
            running = False

        clock.tick(60)

    pygame.mixer.music.stop()
    if laps_completed[car.get_name()] >= max_lap:
        show_end_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, "Ви перемогли!", "C:/CourseWork/music/victory.mp3")
    else:
        show_end_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, "Ви програли!", "C:/CourseWork/music/defeat.mp3")
    pygame.quit()

if __name__ == "__main__":
    classic_race()