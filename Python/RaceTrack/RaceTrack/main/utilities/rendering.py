import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import pygame
from game_logic.cr_logic import determine_leader
from utilities.audio import play_music, stop_all_sounds
import time

def draw_cr_screen(
    screen, game_map, car, enemy, pedestrians, black_space_width, screen_height, 
    laps_completed, player_checkpoints, enemy_checkpoints, previous_leader, max_lap
):
    screen.fill((0, 0, 0), rect=(0, 0, black_space_width, screen_height))
    font = pygame.font.SysFont("Arial", 24)

    leader = determine_leader(
        player_checkpoints, enemy_checkpoints,
        laps_completed[car.get_name()], laps_completed[enemy.get_name()],
        previous_leader
    )

    if leader != "Нічия":
        previous_leader = leader

    vehicles = [
        {
            "name": "Гравець",
            "laps": laps_completed[car.get_name()],
            "current_texture": car.current_texture,
            "texture": pygame.transform.scale(car.textures[car.current_texture], (40, 40))
        },
        {
            "name": "Противник",
            "laps": laps_completed[enemy.get_name()],
            "current_texture": enemy.current_texture,
            "texture": pygame.transform.scale(enemy.textures[enemy.current_texture], (40, 40))
        }
    ]

    first_vehicle = vehicles[0] if leader == "Гравець" else vehicles[1]
    second_vehicle = vehicles[1] if leader == "Гравець" else vehicles[0]

    for i, vehicle in enumerate([first_vehicle, second_vehicle], start=1):
        screen.blit(vehicle["texture"], (10, 30 + i * 50))
        label_surface = font.render(
            f"{i}) {vehicle['name']} ({vehicle['laps']}/{max_lap})",
            True, (255, 255, 255)
        )
        screen.blit(label_surface, (70, 30 + i * 50))

    leader_surface = font.render(f"Лідер: {leader}", True, (255, 255, 0))
    screen.blit(leader_surface, (10, screen_height - 40))

    player_speed_surface = font.render(f"Гравець: {car.get_speed() * 50:.1f} км/год", True, (255, 255, 255))
    screen.blit(player_speed_surface, (10, screen_height - 100))

    enemy_speed_surface = font.render(f"Противник: {enemy.get_speed() * 50:.1f} км/год", True, (255, 255, 255))
    screen.blit(enemy_speed_surface, (10, screen_height - 70))

    screen.blit(game_map, (black_space_width, 0))

    draw_car(screen, car, black_space_width)
    draw_car(screen, enemy, black_space_width)

    for pedestrian in pedestrians:
        draw_pedestrian(screen, pedestrian, black_space_width=black_space_width)

    if car.get_type() == "Supercar":
        draw_nitro_indicator(screen, car, black_space_width, screen_height)

    pygame.display.flip()

    return previous_leader

def draw_car(screen, car, black_space_width):
    screen.blit(car.textures[car.current_texture], (car.get_x() + black_space_width, car.get_y()))

def draw_nitro_indicator(screen, car, black_space_width, screen_height):
    nitro_level = round(car.nitro.get_nitro_level())
    BAR_WIDTH, BAR_HEIGHT = 20, 200
    BAR_X, BAR_Y = black_space_width - 180, screen_height // 2 - BAR_HEIGHT // 2

    pygame.draw.rect(screen, (255, 255, 255), (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2)

    nitro_height = (nitro_level / 100) * BAR_HEIGHT
    pygame.draw.rect(screen, (0, 0, 255), (BAR_X, BAR_Y + BAR_HEIGHT - nitro_height, BAR_WIDTH, nitro_height))

    font = pygame.font.SysFont("Arial", 18)
    nitro_text = font.render(f"{nitro_level}%", True, (255, 255, 255))
    text_rect = nitro_text.get_rect(center=(BAR_X + BAR_WIDTH // 2, BAR_Y + BAR_HEIGHT + 20))
    screen.blit(nitro_text, text_rect)

def draw_pedestrian(screen, pedestrian, car_y=None, screen_height=None, black_space_width=0):
    if car_y is not None and screen_height is not None:
        screen_y = screen_height // 2 + (car_y - pedestrian.get_y())
    else:
        screen_y = pedestrian.get_y()

    screen_x = pedestrian.get_x() + black_space_width

    texture = (
        pedestrian.get_mirrored_textures()[pedestrian.get_current_texture()]
        if pedestrian.is_moving_right() and pedestrian.get_mirrored_textures()
        else pedestrian.get_textures()[pedestrian.get_current_texture()]
    )
    screen.blit(texture, (screen_x, screen_y))

def draw_canister(screen, canister, car_y, SCREEN_HEIGHT):
    if not canister.get_collected():
        visible_margin = SCREEN_HEIGHT
        screen_y = SCREEN_HEIGHT // 2 + (car_y - canister.get_y())

        if -visible_margin <= screen_y <= SCREEN_HEIGHT + visible_margin:
            screen.blit(canister.texture, (canister.get_x(), screen_y))

def draw_fuel_indicator(screen, fuel_level, SCREEN_WIDTH, SCREEN_HEIGHT):
    fuel_level = round(fuel_level)
    BAR_WIDTH, BAR_HEIGHT = 20, 200
    BAR_X, BAR_Y = SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - BAR_HEIGHT // 2

    if fuel_level > 70:
        color = (0, 255, 0)
    elif 35 < fuel_level <= 70:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)

    pygame.draw.rect(screen, (255, 255, 255), (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2)
    fuel_height = (fuel_level / 100) * BAR_HEIGHT
    pygame.draw.rect(screen, color, (BAR_X, BAR_Y + BAR_HEIGHT - fuel_height, BAR_WIDTH, fuel_height))

    font = pygame.font.SysFont("Arial", 18)
    fuel_text = font.render(f"{fuel_level}%", True, (255, 255, 255))
    text_rect = fuel_text.get_rect(center=(BAR_X + BAR_WIDTH // 2, BAR_Y + BAR_HEIGHT + 15))
    screen.blit(fuel_text, text_rect)

def draw_ff_hud(screen, car, laps, max_laps):
    font = pygame.font.SysFont("Arial", 18, bold=True)
    text_color = (255, 255, 255)

    car_speed = car.get_speed()
    consumption_rate = car.engine.get_consumption_rate()

    laps_text = f"Кіл: {laps}/{max_laps}"
    speed_text = "Швидкість:"
    speed_value_text = f"{car_speed * 40:.1f} км/год"  
    consumption_rate_text = "Розхід:"
    consumption_value_text = f"{consumption_rate * 100:.1f}%"  

    laps_surface = font.render(laps_text, True, text_color)
    speed_surface = font.render(speed_text, True, text_color)
    speed_value_surface = font.render(speed_value_text, True, text_color)
    consumption_rate_surface = font.render(consumption_rate_text, True, text_color)
    consumption_value_surface = font.render(consumption_value_text, True, text_color)

    padding = 10
    current_x, current_y = 10, 10

    screen.blit(laps_surface, (current_x, current_y))
    current_y += laps_surface.get_height() + padding

    screen.blit(speed_surface, (current_x, current_y))
    current_y += speed_surface.get_height()
    screen.blit(speed_value_surface, (current_x, current_y))
    current_y += speed_value_surface.get_height() + padding

    screen.blit(consumption_rate_surface, (current_x, current_y))
    current_y += consumption_rate_surface.get_height()
    screen.blit(consumption_value_surface, (current_x, current_y))

def draw_obstacle(screen, obstacle, car_y, screen_height):
    if not obstacle.get_active():
        return
    screen_y = screen_height // 2 + (car_y - obstacle.get_y())
    screen.blit(obstacle.get_texture(), (obstacle.get_x(), screen_y))

def draw_rails(screen, y_positions, car_y, screen_width, screen_height):
    rail_texture_path = "C:/CourseWork/Map/Rails.png"
    rail_texture = pygame.image.load(rail_texture_path).convert_alpha()
    rail_texture = pygame.transform.scale(rail_texture, (screen_width // 2, 32))
    
    for y in y_positions:
        screen_y = screen_height // 2 + (car_y - y)
        screen.blit(rail_texture, (screen_width // 4, screen_y))

def show_end_screen(screen, screen_width, screen_height, message, music_path):
    import subprocess
    import sys

    stop_all_sounds()

    if music_path and pygame.mixer.get_init():
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        else:
            print(f"Музичний файл {music_path} не знайдено!")

    font = pygame.font.SysFont("Arial", 50)
    lines = message.split("\n")
    screen.fill((0, 0, 0))

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (255, 255, 0))
        screen.blit(
            text_surface,
            (
                screen_width // 2 - text_surface.get_width() // 2,
                screen_height // 2 - len(lines) * text_surface.get_height() // 2 + i * text_surface.get_height(),
            ),
        )

    pygame.display.flip()
    pygame.time.wait(5000)

    try:
        subprocess.Popen(["python", "C:/Coursework/Python/RaceTrack/RaceTrack/main/display/menu.py"])
    except FileNotFoundError:
        print("Menu.py не знайдено! Перевірте шлях до файлу.")
    except Exception as e:
        print(f"Помилка при запуску Menu.py: {e}")
    finally:
        pygame.quit()
        sys.exit()

def show_traffic_light(screen, screen_width, screen_height):
    font = pygame.font.SysFont("Arial", 100)
    colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)] 
    messages = ["НА СТАРТ", "УВАГА", "РУШ!"]

    traffic_light_music = "C:/CourseWork/music/traffic_light.mp3"
    play_music(traffic_light_music, volume=0.5, loop=0)

    for i, color in enumerate(colors):
        screen.fill((0, 0, 0))
        text_surface = font.render(messages[i], True, color)
        screen.blit(
            text_surface,
            (screen_width // 2 - text_surface.get_width() // 2,
             screen_height // 2 - text_surface.get_height() // 2)
        )
        pygame.display.flip()
        time.sleep(1)

    pygame.mixer.stop()

def draw_road_texture(screen, current_map, car, screen_width):
    road_width = screen_width // 2
    road_height = int(current_map.get_texture().get_height() * (road_width / current_map.get_texture().get_width()))
    camera_offset = car.get_y() % road_height  
    for i in range(-1, 3):
        road_x = screen_width // 2 - road_width // 2
        road_y = camera_offset + i * road_height
        screen.blit(current_map.get_scaled_texture(road_width), (road_x, road_y))