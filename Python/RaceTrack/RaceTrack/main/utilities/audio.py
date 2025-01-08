import pygame
import os

def play_music(music_path, volume=0.3, loop=-1):
    if music_path and pygame.mixer.get_init():
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loop)
            except pygame.error as e:
                print(f"Помилка відтворення музики: {e}")
        else:
            print(f"Музичний файл {music_path} не знайдено!")

def play_sound_effect(sound_path, volume=0.5):
    if sound_path and pygame.mixer.get_init():
        if os.path.exists(sound_path):
            try:
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(volume)
                sound.play()
            except pygame.error as e:
                print(f"Помилка відтворення звукового ефекту: {e}")
        else:
            print(f"Звуковий файл {sound_path} не знайдено!")

def stop_all_sounds():
    if pygame.mixer.get_init():
        pygame.mixer.stop()
        pygame.mixer.music.stop()