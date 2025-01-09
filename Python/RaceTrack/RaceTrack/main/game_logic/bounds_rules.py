import ctypes
from abc import ABC, abstractmethod

bounds_rules = ctypes.CDLL(r"C:\CourseWork\C++\FastCompute\x64\Release\FastCompute.dll")

bounds_rules.check_within_cr_bounds.argtypes = [ctypes.c_float, ctypes.c_float]
bounds_rules.check_within_cr_bounds.restype = ctypes.c_bool

bounds_rules.check_within_ff1_bounds.argtypes = [ctypes.c_float, ctypes.c_float]
bounds_rules.check_within_ff1_bounds.restype = ctypes.c_bool

bounds_rules.check_within_ff2_bounds.argtypes = [ctypes.c_float, ctypes.c_float]
bounds_rules.check_within_ff2_bounds.restype = ctypes.c_bool


class BoundsRule(ABC):
    def apply_bounds(self, car, prev_x, prev_y):
        x, y = car.get_x(), car.get_y()
        if not self.is_within_bounds(x, y):
            self.reset_position(car, prev_x, prev_y)

    @abstractmethod
    def is_within_bounds(self, x, y):
        raise NotImplementedError("Subclasses must implement the is_within_bounds method.")

    def reset_position(self, car, prev_x, prev_y):
        car.set_x(prev_x)
        car.set_y(prev_y)


class CRBoundsRule(BoundsRule):
    def is_within_bounds(self, x, y):
        return bounds_rules.check_within_cr_bounds(x, y)

class FF1BoundsRule(BoundsRule):
    def apply_bounds(self, car, prev_x, prev_y):
        x, y = car.get_x(), car.get_y()
        if y > 2500:
            car.set_y(0)
        elif not self.is_within_bounds(x, y):
            self.reset_position(car, prev_x, prev_y)

    def is_within_bounds(self, x, y):
        return bounds_rules.check_within_ff1_bounds(x, y)


class FF2BoundsRule(BoundsRule):
    def is_within_bounds(self, x, y):
        return bounds_rules.check_within_ff2_bounds(x, y)


def get_bounds_rule_for_map(game_map):
    map_name = game_map.get_name()
    if map_name == "Classic Race":
        return CRBoundsRule()
    elif map_name == "Fuel Frenzy 1":
        return FF1BoundsRule()
    elif map_name == "Fuel Frenzy 2":
        return FF2BoundsRule()
    else:
        raise ValueError(f"Невідомий тип карти: {map_name}")