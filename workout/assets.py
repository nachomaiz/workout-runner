import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self, TypedDict

import pygame as pg


class FontData(TypedDict):
    name: str
    size: int


@dataclass(slots=True)
class Assets:
    fonts: dict[str, pg.font.Font]
    sounds: dict[str, pg.mixer.Sound]

    @classmethod
    def from_path(cls, path: str | Path) -> Self:
        path = Path(path)

        with open(path / "data/fonts.json", encoding="utf-8") as file:
            font_data: dict[str, FontData] = json.load(file)

        return cls(
            fonts={k: pg.font.SysFont(**v) for k, v in font_data.items()},
            sounds={
                file.stem: pg.mixer.Sound(file)
                for file in (path / "sounds").glob("*.wav")
            },
        )
