import pygame as pg


def highlight_color(color: pg.Color, offset: int) -> pg.Color:
    return pg.Color(
        max(255, color.r + offset),
        max(255, color.g + offset),
        max(255, color.b + offset),
    )
