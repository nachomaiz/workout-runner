from enum import Enum
from typing import Self

import pygame as pg

from .assets import Assets
from .inputs import Inputs
from .progress import Progress


class AppState(Enum):
    EXERCISE = 0
    REST = 1
    PAUSED = 2
    WELCOME = 3


bg_colors = {
    AppState.EXERCISE: pg.Color(136, 176, 57),
    AppState.REST: pg.Color(176, 176, 57),
    AppState.PAUSED: pg.Color(57, 57, 136),
    AppState.WELCOME: pg.Color(30, 30, 30),
}


class Section:
    def __init__(
        self,
        title: str,
        progress: Progress,
        assets: Assets,
        state: AppState = AppState.EXERCISE,
        rest_duration: float = 10.0,
    ) -> None:
        self.title = title
        self.base_state = self.state = state
        self.progress = progress
        self.rest_duration = rest_duration
        self.font = assets.fonts["medium"]
        self.orig_duration = self.progress.duration

    @classmethod
    def create_default(
        cls,
        title: str,
        assets: Assets,
        duration: float = 30.0,
        rest_duration: float = 10.0,
    ) -> Self:
        return cls(
            title,
            Progress(assets, duration),
            rest_duration=rest_duration,
            assets=assets,
        )

    @property
    def done(self) -> bool:
        return self.base_state is AppState.REST and self.progress.done

    def update(self, dt: int, inputs: Inputs) -> None:
        if inputs.pause:
            self.progress.toggle_pause()
            self.state = AppState.PAUSED if self.progress.paused else self.base_state

        if self.progress.done and self.base_state is not AppState.REST:
            self.progress.reset_progress(self.rest_duration)
            self.base_state = self.state = AppState.REST

        self.progress.update(dt)

    def draw(self, surf: pg.Surface) -> None:
        bg_color = bg_colors[self.state]

        title_surf = self.font.render(self.title, True, "white")
        title_rect = title_surf.get_frect()
        title_rect.center = (600, 100)

        state_surf = self.font.render(self.state.name, True, "white")
        state_rect = state_surf.get_frect()
        state_rect.center = (600, 200)

        surf.fill(bg_color)
        self.progress.draw(surf, bg_color)
        surf.blit(state_surf, state_rect)
        surf.blit(title_surf, title_rect)

    def reset_progress(self) -> None:
        self.progress.reset_progress(self.orig_duration)
        self.base_state = self.state = AppState.EXERCISE


class WelcomeScreen:
    def __init__(self, title: str, index: list[str], assets: Assets) -> None:
        self.title = title
        self.index = index
        self.state = AppState.WELCOME
        self.progress = Progress(assets, 5)
        self.starting = False
        self.title_font = assets.fonts["large"]
        self.idx_font = assets.fonts["small"]

    @property
    def done(self) -> bool:
        return self.starting and self.progress.done

    def update(self, dt: int, inputs: Inputs) -> None:
        if self.starting:
            if inputs.pause:
                self.progress.toggle_pause()
                self.state = (
                    AppState.PAUSED if self.progress.paused else AppState.WELCOME
                )

            self.progress.update(dt)
        elif inputs.pause:
            self.starting = True
        else:
            self.state = AppState.WELCOME
            self.progress.paused = False

    def draw(self, surf: pg.Surface) -> None:
        bg_color = bg_colors[AppState.WELCOME]
        surf.fill(bg_color)

        if self.starting:
            title_surf = self.title_font.render("Get ready", True, "white")
            title_rect = title_surf.get_frect()
            title_rect.center = (600, 200)

            self.progress.draw(surf, bg_color)
            surf.blit(title_surf, title_rect)
        else:
            title_surf = self.title_font.render(self.title, True, "white")
            title_rect = title_surf.get_frect()
            title_rect.center = (600, 200)

            subtitle_surf = self.idx_font.render(
                "Click anywhere to start", True, "white"
            )
            subtitle_rect = subtitle_surf.get_frect()
            subtitle_rect.center = (600, 300)

            surf.blit(title_surf, title_rect)
            surf.blit(subtitle_surf, subtitle_rect)

            idx_y = 400
            for i, item in enumerate(self.index):
                idx_surf = self.idx_font.render(item, True, "white")
                idx_rect = idx_surf.get_frect()
                idx_rect.centery = idx_y + idx_rect.height * i
                idx_rect.left = 100

                surf.blit(idx_surf, idx_rect)

    def reset_progress(self) -> None:
        self.starting = False
        self.progress.reset_progress()
