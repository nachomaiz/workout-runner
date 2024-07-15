from dataclasses import dataclass, field
from typing import Self

import pygame as pg


@dataclass(slots=True)
class Inputs:
    pause: bool = False
    quit: bool = False
    stop: bool = False
    mouse_pos: pg.Vector2 = field(default_factory=pg.Vector2)

    @classmethod
    def from_events(cls, events: list[pg.Event], pressable: list[pg.FRect]) -> Self:
        res = cls()
        for event in events:
            if event.type == pg.QUIT:  # pylint: disable=no-member
                res.quit = True
            elif event.type == pg.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                if not any(p.collidepoint(event.pos) for p in pressable):
                    res.pause = True
                else:
                    res.stop = True

        return res
