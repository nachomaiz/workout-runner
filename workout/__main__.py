import pygame as pg

from .app import App
from .assets import Assets
from .load import load_sections

pg.init()  # pylint: disable=no-member
pg.font.init()
pg.mixer.init()

HEIGHT = 800
WIDTH = 1200
FPS = 60


def main() -> int:
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Workout")
    clock = pg.time.Clock()
    assets = Assets.from_path("assets/")
    sections = load_sections("assets/data/workout_data.json", assets)
    app = App(sections, screen, clock, assets, FPS)

    app.run()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
