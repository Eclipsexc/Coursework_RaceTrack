import unittest
from unittest.mock import patch
import pygame
from ff_spawn_objects import (
    generate_random_canister_x,
    generate_random_coordinates,
    generate_specific_y,
    generate_specific_x,
    generate_random_x,
    generate_random_y,
    create_random_canisters,
    spawn_suspicious_canisters,
    generate_repair_kit_canister,
    generate_suspicious_canister,
)

class TestSpawnObjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init() 
        pygame.display.set_mode((800, 600))  

    @classmethod
    def tearDownClass(cls):
        pygame.quit() 
    def test_generate_random_canister_x(self):
        for y in [100, 500, 1600, 2500]:
            x = generate_random_canister_x(y)
            self.assertGreaterEqual(x, 225)
            self.assertLessEqual(x, 506)

    def test_generate_random_coordinates(self):
        result = generate_random_coordinates(1.0)
        self.assertIsNotNone(result)
        x, y = result
        self.assertGreaterEqual(x, 225)
        self.assertLessEqual(x, 506)
        self.assertGreaterEqual(y, 301)
        self.assertLessEqual(y, 2400)

    def test_generate_specific_y(self):
        choices = [50, 100, 150, 200]
        y = generate_specific_y(choices)
        self.assertIn(y, choices)

    def test_generate_specific_x(self):
        choices = [225, 300, 400, 500]
        x = generate_specific_x(choices)
        self.assertIn(x, choices)

    def test_generate_random_x(self):
        x = generate_random_x()
        self.assertGreaterEqual(x, 180)
        self.assertLessEqual(x, 570)

    def test_generate_random_y(self):
        y = generate_random_y()
        self.assertGreaterEqual(y, 50)
        self.assertLessEqual(y, 2400)

    def test_create_random_canisters(self):
        count = 10
        canisters = create_random_canisters(count)
        self.assertEqual(len(canisters), count)
        for canister in canisters:
            self.assertGreaterEqual(canister.get_x(), 225)
            self.assertLessEqual(canister.get_x(), 506)

    def test_spawn_suspicious_canisters(self):
        canisters = []
        max_canisters = 5
        spawn_suspicious_canisters(max_canisters, canisters)
        self.assertLessEqual(len(canisters), max_canisters)

    def test_generate_repair_kit_canister(self):
        repair_kit = generate_repair_kit_canister()
        self.assertIsNotNone(repair_kit)
        self.assertGreaterEqual(repair_kit.get_x(), 225)
        self.assertLessEqual(repair_kit.get_x(), 506)

    def test_generate_suspicious_canister(self):
        suspicious_canister = generate_suspicious_canister()
        if suspicious_canister is not None:
            self.assertGreaterEqual(suspicious_canister.get_x(), 225)
            self.assertLessEqual(suspicious_canister.get_x(), 506)

if __name__ == "__main__":
    unittest.main()