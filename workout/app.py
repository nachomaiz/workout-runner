from typing import Protocol, Self, Sequence

import pygame as pg

from .assets import Assets
from .section import AppState, Inputs, WelcomeScreen


class Section(Protocol):
    title: str
    state: AppState

    @property
    def done(self) -> bool: ...

    def update(self, dt: int, inputs: Inputs) -> None: ...

    def draw(self, surf: pg.Surface) -> None: ...

    def reset_progress(self) -> None: ...


class SectionIterator:
    def __init__(self, sections: Sequence[Section]) -> None:
        self.sections = sections
        self.len = len(sections)
        self.idx = -1

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Section:
        if self.len == 0:
            raise StopIteration

        self.idx = self.get_next_section_idx()
        return self.sections[self.idx]

    def __getitem__(self, index: int) -> Section:
        return self.sections[self.idx + index]

    def get_next_section_idx(self) -> int:
        return (self.idx + 1) % self.len

    def get_current_section(self) -> Section:
        return self.sections[self.idx]

    def get_next_section(self) -> Section:
        return self.sections[self.get_next_section_idx()]


class App:
    def __init__(
        self,
        sections: Sequence[Section],
        screen: pg.Surface,
        clock: pg.time.Clock,
        assets: Assets,
        fps: float = 60,
    ) -> None:
        self.sections: list[Section] = [
            WelcomeScreen(
                "Exercise Challenge",
                [section.title for section in sections or []],
                assets,
            )
        ] + list(sections)
        self.section_it = SectionIterator(self.sections)
        self.current_section = next(self.section_it)
        self.font = assets.fonts["small"]
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.stop_rect = pg.FRect(-1, -1, 1, 1)
        self.stop_hover = False

    def update(self, dt: int, inputs: Inputs) -> None:
        if self.current_section.done:
            self.current_section.reset_progress()
            self.current_section = next(self.section_it)

        if self.stop_rect.collidepoint(pg.mouse.get_pos()):
            self.stop_hover = True
            if inputs.stop:
                self.current_section.reset_progress()
                self.section_it = SectionIterator(self.sections)
                self.current_section = next(self.section_it)
        else:
            self.stop_hover = False

        self.current_section.update(dt, inputs)

    def draw(self, surf: pg.Surface) -> None:
        self.current_section.draw(surf)

        title_surf = self.font.render(
            f"Next: {self.section_it.get_next_section().title}", True, "white"
        )
        title_rect = title_surf.get_frect()
        title_rect.right = 1100
        title_rect.centery = 700

        surf.blit(title_surf, title_rect)
        if self.current_section.state == AppState.PAUSED:
            stop_surf = self.font.render(
                " ■ Stop workout ", True, "white" if self.stop_hover else "lightgrey"
            )
            self.stop_rect = stop_rect = stop_surf.get_frect()
            stop_rect.topleft = 50, 50
            surf.blit(stop_surf, stop_rect)
            pg.draw.rect(
                surf,
                "white" if self.stop_hover else "lightgrey",
                stop_rect,
                width=1,
                border_radius=2,
            )

        # mouse_pos = pg.mouse.get_pos()
        # mouse_pos_surf = self.font.render(f"{mouse_pos}", True, "white")
        # mouse_pos_rect = mouse_pos_surf.get_frect()
        # surf.blit(mouse_pos_surf, mouse_pos_rect)

    def run(self) -> None:
        while True:
            dt = self.clock.tick(self.fps)

            inputs = Inputs.from_events(pg.event.get(), [self.stop_rect])

            if inputs.quit:
                return pg.quit()  # pylint: disable=no-member

            self.update(dt, inputs)
            self.draw(self.screen)

            pg.display.flip()
