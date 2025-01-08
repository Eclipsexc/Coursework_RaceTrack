import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import pygame
from utilities.audio import play_music, play_sound_effect
from objects.vehicles import Bolide, Supercar, CarWithFuel
from objects.maps import Map

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_WIDTH = 200
TARGET_HEIGHT = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAME_COLOR = (0, 0, 0)
FRAME_THICKNESS = 8
ANIMATION_DELAY = 10

GARAGE_MUSIC = "C:/CourseWork/music/garage.mp3"
SELECT_SOUND = "C:/CourseWork/music/select.mp3"
SPRAYER_SOUND = "C:/CourseWork/music/sprayer.mp3"
SELECT1_SOUND = "C:/CourseWork/music/select1.mp3"
DENIED_SOUND = "C:/CourseWork/music/denied.mp3"

def draw_frame(screen, position, width, height):
    pygame.draw.rect(
        screen,
        FRAME_COLOR,
        (position[0] - FRAME_THICKNESS // 2,
         position[1] - FRAME_THICKNESS // 2,
         width + FRAME_THICKNESS,
         height + FRAME_THICKNESS),
        FRAME_THICKNESS
    )

def render_instructions(screen, lines, position, width, height, font, text_color, bg_color, bg_offset_y=-10):
    background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    background_surface.fill(bg_color)
    background_rect = background_surface.get_rect(center=(position[0], position[1] + bg_offset_y))
    frame_thickness = 2
    pygame.draw.rect(
        screen,
        WHITE,
        (background_rect.left - frame_thickness, background_rect.top - frame_thickness,
         background_rect.width + 2 * frame_thickness, background_rect.height + 2 * frame_thickness),
        frame_thickness
    )
    screen.blit(background_surface, background_rect)
    line_spacing = 5
    total_height = sum(font.render(line, True, text_color).get_height() for line in lines) + line_spacing * (len(lines) - 1)
    start_y = position[1] - total_height // 2
    for line in lines:
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect(center=(position[0], start_y))
        screen.blit(text_surface, text_rect)
        start_y += text_surface.get_height() + line_spacing

def render_car_selection_instructions(screen, car_position, target_width):
    x_offset = 250
    instructions_position = (
        car_position[0] + target_width // 2 + x_offset,
        car_position[1] - 170
    )
    render_instructions(
        screen,
        ["Up/Down - зміна фарбування", "Left/Right - зміна типу авто", "Enter - підтвердити вибір"],
        instructions_position,
        250, 100,
        pygame.font.SysFont("Arial", 20),
        WHITE,
        (0, 0, 0, 220),
        bg_offset_y=-5
    )

def get_texture_count_from_sprite(sprite_path, sprite_height):
    sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
    sprite_sheet_height = sprite_sheet.get_height()
    return sprite_sheet_height // sprite_height

def create_car_selection(screen, mode, spawn, forbidden_choices):
    pygame.mixer.init()
    garage_map = Map("C:/CourseWork/Map/garage.jpg", "C:/CourseWork/music/garage.mp3", 800, 600)
    play_music(garage_map.get_music_path(), volume=0.3)
    background = garage_map.get_scaled_texture()
    clock = pygame.time.Clock()

    car_x, car_y = 0, 0
    selected_car = None
    animation_index = 0
    frame_counter = 0
    running = True

    if spawn == "carWithFuel":
        x, y = 400, 0
    elif spawn == "player":
        x, y = 715, 135
    else:
        x, y = 705, 185

    if mode == "classic race":
        selected_car = handle_classic_race_mode(
            screen, background, clock, spawn, forbidden_choices, car_x, car_y, animation_index, frame_counter
        )
    elif mode == "fuel frenzy":
        selected_car = handle_fuel_frenzy_mode(
            screen, background, clock, car_x, car_y, x, y, animation_index, frame_counter
        )

    return selected_car

def handle_classic_race_mode(screen, background, clock, spawn, forbidden_choices, car_x, car_y, animation_index, frame_counter):
    temp_bolide = Bolide(0, 0, 0)
    temp_supercar = Supercar(0, 0, 0)

    bolide_texture_count = get_texture_count_from_sprite(temp_bolide.get_textures_path(), temp_bolide.get_sprite_dimensions()[1])
    supercar_texture_count = get_texture_count_from_sprite(temp_supercar.get_textures_path(), temp_supercar.get_sprite_dimensions()[1])

    running = True
    selected_car = None

    while running:
        screen.blit(background, (0, 0))

        frame_counter += 1
        if frame_counter >= ANIMATION_DELAY:
            animation_index = (animation_index + 1) % 4
            frame_counter = 0

        car_position = (300, SCREEN_HEIGHT - TARGET_HEIGHT - 100)
        padding = 10

        overlay = pygame.Surface((TARGET_WIDTH + padding, TARGET_HEIGHT + padding), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 100))
        screen.blit(overlay, (car_position[0] - padding // 2, car_position[1] - padding // 2))

        unavailable_message = None

        if car_x == 0 and ("Supercar", car_y) not in forbidden_choices:
            temp_supercar.set_sprite_height(car_y)
            current_texture = temp_supercar.textures[animation_index]
            stats = {
                "type": temp_supercar.get_type(),
                "speed": temp_supercar.get_speed(),
                "good_on_dirt": temp_supercar.is_good_on_dirt,
                "ability": temp_supercar.get_ability_name()
            }
        elif car_x == 2 and ("Bolide", car_y) not in forbidden_choices:
            temp_bolide.set_sprite_height(car_y)
            current_texture = temp_bolide.textures[animation_index]
            stats = {
                "type": temp_bolide.get_type(),
                "speed": temp_bolide.get_speed(),
                "good_on_dirt": temp_bolide.is_good_on_dirt,
                "ability": temp_bolide.get_ability_name()
            }
        else:
            current_texture = None
            stats = None
            unavailable_message = "На жаль,\nцей авто був обраний раніше.\nОберіть інший транспорт"

        draw_frame(screen, car_position, TARGET_WIDTH, TARGET_HEIGHT)

        if current_texture:
            scaled_texture = pygame.transform.scale(current_texture, (TARGET_WIDTH, TARGET_HEIGHT))
            screen.blit(scaled_texture, car_position)

        font_large = pygame.font.SysFont("Arial", 32)
        mode_text = "Вибір авто гравця" if spawn == "player" else "Вибір авто противника"
        mode_color = (0, 0, 255) if spawn == "player" else (255, 0, 0)
        mode_surface = font_large.render(mode_text, True, mode_color)
        text_position = (car_position[0] + TARGET_WIDTH // 2 - mode_surface.get_width() // 2,
                         car_position[1] + TARGET_HEIGHT + 20)
        pygame.draw.rect(screen, (0, 0, 0), (text_position[0] - 10, text_position[1] - 5,
                                             mode_surface.get_width() + 20, mode_surface.get_height() + 10))
        screen.blit(mode_surface, text_position)

        font = pygame.font.SysFont("Arial", 24)
        if stats:
            stats_text = [
                f"Тип авто: {stats['type']}",
                f"Швидкість: {stats['speed'] * 50} км/год",
                f"Їзда по грунту: {'Хороша' if stats['good_on_dirt'] else 'Погана'}",
                f"Особливість: {stats['ability']}",
            ]
            draw_frame(screen, (car_position[0] - 270, car_position[1] + 20), 250, 140)
            text_overlay = pygame.Surface((250, 140), pygame.SRCALPHA)
            text_overlay.fill((255, 255, 255, 200))
            screen.blit(text_overlay, (car_position[0] - 270, car_position[1] + 20))

            for i, text in enumerate(stats_text):
                surface = font.render(text, True, BLACK)
                screen.blit(surface, (car_position[0] - 260, car_position[1] + 30 + i * 30))
        elif unavailable_message:
            draw_frame(screen, (car_position[0] - 270, car_position[1] + 20), 250, 140)
            text_overlay = pygame.Surface((250, 140), pygame.SRCALPHA)
            text_overlay.fill((255, 255, 255, 200))
            screen.blit(text_overlay, (car_position[0] - 270, car_position[1] + 20))

            small_font = pygame.font.SysFont("Arial", 20)
            for i, line in enumerate(unavailable_message.split("\n")):
                unavailable_surface = small_font.render(line, True, BLACK)
                screen.blit(unavailable_surface, (car_position[0] - 260, car_position[1] + 30 + i * 30))

        render_car_selection_instructions(screen, car_position, TARGET_WIDTH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                del temp_bolide, temp_supercar
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    car_x = 0 if car_x == 2 else 2
                    play_sound_effect(SELECT1_SOUND)
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    if car_x == 0:
                        car_y = (car_y + 1) % supercar_texture_count
                    elif car_x == 2:
                        car_y = (car_y + 1) % bolide_texture_count
                    play_sound_effect(SPRAYER_SOUND)
                elif event.key == pygame.K_RETURN:
                    if current_texture:
                        play_sound_effect(SELECT_SOUND, volume=0.7)
                        pygame.mixer.music.stop()
                        if car_x == 0 and ("Supercar", car_y) not in forbidden_choices:
                            selected_car = temp_supercar
                            running = False
                        elif car_x == 2 and ("Bolide", car_y) not in forbidden_choices:
                            selected_car = temp_bolide
                            running = False
                    else:
                        play_sound_effect(DENIED_SOUND)

        pygame.display.flip()
        clock.tick(30)

    del temp_bolide, temp_supercar

    forbidden_choices.append((selected_car.get_type(), car_y))

    if selected_car.get_type() == "Supercar":
        return Supercar(0, 0, car_y)
    else:
        return Bolide(0, 0, car_y)

def handle_fuel_frenzy_mode(screen, background, clock, car_x, car_y, x, y, animation_index, frame_counter):
    temp_car = CarWithFuel(x, y, 0)
    texture_count = get_texture_count_from_sprite(temp_car.get_textures_path(), temp_car.get_sprite_dimensions()[0])

    running = True

    while running:
        screen.blit(background, (0, 0))

        frame_counter += 1
        if frame_counter >= ANIMATION_DELAY:
            animation_index = (animation_index + 1) % 4
            frame_counter = 0

        car_position = (300, SCREEN_HEIGHT - TARGET_HEIGHT - 100)
        padding = 10

        overlay = pygame.Surface((TARGET_WIDTH + padding, TARGET_HEIGHT + padding), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 100))
        screen.blit(overlay, (car_position[0] - padding // 2, car_position[1] - padding // 2))

        draw_frame(screen, car_position, TARGET_WIDTH, TARGET_HEIGHT)

        temp_car.set_sprite_height(car_y)
        current_texture = temp_car.textures[animation_index]
        scaled_texture = pygame.transform.scale(current_texture, (TARGET_WIDTH, TARGET_HEIGHT))
        screen.blit(scaled_texture, car_position)

        font_large = pygame.font.SysFont("Arial", 32)
        mode_text = "Оберіть авто гравця"
        mode_color = (0, 255, 0)
        mode_surface = font_large.render(mode_text, True, mode_color)
        text_position = (car_position[0] + TARGET_WIDTH // 2 - mode_surface.get_width() // 2,
                         car_position[1] + TARGET_HEIGHT + 20)
        pygame.draw.rect(screen, (0, 0, 0), (text_position[0] - 10, text_position[1] - 5,
                                             mode_surface.get_width() + 20, mode_surface.get_height() + 10))
        screen.blit(mode_surface, text_position)

        render_car_selection_instructions(screen, car_position, TARGET_WIDTH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    car_y = (car_y + 1) % texture_count
                    play_sound_effect(SPRAYER_SOUND)
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    play_sound_effect(SELECT1_SOUND)
                elif event.key == pygame.K_RETURN:
                    play_sound_effect(SELECT_SOUND, volume=0.7)
                    pygame.mixer.music.stop()
                    running = False

        pygame.display.flip()
        clock.tick(30)

    return CarWithFuel(x, y, car_y)