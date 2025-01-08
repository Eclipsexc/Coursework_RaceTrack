import unittest
from unittest.mock import Mock, patch
import pygame
from car_selector import (
    get_texture_count_from_sprite,
    draw_frame,
    create_car_selection,
    render_car_selection_instructions,
)

class TestCarSelection(unittest.TestCase):
    @patch("pygame.image.load")
    def test_get_texture_count_from_sprite(self, mock_load):
        pygame.init()
        pygame.display.set_mode((800, 600))
        sprite_surface = pygame.Surface((128, 64)) 
        mock_load.return_value = sprite_surface

        count = get_texture_count_from_sprite("C:\\CourseWork\\Cars\\Supercar_Sprites.png", 32)
        self.assertEqual(count, 2) 

    def test_draw_frame(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        screen = pygame.Surface((800, 600))
        position = (100, 100)
        width, height = 200, 200

        draw_frame(screen, position, width, height)

    @patch("pygame.font.SysFont")
    def test_render_car_selection_instructions(self, mock_font):
        pygame.init()
        pygame.display.set_mode((800, 600))
        screen = pygame.Surface((800, 600))

        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 30))
        mock_font.return_value = mock_font_instance

        render_car_selection_instructions(screen, (100, 100), 200)

    @patch("pygame.mixer.init")
    @patch("pygame.mixer.music.load")
    @patch("pygame.mixer.music.play")
    @patch("pygame.image.load")
    def test_create_car_selection(self, mock_image, mock_music_play, mock_music_load, mock_mixer_init):
        pygame.init()
        pygame.display.set_mode((800, 600))
        screen = pygame.Surface((800, 600))
        
        mock_sprite = pygame.Surface((128, 64))
        mock_image.return_value = mock_sprite

        forbidden_choices = []

        car = create_car_selection(screen, "classic race", "player", forbidden_choices)
        self.assertIsNotNone(car)

if __name__ == "__main__":
    unittest.main()