import ctypes
import pygame

dll_path = r"C:\\CourseWork\\C++\\FastCompute\\x64\\Release\\FastCompute.dll"
cpp_dll = ctypes.CDLL(dll_path)

cpp_dll.move_car.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_bool * 4
]

cpp_dll.boost_bolide.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_bool
]

cpp_dll.use_nitro.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_bool
]

cpp_dll.restore_nitro.argtypes = [ctypes.POINTER(ctypes.c_float)]

cpp_dll.slip_wheels.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_float,
    ctypes.c_bool,
    ctypes.POINTER(ctypes.c_bool)
]

cpp_dll.consume_fuel.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_float
]

cpp_dll.consume_nitro.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_float
]

cpp_dll.adjust_speed.argtypes = [
    ctypes.c_float,
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_float)
]

cpp_dll.adjust_fuel_level.argtypes = [
    ctypes.c_float,
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_float)
]

cpp_dll.attempt_repair.argtypes = [
    ctypes.c_float,
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_float)
]

class Car:
    SPRITE_WIDTH = SPRITE_HEIGHT = 32
    TARGET_WIDTH = TARGET_HEIGHT = 52

    class Engine:
        def __init__(self, engine_sound_path, idle_sound_path):
            self._engine_sound_path = engine_sound_path
            self._idle_sound_path = idle_sound_path
            self._current_sound = None

        def play_engine_sound(self, sound_path, volume=0.3):
            if sound_path and pygame.mixer.get_init():
                if self._current_sound != sound_path:
                    self.stop_engine_sound()
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(volume)
                    sound.play(loops=-1)
                    self._current_sound = sound_path

        def stop_engine_sound(self):
            if self._current_sound and pygame.mixer.get_init():
                pygame.mixer.stop()
                self._current_sound = None

    class Wheels:
        def __init__(self, slipping_sound_path):
            self._slipping_sound_path = slipping_sound_path
            self._wheels_slipping = ctypes.c_bool(False)

        def play_wheels_sound(self, volume=0.5):
            if not self._slipping_sound_path or not pygame.mixer.get_init():
                return
            sound = pygame.mixer.Sound(self._slipping_sound_path)
            sound.set_volume(volume)
            sound.play(loops=-1)

        def slip(self, speed, default_speed, is_good_on_dirt):
            speed_c = ctypes.c_float(speed)
            cpp_dll.slip_wheels(
                ctypes.byref(speed_c),
                default_speed,
                is_good_on_dirt,
                ctypes.byref(self._wheels_slipping)
            )
            return speed_c.value

        def is_wheels_slipping(self):
            return self._wheels_slipping.value

        def set_wheels_slipping(self, value):
            self._wheels_slipping.value = value

    def __init__(self, textures_path, sprite_height, x, y, speed, good_on_dirt, car_type, ability_name, engine_sound_path, slipping_sound_path):
        self._textures_path = textures_path
        self._sprite_height = sprite_height
        self._x = x
        self._y = y
        self._speed = ctypes.c_float(speed)
        self.default_speed = speed
        self.current_texture = 3
        self.good_on_dirt = good_on_dirt
        self._type = car_type
        self._ability_name = ability_name
        self.textures = self._load_textures()
        self._name = f"{self._type}_{self._sprite_height}"
        self.engine = self.Engine(engine_sound_path, "C:/CourseWork/music/engine_running.mp3")
        self.wheels = self.Wheels(slipping_sound_path)

    def _load_textures(self):
        sprite_sheet = pygame.image.load(self._textures_path).convert_alpha()
        return [
            pygame.transform.scale(
                sprite_sheet.subsurface(
                    pygame.Rect(i * self.SPRITE_WIDTH, self._sprite_height * self.SPRITE_HEIGHT, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)
                ),
                (self.TARGET_WIDTH, self.TARGET_HEIGHT)
            )
            for i in range(4)
        ]

    def update_sounds(self, keys):
        if self.wheels.is_wheels_slipping():
            self.engine.stop_engine_sound()
            self.wheels.play_wheels_sound(volume=0.2)
        else:
            self.engine.play_engine_sound(
                self.engine._engine_sound_path if any(keys[key] for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]) else self.engine._idle_sound_path,
                volume=0.3
            )

    def move(self, keys):
        self.update_sounds(keys)

        prev_x, prev_y = self._x, self._y
        keys_array = (ctypes.c_bool * 4)(keys[pygame.K_w], keys[pygame.K_d], keys[pygame.K_s], keys[pygame.K_a])
        x_c = ctypes.c_float(self._x)
        y_c = ctypes.c_float(self._y)
        current_texture_c = ctypes.c_int(self.current_texture)
        cpp_dll.move_car(ctypes.byref(x_c), ctypes.byref(y_c), self.get_speed(), ctypes.byref(current_texture_c), keys_array)
        self._x = x_c.value
        self._y = y_c.value
        self.current_texture = current_texture_c.value
        return prev_x, prev_y

    def get_sprite_height(self):
        return self._sprite_height

    def set_sprite_height(self, value):
        self._sprite_height = value
        self.textures = self._load_textures()
        self._name = f"{self._type}_{self._sprite_height}"

    def get_speed(self):
        return self._speed.value

    def set_speed(self, value):
        self._speed.value = value

    def get_default_speed(self):
        return self.default_speed

    def get_type(self):
        return self._type

    def get_ability_name(self):
        return self._ability_name

    def get_current_texture(self):
        return self.textures[self.current_texture]

    def get_name(self):
        return self._name

    def is_good_on_dirt(self):
        return self.good_on_dirt

    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value

    def get_textures_path(self):
        return self._textures_path

    def get_sprite_dimensions(self):
        return self.SPRITE_WIDTH, self.SPRITE_HEIGHT

class CarWithFuel(Car):
    SPRITE_WIDTH = SPRITE_HEIGHT = 16
    TARGET_WIDTH = TARGET_HEIGHT = 52

    class FuelTank:
        def __init__(self, fuel_capacity, fuel_level):
            self._fuel_capacity = fuel_capacity
            self._fuel_level = fuel_level

        def get_fuel_level(self):
            return self._fuel_level

        def set_fuel_level(self, value):
            self._fuel_level = max(0, min(value, self._fuel_capacity))

        def is_empty(self):
            return self._fuel_level == 0

    class GasolineEngine(Car.Engine):
        def __init__(self, fuel_tank, consumption_rate, engine_sound_path, idle_sound_path):
            super().__init__(engine_sound_path, idle_sound_path)
            self._fuel_tank = fuel_tank
            self._consumption_rate = consumption_rate

        def get_consumption_rate(self):
            return self._consumption_rate

        def set_consumption_rate(self, value):
            self._consumption_rate = max(0, value)

        def consume_fuel(self):
            fuel_level_c = ctypes.c_float(self._fuel_tank._fuel_level)
            consumption_rate_c = ctypes.c_float(self._consumption_rate)

            cpp_dll.consume_fuel(ctypes.byref(fuel_level_c), consumption_rate_c)
            self._fuel_tank._fuel_level = fuel_level_c.value

    def __init__(self, x, y, sprite_height):
        super().__init__(
            textures_path="C:/CourseWork/Cars/CarWithFuel_Sprites.png",
            sprite_height=sprite_height,
            x=x,
            y=y,
            speed=5,
            good_on_dirt=None,
            car_type="CarWithFuel",
            ability_name="Пробитий бензобак",
            engine_sound_path="C:/CourseWork/music/carwithfuel_engine.mp3",
            slipping_sound_path=None
        )
        self.current_texture = 2
        self.fuel_tank = self.FuelTank(fuel_capacity=100, fuel_level=100)
        self.engine = self.GasolineEngine(
            fuel_tank=self.fuel_tank,
            consumption_rate=0.0,
            engine_sound_path="C:/CourseWork/music/carwithfuel_engine.mp3",
            idle_sound_path="C:/CourseWork/music/engine_running.mp3"
        )
        self.low_fuel_sound_path = "C:/CourseWork/music/low_fuel.mp3"
        self.engine_fail_sound_path = "C:/CourseWork/music/engine_fail.mp3"

    def can_drive(self):
        return not self.fuel_tank.is_empty()

    def update_sounds(self, keys):
        if self.fuel_tank.get_fuel_level() <= 35:
            self.engine.play_engine_sound(self.low_fuel_sound_path, volume=0.5)
        else:
            super().update_sounds(keys)

    def move(self, keys):
        if not self.can_drive():
            self.engine.stop_engine_sound()
            self.engine.play_engine_sound(self.engine_fail_sound_path, volume=0.5)
            return self.get_x(), self.get_y()

        prev_x, prev_y = super().move(keys)
        self.engine.consume_fuel()
        self.update_sounds(keys)
        return prev_x, prev_y

class Supercar(Car):
    class Nitro:
        def __init__(self, capacity, level, consumption_rate, nitro_sound_path):
            self._capacity = capacity
            self._level = level
            self._consumption_rate = consumption_rate
            self._nitro_sound_path = nitro_sound_path
            self._current_sound = None

        def get_nitro_level(self):
            return self._level

        def set_nitro_level(self, value):
            self._level = max(0, min(value, self._capacity))

        def consume_nitro(self):
            nitro_level_c = ctypes.c_float(self._level)
            consumption_rate_c = ctypes.c_float(self._consumption_rate)

            cpp_dll.consume_nitro(ctypes.byref(nitro_level_c), consumption_rate_c)
            self._level = nitro_level_c.value

        def restore_nitro(self):
            nitro_level_c = ctypes.c_float(self._level)
            cpp_dll.restore_nitro(ctypes.byref(nitro_level_c))
            self._level = nitro_level_c.value

        def is_empty(self):
            return self._level == 0

        def play_nitro_sound(self, volume=0.2):
            if self._nitro_sound_path and pygame.mixer.get_init():
                if not self._current_sound:
                    sound = pygame.mixer.Sound(self._nitro_sound_path)
                    sound.set_volume(volume)
                    sound.play(loops=-1)
                    self._current_sound = sound

        def stop_nitro_sound(self):
            if self._current_sound and pygame.mixer.get_init():
                self._current_sound.stop()
                self._current_sound = None

    def __init__(self, x, y, sprite_height):
        super().__init__(
            textures_path="C:/CourseWork/Cars/Supercar_Sprites.png",
            sprite_height=sprite_height,
            x=x,
            y=y,
            speed=4,
            good_on_dirt=True,
            car_type="Supercar",
            ability_name="Нітро",
            engine_sound_path="C:/CourseWork/music/supercar_engine.mp3",
            slipping_sound_path="C:/CourseWork/music/supercar_slipping.mp3"
        )
        self.nitro = self.Nitro(
            capacity=100, 
            level=100, 
            consumption_rate=0.5, 
            nitro_sound_path="C:/CourseWork/music/nitro.mp3"
        )

    def use_nitro(self, keys):
        if self.wheels.is_wheels_slipping():
            return

        nitro_key_pressed = keys[pygame.K_RCTRL]

        if nitro_key_pressed and not self.nitro.is_empty():
            speed_c = ctypes.c_float(self.get_speed())
            nitro_level_c = ctypes.c_float(self.nitro.get_nitro_level())

            cpp_dll.use_nitro(
                ctypes.byref(speed_c), self.default_speed, ctypes.byref(nitro_level_c), nitro_key_pressed
            )

            self.set_speed(speed_c.value)
            self.nitro.set_nitro_level(nitro_level_c.value)
            self.nitro.consume_nitro()
        elif not nitro_key_pressed:
            self.set_speed(self.default_speed)

        self.update_sounds(keys)

    def update_sounds(self, keys):
        if keys[pygame.K_RCTRL] and not self.nitro.is_empty():
            self.nitro.play_nitro_sound(volume=0.2)
        else:
            self.nitro.stop_nitro_sound()
            super().update_sounds(keys)


class Bolide(Car):
    def __init__(self, x, y, sprite_height):
        super().__init__(
            textures_path="C:/CourseWork/Cars/Bolide_Sprites.png",
            sprite_height=sprite_height,
            x=x,
            y=y,
            speed=5,
            good_on_dirt=False,
            car_type="Bolide",
            ability_name="Розгін",
            engine_sound_path="C:/CourseWork/music/bolide_engine.mp3",
            slipping_sound_path="C:/CourseWork/music/bolide_slipping.mp3"
        )
        self.last_position_change = (x, y)
        self.single_key_pressed = False

    def boost(self):
        if self.wheels.is_wheels_slipping():
            return

        speed_c = ctypes.c_float(self.get_speed())
        last_x_c = ctypes.c_float(self.last_position_change[0])
        last_y_c = ctypes.c_float(self.last_position_change[1])
        cpp_dll.boost_bolide(
            ctypes.byref(speed_c),
            self.default_speed,
            self._x,  
            self._y,
            ctypes.byref(last_x_c),
            ctypes.byref(last_y_c),
            self.single_key_pressed
        )
        self.set_speed(speed_c.value)
        self.last_position_change = (last_x_c.value, last_y_c.value)

    def move(self, keys):
        self.single_key_pressed = sum([keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]]) == 1
        prev_x, prev_y = super().move(keys)
        self.boost()
        return prev_x, prev_y