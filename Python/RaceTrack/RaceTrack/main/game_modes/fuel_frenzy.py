import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pygame
from objects.vehicles import CarWithFuel, Bolide, Supercar
from objects.canisters import Canister, RepairKitCanister, SuspiciousCanister
from utilities.rendering import draw_canister, draw_fuel_indicator, draw_hud, draw_obstacle, draw_rails, draw_pedestrian, stop_all_sounds, show_end_screen, draw_road_texture
from game_logic.ff_spawn_objects import (
    generate_random_x, generate_random_y, generate_minecarts, generate_random_obstacles,
    generate_tumbleweeds, reset_obstacle_position, spawn_suspicious_canisters,
    create_random_canisters, spawn_repair_kit_canisters, generate_repair_kit_canister, generate_suspicious_canister
)
from game_logic.ff_logic import (
    update_lap, collect_canister, check_obstacle_collision, switch_map, update_map_objects
)
from display.car_selector import create_car_selection
from objects.pedestrians import DiagonalPedestrian
from objects.obstacles import Obstacle, Tumbleweed, Minecart
from utilities.audio import play_music
from objects.maps import MapFF
from game_logic.bounds_rules import get_bounds_rule_for_map


def fuel_frenzy():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Паливна лихоманка")
    clock = pygame.time.Clock()

    road_map1 = MapFF(
        texture_path="C:/CourseWork/Map/FF_map1.png",
        music_path="C:/CourseWork/music/fuel_frenzy1.mp3",
        name="Fuel Frenzy 1"
    )

    road_map2 = MapFF(
        texture_path="C:/CourseWork/Map/FF_map2.png",
        music_path="C:/CourseWork/music/fuel_frenzy2.mp3",
        name="Fuel Frenzy 2"
    )

    if pygame.mixer.get_init() is None:
        pygame.mixer.init()

    current_map = road_map1

    mode = "fuel frenzy"
    spawn = "carWithFuel"
    car = create_car_selection(screen, mode, spawn, None)
    play_music(current_map.get_music_path(), volume=0.3, loop=-1)

    laps = 5
    lap_completed = True
    car.engine.set_consumption_rate(0.1 * laps)
    Canister.load_textures()
    canisters = create_random_canisters(15)
    texture_paths = ["C:/CourseWork/Obstacles/Roadblock.png", "C:/CourseWork/Obstacles/Broken_roadblock.png"]
    obstacles = []
    moving_obstacles = []
    prev_x, prev_y = car.get_x(), car.get_y()
    map_switched = False
    rail_positions = [1640 + 175 * n for n in range(5)]
    active_rails = []

    pedestrian = DiagonalPedestrian(
        "C:/CourseWork/Pedestrians/Red_Cop (32 x 32).png",
        "C:/CourseWork/Pedestrians/Red_Cop_inverse (32 x 32).png",
        "Red Cop",
        x=240, y=820, target_x=320, target_y=920
    )

    running = True
    bounds_rule = get_bounds_rule_for_map(current_map)

    while running:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        prev_x, prev_y = car.get_x(), car.get_y()

        draw_road_texture(screen, current_map, car, SCREEN_WIDTH)

        if active_rails:
            draw_rails(screen, active_rails, car.get_y(), SCREEN_WIDTH, SCREEN_HEIGHT)

        for canister in canisters:
            collect_canister(car, canister)
            draw_canister(screen, canister, car.get_y(), SCREEN_HEIGHT)

        if map_switched:
            draw_pedestrian(screen, pedestrian, car.get_y(), SCREEN_HEIGHT)
            pedestrian.move()

        obstacles_to_remove = []
        for obstacle in obstacles:
            draw_obstacle(screen, obstacle, car.get_y(), SCREEN_HEIGHT)
            check_obstacle_collision(obstacle, car)
            if not obstacle.get_active():
                obstacles_to_remove.append(obstacle)

        for moving_obstacle in moving_obstacles[:]:
            if moving_obstacle.is_moving():
                moving_obstacle.move()
            else:
                reset_obstacle_position(moving_obstacle)

            draw_obstacle(screen, moving_obstacle, car.get_y(), SCREEN_HEIGHT)
            check_obstacle_collision(moving_obstacle, car)
            if not moving_obstacle.get_active():
                moving_obstacle.set_active(False)

        for obstacle in obstacles_to_remove:
            obstacles.remove(obstacle)

        corrected_keys = {
            pygame.K_w: keys[pygame.K_s],
            pygame.K_s: keys[pygame.K_w],
            pygame.K_a: keys[pygame.K_a],
            pygame.K_d: keys[pygame.K_d],
        }

        car.move(corrected_keys)
        bounds_rule.apply_bounds(car, prev_x, prev_y)

        if 340 <= prev_y and car.get_y() >= 340 and 210 <= car.get_x() <= 330 and lap_completed and not map_switched:
            laps, lap_completed = update_lap(car, laps, lap_completed)

        if laps >= 10 and lap_completed and not map_switched:
            map_switched = True
            current_map, bounds_rule = switch_map(car, road_map2, canisters, obstacles, moving_obstacles, active_rails)

        if 2490 <= prev_y <= 2500 and 0 <= car.get_y() <= 5:
            lap_completed = True
            canisters, obstacles, moving_obstacles, active_rails = update_map_objects(
                laps, canisters, obstacles, moving_obstacles, active_rails, texture_paths, rail_positions
            )

        if map_switched and 750 <= car.get_y() <= 770:
            show_end_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, "Вам вдалось дібратись АЗС!\nВи перемогли!", "C:/CourseWork/music/victory.mp3")
            running = False

        screen.blit(car.get_current_texture(), (car.get_x(), SCREEN_HEIGHT // 2))
        draw_fuel_indicator(screen, car.fuel_tank.get_fuel_level(), SCREEN_WIDTH, SCREEN_HEIGHT)
        draw_hud(screen, car, laps)
        pygame.display.flip()
        clock.tick(60)

        if not car.can_drive():
            stop_all_sounds()
            car.move({pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False})
            pygame.time.wait(4000)
            show_end_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, "Двигун \"заглох\"!\nВи програли!", "C:/CourseWork/music/defeat.mp3")
            running = False

    pygame.quit()


if __name__ == "__main__":
    fuel_frenzy()