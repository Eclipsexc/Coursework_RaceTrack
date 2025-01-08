import os
import sys
import pygame

class Map:
    def __init__(self, texture_path, music_path, screen_width=None, screen_height=None, name="Default"):
        self.texture_path = texture_path
        self.music_path = music_path
        self.texture = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.name = name

    def load_texture(self):
        if not os.path.exists(self.texture_path):
            print(f"Мапа {self.texture_path} не знайдена! Перевірте шлях.")
            sys.exit()
        self.texture = pygame.image.load(self.texture_path).convert_alpha()

    def get_scaled_texture(self):
        if self.texture is None:
            self.load_texture()
        if self.screen_width and self.screen_height:
            return pygame.transform.scale(self.texture, (self.screen_width, self.screen_height))
        return self.texture

    def get_texture(self):
        if self.texture is None:
            self.load_texture()
        return self.texture

    def get_music_path(self):
        return self.music_path

    def get_name(self):
        return self.name

class MapCR(Map):
    def __init__(self, texture_path, music_path, screen_width, screen_height, black_space_width, name="Classic Race"):
        super().__init__(texture_path, music_path, screen_width, screen_height, name)
        self.black_space_width = black_space_width

    def load_texture(self):
        if not os.path.exists(self.texture_path):
            print(f"Мапа {self.texture_path} не знайдена! Перевірте шлях.")
            sys.exit()
        self.texture = pygame.image.load(self.texture_path).convert_alpha()
        if self.screen_width and self.screen_height and self.black_space_width > 0:
            self.texture = pygame.transform.scale(
                self.texture,
                (self.screen_width - self.black_space_width, self.screen_height)
            )

class MapFF(Map):
    def __init__(self, texture_path, music_path, screen_width=None, screen_height=None, name="Fuel Frenzy"):
        super().__init__(texture_path, music_path, screen_width, screen_height, name)

    def get_scaled_texture(self, width):
        if self.texture is None:
            self.load_texture()
        new_height = int(self.texture.get_height() * (width / self.texture.get_width()))
        return pygame.transform.scale(self.texture, (width, new_height))