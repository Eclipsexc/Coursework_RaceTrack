import unittest
from unittest.mock import Mock, patch
import pygame
from rendering import (
    draw_screen, draw_car, draw_nitro_indicator, draw_pedestrian,
    draw_canister, draw_fuel_indicator, draw_hud, draw_obstacle,
    draw_rails, show_end_screen, show_traffic_light, draw_road_texture
)

class TestDrawFunctions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_draw_canister(self):
        canister = Mock()
        canister.get_collected.return_value = False
        canister.get_y.return_value = 100
        canister.get_x.return_value = 50
        canister.texture = pygame.Surface((32, 32))
        draw_canister(self.screen, canister, 200, 600)

    def test_draw_car(self):
        car = Mock()
        car.get_x.return_value = 50
        car.get_y.return_value = 100
        car.textures = [pygame.Surface((32, 32))]
        car.current_texture = 0
        draw_car(self.screen, car, 100)

    def test_draw_fuel_indicator(self):
        draw_fuel_indicator(self.screen, 50, 800, 600)

    def test_draw_hud(self):
        car = Mock()
        car.get_x.return_value = 50
        car.get_y.return_value = 100
        car.get_speed.return_value = 2
        car.engine.get_consumption_rate.return_value = 0.05
        draw_hud(self.screen, car, 3)

    def test_draw_nitro_indicator(self):
        car = Mock()
        car.nitro.get_nitro_level.return_value = 50
        draw_nitro_indicator(self.screen, car, 100, 600)

    def test_draw_obstacle(self):
        obstacle = Mock()
        obstacle.get_active.return_value = True
        obstacle.get_y.return_value = 200
        obstacle.get_x.return_value = 100
        obstacle.get_texture.return_value = pygame.Surface((32, 32))
        draw_obstacle(self.screen, obstacle, 300, 600)

    def test_draw_pedestrian(self):
        pedestrian = Mock()
        pedestrian.get_y.return_value = 100
        pedestrian.get_x.return_value = 50
        pedestrian.get_textures.return_value = [pygame.Surface((32, 32))]
        pedestrian.get_current_texture.return_value = 0
        pedestrian.is_moving_right.return_value = False
        draw_pedestrian(self.screen, pedestrian)

    def test_draw_rails(self):
        draw_rails(self.screen, [100, 200, 300], 150, 800, 600)

    def test_draw_road_texture(self):
        current_map = Mock()
        current_map.get_texture.return_value = pygame.Surface((800, 600))
        current_map.get_scaled_texture.return_value = pygame.Surface((400, 300))
        car = Mock()
        car.get_y.return_value = 100
        draw_road_texture(self.screen, current_map, car, 800)

    @patch("subprocess.Popen")
    def test_show_end_screen(self, mock_subprocess):
        with self.assertRaises(SystemExit):
            show_end_screen(self.screen, 800, 600, "Test Message", None)

    @patch("pygame.mixer.music.play")
    @patch("pygame.mixer.music.load")
    def test_show_traffic_light(self, mock_music_load, mock_music_play):
        show_traffic_light(self.screen, 800, 600)

if __name__ == "__main__":
    unittest.main()
