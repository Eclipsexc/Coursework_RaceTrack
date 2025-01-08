import unittest
from unittest.mock import Mock, patch
from ff_logic import (
    update_lap,
    switch_map,
    update_map_objects,
)
from maps import MapFF
import pygame


class TestLogicFunctions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_update_lap(self):
        car = Mock()
        car.engine.get_consumption_rate.return_value = 0.3
        car.engine.set_consumption_rate = Mock()

        laps, lap_completed = update_lap(car, 2, True)

        self.assertEqual(laps, 3)
        self.assertFalse(lap_completed)
        car.engine.set_consumption_rate.assert_called_once_with(0.4)

    @patch("fflogic.play_music")
    def test_switch_map(self, mock_play_music):
        car = Mock()
        road_map1 = MapFF(
            texture_path="C:/CourseWork/Map/FF_map1.png",
            music_path="C:/CourseWork/music/fuel_frenzy1.mp3",
            name="Fuel Frenzy 1"
        )

        canisters, obstacles, moving_obstacles, active_rails = [], [], [], []

        new_map, bounds_rule = switch_map(
            car, road_map1, canisters, obstacles, moving_obstacles, active_rails
        )

        car.set_y.assert_called_once_with(0)
        car.engine.set_consumption_rate.assert_called_once_with(0)
        mock_play_music.assert_called_once_with(
            "C:/CourseWork/music/fuel_frenzy1.mp3", volume=0.3
        )

    @patch("fflogic.generate_tumbleweeds")
    @patch("fflogic.spawn_suspicious_canisters")
    def test_update_map_objects(self, mock_spawn_suspicious, mock_generate_tumbleweeds):
        canisters, obstacles, moving_obstacles, active_rails = [], [], [], []
        texture_paths = Mock()
        rail_positions = Mock()

        canisters, obstacles, moving_obstacles, active_rails = update_map_objects(
            4, canisters, obstacles, moving_obstacles, active_rails, texture_paths, rail_positions
        )

        mock_generate_tumbleweeds.assert_called_once()
        mock_spawn_suspicious.assert_called_once()


if __name__ == "__main__":
    unittest.main()