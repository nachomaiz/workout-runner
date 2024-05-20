import math

import pygame as pg

from .assets import Assets
from .utils import highlight_color


class Progress:
    def __init__(
        self,
        assets: Assets,
        duration: float = 30,
        radius: float = 200,
        center: pg.Vector2 = pg.Vector2(600, 500),
        width: int = 20,
        color_offset: int = 60,
    ) -> None:
        self.duration = duration
        self.width = width
        self.color_offset = color_offset
        self.rect = pg.FRect(
            center.x - radius, center.y - radius, radius * 2, radius * 2
        )

        self.progress = self.second_progress = 0.0
        self.paused = False

        self.font = assets.fonts["medium"]
        self.tock_sound = assets.sounds["single_tock"]
        self.tock_sound.set_volume(0.5)
        self.double_tock_sound = assets.sounds["double_tock"]
        self.double_tock_sound.set_volume(0.7)

    @property
    def done(self) -> bool:
        return self.duration <= self.progress

    def update(self, dt: int) -> None:
        if not self.paused:
            seconds = dt / 1000
            self.progress = min(self.progress + seconds, self.duration)
            self.second_progress += seconds

        if self.second_progress >= 1.0:
            self.tock_sound.play(maxtime=300)
            self.second_progress %= 1.0

        if self.done:
            self.double_tock_sound.play(maxtime=500)

    def toggle_pause(self):
        self.paused = not self.paused

    def draw(self, surf: pg.Surface, bg_color: pg.Color) -> None:
        percentage = self.progress / self.duration
        start_angle = 2 * math.pi * percentage

        secs_surf = self.font.render(
            f"{int(self.duration - self.progress + 1)}s", True, "white"
        )
        secs_rect = secs_surf.get_frect()
        secs_rect.center = self.rect.center
        pg.draw.arc(
            surface=surf,
            color=highlight_color(bg_color, self.color_offset),
            rect=self.rect,
            start_angle=start_angle,
            stop_angle=0.0000001 * math.pi,
            width=self.width,
        )
        surf.blit(secs_surf, secs_rect)

    def reset_progress(self, new_duration: float | None = None) -> None:
        if new_duration:
            self.duration = new_duration

        self.progress = self.second_progress = 0.0
