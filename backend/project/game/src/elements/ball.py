import math
import random
import time
import asyncio
from dataclasses import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def multiply_scalar(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def clone(self):
        return Vector3(self.x, self.y, self.z)


class Ball:
    def __init__(self):
        self.ARENA_WIDTH = 24.0
        self.ARENA_DEPTH = 44.0
        self.PADDLE_WIDTH = 6.0
        self.PADDLE_DEPTH = 7.0
        self.BALL_RADIUS = 0.3

        self.conf = {
            "speed": {
                "initialMin": 0.5,
                "initialMax": 0.6,
                "max": 1.4,
                "incrementFactor": 1.03,
                "deltaFactor": 30,
            }
        }

        self.position = Vector3(0, 2.7, 0)
        self.velocity = self._random_initial_velocity()
        self.is_falling = False
        self.elapsed_time = 0
        self.bounces = 0
        self.last_collision = {"side": None, "time": 0}
        self.collision_cooldown = 0.1
        self.isResetting = False

    def _random_initial_velocity(self):
        while True:
            x = random.uniform(
                self.conf["speed"]["initialMin"], self.conf["speed"]["initialMax"]
            ) * random.choice([-1, 1])

            y = random.uniform(
                self.conf["speed"]["initialMin"], self.conf["speed"]["initialMax"]
            ) * random.choice([-1, 1])

            if abs(x) > 0.01 or abs(y) > 0.01:
                break
        self.bounces = 0
        initial_speed = math.sqrt(x * x + y * y)
        self.bounces_needed = math.log(
            self.conf["speed"]["max"] / initial_speed
        ) / math.log(self.conf["speed"]["incrementFactor"])

        return Vector3(x, 0, y)

    def check_collision(self, paddle_x_left, paddle_x_right):

        if self.is_falling:
            return None, None

        if (
            self.position.z < -self.ARENA_DEPTH / 2 + 2
            or self.position.z > self.ARENA_DEPTH / 2 - 2
        ):
            return None, None

        half_width = self.ARENA_WIDTH / 2
        left_paddle_z = -self.ARENA_DEPTH / 2 + self.PADDLE_DEPTH / 2
        right_paddle_z = self.ARENA_DEPTH / 2 - self.PADDLE_DEPTH / 2

        if self.position.x >= half_width - self.BALL_RADIUS:
            return "top", None
        if self.position.x <= -(half_width - self.BALL_RADIUS):
            return "bottom", None

        if self.position.z <= left_paddle_z + self.BALL_RADIUS:
            if (
                abs(self.position.x - paddle_x_left)
                <= self.PADDLE_WIDTH / 2 + self.BALL_RADIUS
            ):
                return None, "left"

        if self.position.z >= right_paddle_z - self.BALL_RADIUS:
            if (
                abs(self.position.x - paddle_x_right)
                <= self.PADDLE_WIDTH / 2 + self.BALL_RADIUS
            ):
                return None, "right"

        return None, None

    def bounce(self, side, paddle_pos=None):
        current_time = time.time()
        if (
            side == self.last_collision["side"]
            and current_time - self.last_collision["time"] < self.collision_cooldown
        ):
            return

        self.last_collision["side"] = side
        self.last_collision["time"] = current_time

        if side in ["left", "right"]:
            if paddle_pos is not None:
                relative_position = self.position.x - paddle_pos
                normalized_position = relative_position / (self.PADDLE_WIDTH / 2)
                max_angle = math.pi / 4
                new_angle = normalized_position * max_angle

                current_speed = self.velocity.length()
                y_direction = 1 if side == "left" else -1

                self.velocity.x = current_speed * math.sin(new_angle)
                self.velocity.z = y_direction * abs(current_speed * math.cos(new_angle))

                self.bounces += 1
                if self.bounces < self.bounces_needed:
                    current_speed *= self.conf["speed"]["incrementFactor"]
                    self.velocity = self.velocity.multiply_scalar(
                        self.conf["speed"]["incrementFactor"]
                    )

        elif side in ["top", "bottom"]:
            self.velocity.x *= -1

    def update(self, delta_time):
        if self.isResetting:
            return
        elif self.is_falling:
            if self.position.y <= -1:
                self.velocity.y *= 0.7
                self.velocity.x *= 0.85
                self.velocity.z *= 0.85

            scaled_velocity = self.velocity.multiply_scalar(
                delta_time * self.conf["speed"]["deltaFactor"]
            )
            self.position.add(scaled_velocity)

            self.elapsed_time += delta_time
            if self.elapsed_time >= 1.2:
                side = "right" if self.position.z < 0 else "left"
                return f"point_scored_{side}"
        else:
            scaled_velocity = self.velocity.multiply_scalar(
                delta_time * self.conf["speed"]["deltaFactor"]
            )
            self.position.add(scaled_velocity)
            if (
                self.position.z < -self.ARENA_DEPTH / 2 - 0.2
                or self.position.z > self.ARENA_DEPTH / 2 + 0.2
            ):
                self.start_falling()
        return "continue"

    def start_falling(self):
        if not self.is_falling:
            self.elapsed_time = 0
            self.is_falling = True
            self.velocity = self.velocity.multiply_scalar(0.7)
            self.velocity.y = -0.2

    def reset(self):
        async def _reset():
            self.isResetting = True
            self.position = Vector3(0, 2.7, 0)
            await asyncio.sleep(1)
            self.elapsed_time = 0
            self.is_falling = False
            self.position = Vector3(0, 2.7, 0)
            self.velocity = self._random_initial_velocity()
            self.isResetting = False

        asyncio.create_task(_reset())

    def getCurrentState(self):
        return {
            "pos": {
                "x": float(self.position.x),
                "y": float(self.position.y),
                "z": float(self.position.z),
            },
            "vel": {
                "x": float(self.velocity.x),
                "y": float(self.velocity.y),
                "z": float(self.velocity.z),
            },
        }
