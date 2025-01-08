import unittest
from unittest.mock import Mock, patch
import pygame
from cr_logic import (
    handle_terrain,
    is_finish_line,
    update_checkpoints,
    check_lap_completion,
    determine_leader,
    handle_enemy_ai,
)

class TestLogicFunctions(unittest.TestCase):
    @patch("logic.logic.is_slipping_terrain")
    @patch("logic.logic.is_non_slipping_terrain")
    def test_handle_terrain(self, mock_non_slipping, mock_slipping):
        entity = Mock()
        entity.get_x.return_value = 50
        entity.get_y.return_value = 50
        entity.wheels.is_wheels_slipping.return_value = False

        mock_slipping.return_value = True
        mock_non_slipping.return_value = False
        handle_terrain(entity)
        entity.wheels.slip.assert_called_once()

        entity.wheels.reset_mock()

        mock_slipping.return_value = False
        mock_non_slipping.return_value = True
        entity.wheels.is_wheels_slipping.return_value = True
        handle_terrain(entity)
        entity.wheels.reset_speed.assert_called_once()

    @patch("logic.logic.is_finish_line")
    def test_is_finish_line(self, mock_is_finish_line):
        mock_is_finish_line.return_value = True
        self.assertTrue(is_finish_line(10, 20))

    @patch("logic.logic.update_checkpoints")
    def test_update_checkpoints(self, mock_update_checkpoints):
        checkpoints = [False, False, False]
        def mock_update(x, y, c):
            c[0] = True
        mock_update_checkpoints.side_effect = mock_update
        update_checkpoints(10, 20, checkpoints)
        self.assertTrue(checkpoints[0])

    @patch("logic.play_sound_effect")
    @patch("logic.logic.is_finish_line")
    def test_check_lap_completion(self, mock_is_finish_line, mock_play_sound_effect):
        car = Mock()
        car.get_x.return_value = 10
        car.get_y.return_value = 20
        car.get_name.return_value = "Car1"
        car.get_type.return_value = "Supercar"

        checkpoints = [True, True, True]
        laps_completed = {"Car1": 0}

        mock_is_finish_line.return_value = True
        check_lap_completion(car, checkpoints, laps_completed)

        self.assertEqual(laps_completed["Car1"], 1)
        self.assertTrue(checkpoints[0])
        self.assertFalse(any(checkpoints[1:]))
        car.nitro.restore_nitro.assert_called_once()
        mock_play_sound_effect.assert_called_once()

    @patch("logic.check_collision")
    @patch("logic.determine_enemy_keys")
    def test_handle_enemy_ai(self, mock_determine_enemy_keys, mock_check_collision):
        enemy = Mock()
        player = Mock()
        enemy_checkpoints = [False, False, False]
        laps_completed = {"Enemy": 0}

        enemy.get_x.return_value = 10
        enemy.get_y.return_value = 20
        player.get_x.return_value = 15
        player.get_y.return_value = 25

        mock_determine_enemy_keys.return_value = {
            pygame.K_w: True,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: True
        }

        mock_check_collision.return_value = (10.0, 20.0)

        handle_enemy_ai(enemy, player, enemy_checkpoints, laps_completed)

        enemy.move.assert_called_once_with({
            pygame.K_w: True,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: True
        })
        enemy.set_x.assert_called_once_with(10.0)
        enemy.set_y.assert_called_once_with(20.0)
        self.assertEqual(laps_completed["Enemy"], 0)

if __name__ == "__main__":
    unittest.main()