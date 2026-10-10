from __future__ import annotations

import random
from typing import Iterable

from .models import Ball, Pocket, Vector2D


class BilliardsWorld:
    """Simulation state and physics update loop."""

    DEFAULT_COLORS = (
        "red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"
    )

    def __init__(self, width: int = 600, height: int = 600, pocket_radius: int = 25):
        self.width = width
        self.height = height
        self.balls: list[Ball] = []
        margin = 10
        r = pocket_radius
        self.pockets = [
            Pocket(Vector2D(margin + r, margin + r), r),
            Pocket(Vector2D(width - margin - r, margin + r), r),
            Pocket(Vector2D(margin + r, height - margin - r), r),
            Pocket(Vector2D(width - margin - r, height - margin - r), r),
        ]

    def reset_random_balls(
        self,
        count: int,
        *,
        min_radius: float = 10,
        max_radius: float = 20,
        min_speed: float = -3,
        max_speed: float = 3,
        seed: int | None = None,
    ) -> None:
        if count <= 0:
            raise ValueError("count must be positive")

        rng = random.Random(seed)
        self.balls = []
        for _ in range(count):
            radius = rng.uniform(min_radius, max_radius)
            x = rng.uniform(max(50, radius), self.width - max(50, radius))
            y = rng.uniform(max(50, radius), self.height - max(50, radius))
            velocity = Vector2D(rng.uniform(min_speed, max_speed), rng.uniform(min_speed, max_speed))
            self.balls.append(
                Ball(
                    position=Vector2D(x, y),
                    velocity=velocity,
                    radius=radius,
                    color=rng.choice(self.DEFAULT_COLORS),
                )
            )

    def add_balls(self, balls: Iterable[Ball]) -> None:
        self.balls.extend(balls)

    def step(self) -> None:
        for ball in self.balls:
            ball.move()
            ball.bounce_off_walls(self.width, self.height)

        for i, first in enumerate(self.balls):
            for second in self.balls[i + 1 :]:
                if first.overlaps(second):
                    first.resolve_elastic_collision(second)

        survivors: list[Ball] = []
        for ball in self.balls:
            captured = any(pocket.captures(ball) for pocket in self.pockets)
            if captured:
                ball.active = False
            else:
                survivors.append(ball)
        self.balls = survivors
