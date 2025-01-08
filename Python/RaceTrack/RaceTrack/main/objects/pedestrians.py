import pygame
import ctypes

pedestrians_lib = ctypes.CDLL(r"C:/CourseWork/C++/FastCompute/x64/Release/FastCompute.dll")

pedestrians_lib.calculate_direction.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float,
                                                ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
pedestrians_lib.move_horizontal.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_float, ctypes.c_float,
                                            ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
pedestrians_lib.move_diagonal.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float),
                                          ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float,
                                          ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_float),
                                          ctypes.POINTER(ctypes.c_float), ctypes.c_float, ctypes.POINTER(ctypes.c_bool),
                                          ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

class Pedestrian:
    def __init__(self, texture_path, mirrored_texture_path, name, x, y, x_min, x_max):
        self._textures = [
            pygame.transform.scale(
                pygame.image.load(texture_path).subsurface(pygame.Rect(i * 32, 0, 32, 32)),
                (64, 64)
            )
            for i in range(3)
        ]
        self._mirrored_textures = [
            pygame.transform.scale(
                pygame.image.load(mirrored_texture_path).subsurface(pygame.Rect(i * 32, 0, 32, 32)),
                (64, 64)
            )
            for i in range(3)
        ] if mirrored_texture_path else None
        self._name = name
        self._x = ctypes.c_float(x)
        self._y = ctypes.c_float(y)
        self._x_min = x_min
        self._x_max = x_max
        self._current_texture = 0
        self._moving_right = ctypes.c_bool(True)
        self._animation_counter = 0

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_x(self):
        return self._x.value

    def set_x(self, x):
        self._x = ctypes.c_float(x)

    def get_y(self):
        return self._y.value

    def set_y(self, y):
        self._y = ctypes.c_float(y)

    def get_position(self):
        return self._x.value, self._y.value

    def set_position(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def get_textures(self):
        return self._textures

    def get_mirrored_textures(self):
        return self._mirrored_textures

    def get_current_texture(self):
        return self._current_texture

    def set_current_texture(self, texture_index):
        self._current_texture = texture_index

    def is_moving_right(self):
        return self._moving_right.value

    def set_moving_right(self, moving_right):
        self._moving_right.value = moving_right

    def update_animation(self):
        self._animation_counter = (self._animation_counter + 1) % 15
        if self._animation_counter == 0:
            self._current_texture = (self._current_texture + 1) % 3

    def move(self):
        pedestrians_lib.move_horizontal(ctypes.byref(self._x), self._x_min, self._x_max,
                                        ctypes.byref(self._moving_right),
                                        ctypes.byref(ctypes.c_int(self._animation_counter)),
                                        ctypes.byref(ctypes.c_int(self._current_texture)))
        self.update_animation()


class StandingPedestrian(Pedestrian):
    def __init__(self, texture_path, name, x, y):
        super().__init__(texture_path, None, name, x, y, x, x)

    def move(self):
        self.update_animation()


class DiagonalPedestrian(Pedestrian):
    def __init__(self, texture_path, mirrored_texture_path, name, x, y, target_x, target_y):
        super().__init__(texture_path, mirrored_texture_path, name, x, y, x, x)
        self._start_x = x
        self._start_y = y
        self._target_x = target_x
        self._target_y = target_y
        self._moving_to_target = ctypes.c_bool(True)
        self._speed = ctypes.c_float(1.0)
        self._dx = ctypes.c_float(0.0)
        self._dy = ctypes.c_float(0.0)
        pedestrians_lib.calculate_direction(self._start_x, self._start_y, self._target_x, self._target_y,
                                            ctypes.byref(self._dx), ctypes.byref(self._dy))

    def get_target_position(self):
        return self._target_x, self._target_y

    def set_target_position(self, target_x, target_y):
        self._target_x = target_x
        self._target_y = target_y
        pedestrians_lib.calculate_direction(self._start_x, self._start_y, self._target_x, self._target_y,
                                            ctypes.byref(self._dx), ctypes.byref(self._dy))

    def move(self):
        pedestrians_lib.move_diagonal(ctypes.byref(self._x), ctypes.byref(self._y),
                                      self._start_x, self._start_y, self._target_x, self._target_y,
                                      ctypes.byref(self._moving_to_target),
                                      ctypes.byref(self._dx), ctypes.byref(self._dy),
                                      self._speed.value, ctypes.byref(self._moving_right),
                                      ctypes.byref(ctypes.c_int(self._animation_counter)),
                                      ctypes.byref(ctypes.c_int(self._current_texture)))
        self.update_animation()