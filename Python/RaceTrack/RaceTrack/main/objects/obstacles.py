import pygame
import abc
import ctypes

obstacles_dll_path = r"C:/CourseWork/C++/FastCompute/x64/Release/FastCompute.dll"
obstacles_logic = ctypes.CDLL(obstacles_dll_path)

obstacles_logic.move_tumbleweed.argtypes = [
    ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_bool),
    ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float
]
obstacles_logic.move_tumbleweed.restype = None

obstacles_logic.move_minecart.argtypes = [
    ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float),
    ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_bool)
]
obstacles_logic.move_minecart.restype = None

class Obstacle:
    def __init__(self, texture_paths, x, y, hits_required, name, width=160, height=72):
        self._textures = [pygame.image.load(path).convert_alpha() for path in texture_paths]
        self._current_texture_index = 0
        self._width = width
        self._height = height
        self._texture = pygame.transform.scale(self._textures[self._current_texture_index], (self._width, self._height))
        self._name = name
        self._x = x
        self._y = y
        self._hits_required = hits_required
        self._current_hits = 0
        self._obstacle_type = "Default"
        self._is_colliding = False
        self._active = True

    def update_texture(self):
        if self._current_hits < len(self._textures):
            self._current_texture_index = self._current_hits
            self._texture = pygame.transform.scale(self._textures[self._current_texture_index], (self._width, self._height))

        if self._current_hits == len(self._textures):
            self._active = False

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_obstacle_type(self):
        return self._obstacle_type

    def set_obstacle_type(self, obstacle_type):
        self._obstacle_type = obstacle_type

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_width(self):
        return self._width

    def set_width(self, width):
        self._width = width

    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    def get_hits_required(self):
        return self._hits_required

    def set_hits_required(self, hits_required):
        self._hits_required = hits_required

    def get_current_hits(self):
        return self._current_hits

    def set_current_hits(self, current_hits):
        self._current_hits = current_hits

    def get_is_colliding(self):
        return self._is_colliding

    def set_is_colliding(self, is_colliding):
        self._is_colliding = is_colliding

    def get_active(self):
        return self._active

    def set_active(self, active):
        self._active = active

    def get_texture(self):
        return self._texture

class MovingObstacle(Obstacle, metaclass=abc.ABCMeta):
    def __init__(self, texture_paths, x, y, speed=5, hits_required=1, name="AbstractMovingObstacle", width=32, height=32):
        super().__init__(texture_paths, x, y, hits_required, name, width, height)
        self._speed = speed
        self._starting_x = x
        self._moving = True
        self._obstacle_type = "Moving"

    @abc.abstractmethod
    def move(self):
        pass

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        self._speed = speed

    def get_starting_x(self):
        return self._starting_x

    def set_starting_x(self, starting_x):
        self._starting_x = starting_x

    def is_moving(self):
        return self._moving

    def reset_moving(self):
        self._moving = True

class Tumbleweed(MovingObstacle):
    def __init__(self, x, y, speed=5, hits_required=1, name="Tumbleweed"):
        texture_paths = ["C:/Coursework/Obstacles/Tumbleweed.png"]
        super().__init__(texture_paths, x, y, speed, hits_required, name)

    def move(self):
        if not self._moving:
            return

        x_c = ctypes.c_float(self._x)
        moving_c = ctypes.c_bool(self._moving)

        obstacles_logic.move_tumbleweed(
            ctypes.byref(x_c), ctypes.byref(moving_c),
            self._speed, self._starting_x, 180.0, 570.0
        )

        self._x = x_c.value
        self._moving = moving_c.value


class Minecart(MovingObstacle):
    def __init__(self, x, y, speed=5, hits_required=1, name="Minecart", width=32, height=32):
        texture_paths = [
            "C:/Coursework/Obstacles/minecart.png",
            "C:/Coursework/Obstacles/broken_minecart.png"
        ]
        super().__init__(texture_paths, x, y, speed, hits_required, name, width, height)

    def move(self):
        if self._current_hits == 0:
            x_c = ctypes.c_float(self._x)
            speed_c = ctypes.c_float(self._speed)
            is_active_c = ctypes.c_bool(self._active)

            obstacles_logic.move_minecart(
                ctypes.byref(x_c), ctypes.byref(speed_c),
                self._current_hits, self._hits_required,
                180.0, 570.0, ctypes.byref(is_active_c)
            )

            self._x = x_c.value
            self._speed = speed_c.value
            self._active = is_active_c.value

    def update_texture(self):
        super().update_texture()
        if self._current_hits == 1:
            self._speed = 0
        if self._current_hits >= self._hits_required:
            self.set_active(False)