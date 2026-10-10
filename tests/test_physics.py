import math
import unittest

from billiards_sim.models import Ball, Pocket, Vector2D
from billiards_sim.world import BilliardsWorld


class VectorTests(unittest.TestCase):
    def test_vector_operations(self):
        a = Vector2D(2, 3)
        b = Vector2D(4, 1)
        self.assertEqual(a + b, Vector2D(6, 4))
        self.assertEqual(a - b, Vector2D(-2, 2))
        self.assertEqual(a.dot(b), 11)
        self.assertAlmostEqual(Vector2D(3, 4).magnitude(), 5.0)


class PhysicsTests(unittest.TestCase):
    def test_wall_bounce(self):
        ball = Ball(Vector2D(3, 50), Vector2D(-2, 0), radius=5)
        ball.bounce_off_walls(100, 100)
        self.assertEqual(ball.position.x, 5)
        self.assertEqual(ball.velocity.x, 2)

    def test_head_on_collision_swaps_velocities(self):
        first = Ball(Vector2D(40, 50), Vector2D(1, 0), radius=6)
        second = Ball(Vector2D(50, 50), Vector2D(-1, 0), radius=6)
        self.assertTrue(first.overlaps(second))
        first.resolve_elastic_collision(second)
        self.assertAlmostEqual(first.velocity.x, -1)
        self.assertAlmostEqual(second.velocity.x, 1)

    def test_pocket_capture(self):
        pocket = Pocket(Vector2D(20, 20), 10)
        ball = Ball(Vector2D(25, 20), Vector2D(0, 0), radius=3)
        self.assertTrue(pocket.captures(ball))

    def test_world_removes_captured_ball(self):
        world = BilliardsWorld(200, 200, pocket_radius=20)
        pocket = world.pockets[0]
        ball = Ball(Vector2D(pocket.position.x, pocket.position.y), Vector2D(0, 0), radius=5)
        world.add_balls([ball])
        world.step()
        self.assertEqual(len(world.balls), 0)
        self.assertFalse(ball.active)


if __name__ == "__main__":
    unittest.main()
