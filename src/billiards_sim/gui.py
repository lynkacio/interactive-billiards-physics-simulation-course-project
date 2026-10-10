from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from .world import BilliardsWorld


class BilliardsApp:
    """Tkinter user interface for the billiards simulation."""

    def __init__(self, root: tk.Tk | None = None):
        self.root = root or tk.Tk()
        self.root.title("Interactive Billiards Physics Simulation")

        self.canvas_width = 600
        self.canvas_height = 600
        self.world = BilliardsWorld(self.canvas_width, self.canvas_height)
        self.running = False
        self.animation_id: str | None = None

        self._build_layout()

    def _build_layout(self) -> None:
        controls = tk.Frame(self.root, padx=12, pady=12)
        controls.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(controls, text="Billiards Simulation", font=("Arial", 16, "bold")).pack(pady=(0, 12))

        tk.Label(controls, text="Number of balls:").pack(anchor=tk.W)
        self.ball_count = tk.Entry(controls)
        self.ball_count.insert(0, "15")
        self.ball_count.pack(fill=tk.X, pady=(0, 10))

        tk.Label(controls, text="Frame interval (ms):").pack(anchor=tk.W)
        self.frame_interval = tk.Entry(controls)
        self.frame_interval.insert(0, "30")
        self.frame_interval.pack(fill=tk.X, pady=(0, 12))

        tk.Button(controls, text="Start / Reset", command=self.start).pack(fill=tk.X, pady=4)
        tk.Button(controls, text="Pause", command=self.pause).pack(fill=tk.X, pady=4)

        self.status = tk.Label(controls, text="Balls: 0\nRunning: No", justify=tk.LEFT)
        self.status.pack(anchor=tk.W, pady=(15, 0))

        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="darkgreen",
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

    def start(self) -> None:
        try:
            count = int(self.ball_count.get())
            interval = int(self.frame_interval.get())
            if count <= 0 or interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Ball count and frame interval must be positive integers.")
            return

        self.pause()
        self.world = BilliardsWorld(self.canvas_width, self.canvas_height)
        self.world.reset_random_balls(count)
        self.running = True
        self._animate(interval)

    def pause(self) -> None:
        self.running = False
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        self._update_status()

    def _animate(self, interval: int) -> None:
        if not self.running:
            return
        self.world.step()
        self._draw()
        self._update_status()
        self.animation_id = self.root.after(interval, lambda: self._animate(interval))

    def _draw(self) -> None:
        self.canvas.delete("all")

        for pocket in self.world.pockets:
            x, y, r = pocket.position.x, pocket.position.y, pocket.radius
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black", outline="gray")

        for ball in self.world.balls:
            x, y, r = ball.position.x, ball.position.y, ball.radius
            self.canvas.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill=ball.color,
                outline="black",
                width=2,
            )

    def _update_status(self) -> None:
        self.status.config(
            text=f"Balls: {len(self.world.balls)}\nRunning: {'Yes' if self.running else 'No'}"
        )

    def run(self) -> None:
        self.root.mainloop()
