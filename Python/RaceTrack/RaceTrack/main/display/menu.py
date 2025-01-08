import pygame
import cv2
import sys
import os
import subprocess
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from  utilities.audio import play_music, play_sound_effect

def scale_image_proportionally(image, target_width, target_height):
    original_width, original_height = image.get_width(), image.get_height()
    aspect_ratio = original_width / original_height
    if target_width / target_height > aspect_ratio:
        new_height = target_height
        new_width = int(aspect_ratio * target_height)
    else:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    return pygame.transform.scale(image, (new_width, new_height))

def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Не вдалося відкрити відео {video_path}.")
        sys.exit()
    return cap

def load_title_image(title_image_path, width, height):
    if not os.path.exists(title_image_path):
        print(f"Зображення титулки {title_image_path} не знайдено! Перевірте шлях.")
        sys.exit()
    title_image = pygame.image.load(title_image_path)
    return scale_image_proportionally(title_image, width, height)

def render_menu(screen, font_menu, font_menu_active, menu_items, active_index, menu_positions, arrow_left, arrow_right, highlight_color, black, gray_transparent):
    for i, item in enumerate(menu_items):
        text = font_menu.render(item, True, black) if i != active_index else font_menu_active.render(item, True, black)
        text_pos = text.get_rect(center=menu_positions[i])

        if i == active_index:
            active_rect = text_pos.inflate(20, 10)
            pygame.draw.rect(screen, highlight_color, active_rect, border_radius=5)
            arrow_left_pos = arrow_left.get_rect(right=text_pos.left - 20, centery=text_pos.centery)
            arrow_right_pos = arrow_right.get_rect(left=text_pos.right + 20, centery=text_pos.centery)
            screen.blit(arrow_left, arrow_left_pos)
            screen.blit(arrow_right, arrow_right_pos)
        else:
            surface = pygame.Surface((text_pos.width + 20, text_pos.height + 10), pygame.SRCALPHA)
            surface.fill(gray_transparent)
            screen.blit(surface, (text_pos.x - 10, text_pos.y - 5))

        screen.blit(text, text_pos)

def render_help_text(screen, font_help, text, screen_width, screen_height, text_color, background_color):
    help_surface = font_help.render(text, True, text_color)
    help_pos = help_surface.get_rect(center=(screen_width // 2, screen_height - 20))

    background_rect = pygame.Surface((help_pos.width + 20, help_pos.height + 10), pygame.SRCALPHA)
    background_rect.fill(background_color)

    background_rect_pos = background_rect.get_rect(center=(screen_width // 2, screen_height - 20))
    screen.blit(background_rect, background_rect_pos)
    screen.blit(help_surface, help_pos)

def start_menu():
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Меню")

    video_paths = {
        "Паливна лихоманка": "C:/CourseWork/video/background_video1.mp4",
        "Класична гонка": "C:/CourseWork/video/background_video2.mp4",
        "Вихід": "C:/CourseWork/video/background_video3.mp4"
    }

    music_paths = {
        "Паливна лихоманка": "C:/CourseWork/music/background_music1.mp3",
        "Класична гонка": "C:/CourseWork/music/background_music2.mp3",
        "Вихід": "C:/CourseWork/music/background_music3.mp3"
    }

    music_volumes = {
        "Паливна лихоманка": 0.5,
        "Класична гонка": 0.2,
        "Вихід": 0.7
    }

    game_scripts = {
        "Паливна лихоманка": str(Path("C:/CourseWork/Python/RaceTrack/RaceTrack/main/game_modes/fuel_frenzy.py").resolve()),
        "Класична гонка": str(Path("C:/CourseWork/Python/RaceTrack/RaceTrack/main/game_modes/classic_race.py").resolve())
    }

    tutorial_images = {
        "Паливна лихоманка": [
            "C:/CourseWork/tutorial/tutorial_ff1.png",
            "C:/CourseWork/tutorial/tutorial_ff2.png"
        ],
        "Класична гонка": [
            "C:/CourseWork/tutorial/tutorial_classic.png"
        ]
    }

    select_sound = "C:/CourseWork/music/select.mp3"
    select1_sound = "C:/CourseWork/music/select1.mp3"

    active_index = 0
    menu_items = list(video_paths.keys())
    current_video_path = video_paths[menu_items[active_index]]
    current_music_path = music_paths[menu_items[active_index]]
    current_music_volume = music_volumes[menu_items[active_index]]
    cap = load_video(current_video_path)
    play_music(current_music_path, current_music_volume)

    title_image_path = "C:/CourseWork/tutorial/title_image.jpg"
    title_image = load_title_image(title_image_path, 600, 150)
    title_image_pos = (SCREEN_WIDTH // 2 - title_image.get_width() // 2, 5)

    font_menu = pygame.font.Font(pygame.font.get_default_font(), 24)
    font_menu_active = pygame.font.Font(pygame.font.get_default_font(), 32)
    font_help = pygame.font.Font(pygame.font.get_default_font(), 20)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    HIGHLIGHT_COLOR = (255, 255, 255)
    GRAY_TRANSPARENT = (128, 128, 128, 128)
    SEMI_TRANSPARENT_BLACK = (0, 0, 0, 180)

    arrow_left = font_menu_active.render("-->", True, HIGHLIGHT_COLOR)
    arrow_right = font_menu_active.render("<--", True, HIGHLIGHT_COLOR)

    menu_positions = [
        (SCREEN_WIDTH // 2, 250),
        (SCREEN_WIDTH // 2, 300),
        (SCREEN_WIDTH // 2, 350),
    ]

    clock = pygame.time.Clock()
    running = True
    pygame.key.set_repeat(200, 50)
    tutorial_index = 0
    in_tutorial = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if in_tutorial:
                    if event.key == pygame.K_RIGHT:
                        tutorial_index = (tutorial_index + 1) % len(tutorial_images[menu_items[active_index]])
                        play_sound_effect(select1_sound)
                    elif event.key == pygame.K_LEFT:
                        tutorial_index = (tutorial_index - 1) % len(tutorial_images[menu_items[active_index]])
                        play_sound_effect(select1_sound)
                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", game_scripts[menu_items[active_index]]], check=True)
                        sys.exit()
                else:
                    if event.key == pygame.K_UP:
                        active_index = (active_index - 1) % len(menu_items)
                        current_video_path = video_paths[menu_items[active_index]]
                        current_music_path = music_paths[menu_items[active_index]]
                        current_music_volume = music_volumes[menu_items[active_index]]
                        cap.release()
                        cap = load_video(current_video_path)
                        play_music(current_music_path, current_music_volume)
                    elif event.key == pygame.K_DOWN:
                        active_index = (active_index + 1) % len(menu_items)
                        current_video_path = video_paths[menu_items[active_index]]
                        current_music_path = music_paths[menu_items[active_index]]
                        current_music_volume = music_volumes[menu_items[active_index]]
                        cap.release()
                        cap = load_video(current_video_path)
                        play_music(current_music_path, current_music_volume)
                    elif event.key == pygame.K_RETURN:
                        if menu_items[active_index] in tutorial_images:
                            in_tutorial = True
                            tutorial_index = 0
                            cap.release()
                        elif menu_items[active_index] == "Вихід":
                            cap.release()
                            pygame.quit()
                            sys.exit()
                        elif menu_items[active_index] in game_scripts:
                            game_path = game_scripts[menu_items[active_index]]
                            if os.path.exists(game_path):
                                cap.release()
                                pygame.mixer.music.stop()
                                pygame.quit()
                                subprocess.run(["python", game_path], check=True)
                                sys.exit()
                            else:
                                print(f"Файл {game_path} не знайдено! Перевірте шлях.")

        if in_tutorial:
            tutorial_image = pygame.image.load(tutorial_images[menu_items[active_index]][tutorial_index])
            scaled_image = scale_image_proportionally(tutorial_image, SCREEN_WIDTH, SCREEN_HEIGHT)
            x_offset = (SCREEN_WIDTH - scaled_image.get_width()) // 2
            y_offset = (SCREEN_HEIGHT - scaled_image.get_height()) // 2
            screen.blit(scaled_image, (x_offset, y_offset))
        else:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))
            screen.blit(title_image, title_image_pos)
            render_menu(screen, font_menu, font_menu_active, menu_items, active_index, menu_positions, arrow_left, arrow_right, HIGHLIGHT_COLOR, BLACK, GRAY_TRANSPARENT)
            render_help_text(screen, font_help, "Up/Down - гортання пунктів меню. Enter - вибір.", SCREEN_WIDTH, SCREEN_HEIGHT, HIGHLIGHT_COLOR, SEMI_TRANSPARENT_BLACK)

        pygame.display.flip()
        clock.tick(60)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    start_menu()