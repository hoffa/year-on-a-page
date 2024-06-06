import datetime
from dataclasses import dataclass
from typing import Any, Iterator
from pathlib import Path

import svgwrite  # type: ignore
from svgwrite.container import Group  # type: ignore


@dataclass
class Point:
    x: float
    y: float


class SVG:
    # TODO: Add margin, either by translating each or translating a container <g>
    def __init__(self, margin_w: int, margin_h: int, bg_color: str = "white") -> None:
        self.svg = svgwrite.Drawing(style=f"background-color: {bg_color};")
        self.g = Group()
        self.g.translate(margin_w, margin_h)
        self.svg.add(self.g)
        self.width: float = 0
        self.height: float = 0
        self.margin_w = margin_w
        self.margin_h = margin_h

    def _update_size(self, point: Point) -> None:
        self.width = max(self.width, point.x)
        self.height = max(self.height, point.y)

    def _add(self, element: Any) -> Any:
        self.g.add(element)

    def polygon(
        self,
        points: list[Point],
        color: str = "black",
        fill: str = "white",
        stroke_width: int = 2,
    ) -> None:
        for point in points:
            self._update_size(point)
        self._add(
            self.svg.polygon(
                [(point.x, point.y) for point in points],
                fill=fill,
                stroke=color,
                stroke_width=stroke_width,
            )
        )

    def text(
        self,
        origin: Point,
        s: str,
        size: int,
        font_weight: str = "normal",
        color="black",
    ) -> None:
        self._add(
            self.svg.text(
                s,
                insert=(origin.x, origin.y),
                alignment_baseline="middle",
                font_family="sans-serif",
                font_size=f"{size}px",
                text_anchor="middle",
                font_weight=font_weight,
                fill=color,
            )
        )

    def __str__(self) -> str:
        # It's ugly but works
        width = self.width + (2 * self.margin_w)
        height = self.height + (2 * self.margin_h)
        return (
            str(self.svg.tostring())
            .replace('width="100%"', f'width="{int(width)}"')
            .replace('height="100%"', f'height="{int(height)}"')
        )


def draw_date(svg, origin, w, h, date, textsize, textadjusty):
    firstdayofmonth = date.day == 1
    weekend = date.weekday() in (5, 6)
    text = f"{date.day}" if firstdayofmonth else f"{date.day}"
    color = "black" if firstdayofmonth else "black"
    fill = "white" if weekend else "white"
    if firstdayofmonth:
        fill = "white"

    svg.polygon(
        [
            origin,
            Point(origin.x + w, origin.y),
            Point(origin.x + w, origin.y + h),
            Point(origin.x, origin.y + h),
        ],
        fill=fill,
    )
    svg.text(Point(origin.x + (w / 2), origin.y + (h / 2) + textadjusty), text, textsize, color=color)


def get_days_in_year(year) -> Iterator[datetime.date]:
    oneday = datetime.timedelta(days=1)
    first = datetime.date(year, 1, 1)
    last = datetime.date(year + 1, 1, 1) - oneday

    d = first
    while d <= last:
        yield d
        d += oneday


def main():
    year = 2024
    days = list(get_days_in_year(year))

    svg = SVG(10, 10)
    # svg.line(Point(10, 10), Point(20, 20), 2)
    # svg.text(Point(30, 30), "12/3", 40)

    max_x = 17
    w = 40
    h = 40

    textsize = w * 0.45
    textadjusty = 1

    x = 0
    y = 0

    textpaddingy = 20
    yearsize = 40
    tablepaddingy = textpaddingy + yearsize - 10

    svg.text(Point(((max_x + 1) * 40) / 2, textpaddingy), str(year), yearsize)

    for d in days:
        draw_date(svg, Point(x * w, (y * h) + tablepaddingy), w, h, d, textsize, textadjusty)
        if x >= max_x:
            x = 0
            y += 1
        else:
            x += 1

    Path("render.svg").write_text(str(svg))


if __name__ == "__main__":
    main()
