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

    def line(
        self,
        start: Point,
        end: Point,
        width: float,
        color: str = "black",
    ) -> None:
        self._update_size(start)
        self._update_size(end)
        self._add(
            self.svg.line(
                (start.x, start.y),
                (end.x, end.y),
                stroke_width=width,
                stroke=color,
                stroke_linecap="square",
            )
        )

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

    def ellipse(
        self,
        center: Point,
        rx: float,
        ry: float,
        angle: float,
        color: str = "black",
        stroke: str = "black",
        stroke_width: float = 1,
    ) -> None:
        self._update_size(center)
        shape = self.svg.ellipse(
            (center.x, center.y),
            (rx, ry),
            fill=color,
            stroke=stroke,
            stroke_width=stroke_width,
        )
        shape.rotate(angle, (center.x, center.y))
        self._add(shape)

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


def draw_date(svg, origin, w, h, date):
    firstdayofmonth = date.day == 1
    weekend = date.weekday() in (5, 6)
    print(firstdayofmonth, weekend)
    text = f"{date.month}/{date.day}" if firstdayofmonth else f"{date.day}"
    color = "red" if firstdayofmonth else "black"
    fill = "#eee" if weekend else "white"

    svg.polygon(
        [
            origin,
            Point(origin.x + w, origin.y),
            Point(origin.x + w, origin.y + h),
            Point(origin.x, origin.y + h),
        ],
        fill=fill,
    )
    svg.text(Point(origin.x + (w / 2), origin.y + (h / 2)), text, 20, color=color)


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
    # for d in days:
    #    print(d)

    svg = SVG(1000, 1000)
    # svg.line(Point(10, 10), Point(20, 20), 2)
    # svg.text(Point(30, 30), "12/3", 40)
    svg.text(Point(375, -40), str(year), 50)

    max_x = 17
    w = 40
    h = 40

    x = 0
    y = 0

    for d in days:
        draw_date(svg, Point(x * w, y * h), w, h, d)
        if x >= max_x:
            x = 0
            y += 1
        else:
            x += 1

    """
    draw_date(svg, Point(15, 15), 40, 40, days[0])
    draw_date(svg, Point(15 + 40, 15), 40, 40, days[1])
    draw_date(svg, Point(15 + 40 + 40, 15), 40, 40, days[2])
    draw_date(svg, Point(15 + 40 + 40 + 40, 15), 40, 40, days[3])
    draw_date(svg, Point(15 + 40 + 40 + 40 + 40, 15), 40, 40, days[4])
    draw_date(svg, Point(15 + 40 + 40 + 40 + 40 + 40, 15), 40, 40, days[5])
    draw_date(svg, Point(15 + 40 + 40 + 40 + 40 + 40 + 40, 15), 40, 40, days[6])
    """

    Path("render.svg").write_text(str(svg))


if __name__ == "__main__":
    main()
