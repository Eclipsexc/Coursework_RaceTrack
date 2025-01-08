import pygame
import random

class Canister:
    CANISTER_SIZE = 64
    textures_paths = [
        "C:/CourseWork/Fuel Frenzy/FFF_gas_large.png",
        "C:/CourseWork/Fuel Frenzy/FFF_gas_medium.png",
        "C:/CourseWork/Fuel Frenzy/FFF_gas_small.png",
    ]
    textures = None

    @classmethod
    def load_textures(cls):
        if cls.textures is None:
            cls.textures = [
                pygame.transform.scale(
                    pygame.image.load(path).convert_alpha(),
                    (cls.CANISTER_SIZE, cls.CANISTER_SIZE)
                ) for path in cls.textures_paths
            ]

    def __init__(self, x, y, n):
        if Canister.textures is None:
            Canister.load_textures()
        self._x = x
        self._y = y
        self.texture = Canister.textures[n]
        self.fuel_increase = [50, 35, 20][n]
        self.collected = False
        self._type = "standard"

    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value

    def get_collected(self):
        return self.collected

    def set_collected(self, value):
        self.collected = value

    def get_fuel_increase(self):
        return self.fuel_increase

    def get_type(self):
        return self._type

class RepairKitCanister(Canister):
    texture_path = "C:/CourseWork/Fuel Frenzy/FFF_gas_repair_kit.png"

    def __init__(self, x, y):
        super().__init__(x, y, 0)
        self.texture = pygame.transform.scale(
            pygame.image.load(self.texture_path).convert_alpha(),
            (self.CANISTER_SIZE, self.CANISTER_SIZE)
        )
        self.fuel_increase = 100
        self._type = "repair_kit"

class SuspiciousCanister(Canister):
    texture_path = "C:/CourseWork/Fuel Frenzy/FFF_gas_suspicious.png"

    def __init__(self, x, y, fuel_increase, speed_change, fuel_quality):
        super().__init__(x, y, 0)
        self.texture = pygame.transform.scale(
            pygame.image.load(self.texture_path).convert_alpha(),
            (self.CANISTER_SIZE, self.CANISTER_SIZE)
        )
        self.fuel_increase = fuel_increase
        self.speed_change = speed_change
        self.fuel_quality = fuel_quality
        self._type = "suspicious"

    def get_speed_change(self):
        return self.speed_change

    def get_fuel_quality(self):
        return self.fuel_quality