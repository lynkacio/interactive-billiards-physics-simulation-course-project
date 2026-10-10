from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class Vector2D:
    """Small 2D vector helper used for position and velocity calculations."""

    x: float
    y: float

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def dot(self, other: "Vector2D") -> float:
        return self.x * other.x + self.y * other.y

    def magnitude_squared(self) -> float:
        return self.dot(self)

    def magnitude(self) -> float:
        return math.sqrt(self.magnitude_squared())


@dataclass
class Ball:
    position: Vector2D
    velocity: Vector2D
    radius: float
    color: str = "blue"
    active: bool = True

    def move(self) -> None:
        if self.active:
            self.position = self.position + self.velocity

    def bounce_off_walls(self, width: float, height: float) -> None:
        """Keep the ball inside the table and reflect velocity at boundaries."""
        if not self.active:
            return

        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x *= -1
        elif self.position.x + self.radius > width:
            self.position.x = width - self.radius
            self.velocity.x *= -1

        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y *= -1
        elif self.position.y + self.radius > height:
            self.position.y = height - self.radius
            self.velocity.y *= -1

    def overlaps(self, other: "Ball") -> bool:
        if not self.active or not other.active:
            return False
        separation = other.position - self.position
        combined_radius = self.radius + other.radius
        return separation.magnitude_squared() < combined_radius * combined_radius

    def resolve_elastic_collision(self, other: "Ball") -> None:
        """Resolve an equal-mass 2D elastic collision along the collision normal."""
        if not self.active or not other.active:
            return

        delta = other.position - self.position
        distance_sq = delta.magnitude_squared()
        if distance_sq == 0:
            return

        relative_other = other.velocity - self.velocity
        relative_self = self.velocity - other.velocity

        self_factor = relative_other.dot(delta) / distance_sq
        other_factor = relative_self.dot(delta) / distance_sq

        self.velocity = self.velocity + delta * self_factor
        other.velocity = other.velocity + delta * other_factor

        # Separate overlapping balls so the next frame does not immediately
        # detect the same collision again.
        distance = math.sqrt(distance_sq)
        overlap = (self.radius + other.radius) - distance
        if overlap > 0:
            normal = delta * (1.0 / distance)
            correction = normal * (overlap / 2.0)
            self.position = self.position - correction
            other.position = other.position + correction


@dataclass(frozen=True)
class Pocket:
    position: Vector2D
    radius: float

    def captures(self, ball: Ball) -> bool:
        return (ball.position - self.position).magnitude() < self.radius
