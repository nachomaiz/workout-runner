import json
from typing import Any

from .assets import Assets
from .section import Section


def load_sections(filename: str, assets: Assets) -> list[Section]:
    with open(filename, "r", encoding="utf-8") as file:
        data: list[dict[str, Any]] = json.load(file)

    return [Section.create_default(**section, assets=assets) for section in data]
