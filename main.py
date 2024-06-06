import argparse
import datetime
from dataclasses import dataclass

import svgwrite
from svgwrite.container import Group


@dataclass
class Point:
    x: float
    y: float


class SVG:
    def __init__(self, margin_w, margin_h, bg_color="white") -> None:
        self.svg = svgwrite.Drawing(style=f"background-color: {bg_color};")
        self.g = Group()
        self.g.translate(margin_w, margin_h)
        self.svg.add(self.g)
        self.width: float = 0
        self.height: float = 0
        self.margin_w = margin_w
        self.margin_h = margin_h

    def _update_size(self, point) -> None:
        self.width = max(self.width, point.x)
        self.height = max(self.height, point.y)

    def _add(self, element):
        self.g.add(element)

    def polygon(
        self,
        points,
        color="black",
        fill="white",
        stroke_width=2,
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
        origin,
        s,
        size,
        font_weight="normal",
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

    def __str__(self):
        # It's ugly but works
        width = self.width + (2 * self.margin_w)
        height = self.height + (2 * self.margin_h)
        return (
            str(self.svg.tostring())
            .replace('width="100%"', f'width="{int(width)}"')
            .replace('height="100%"', f'height="{int(height)}"')
        )


def draw_date(svg, origin, w, h, date, textsize, textadjusty, weekendfill, firstdayfill, firstdaycolor):
    firstdayofmonth = date.day == 1
    weekend = date.weekday() in (5, 6)
    text = f"{date.day}" if firstdayofmonth else f"{date.day}"
    color = firstdaycolor if firstdayofmonth else "black"
    fill = weekendfill if weekend else "white"
    if firstdayofmonth:
        fill = firstdayfill

    svg.polygon(
        [
            origin,
            Point(origin.x + w, origin.y),
            Point(origin.x + w, origin.y + h),
            Point(origin.x, origin.y + h),
        ],
        fill=fill,
    )
    svg.text(
        Point(origin.x + (w / 2), origin.y + (h / 2) + textadjusty),
        text,
        textsize,
        color=color,
    )


def get_days_in_year(year):
    oneday = datetime.timedelta(days=1)
    first = datetime.date(year, 1, 1)
    last = datetime.date(year + 1, 1, 1) - oneday

    d = first
    while d <= last:
        yield d
        d += oneday


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--weekendfill', type=str, default="#ddd")
    parser.add_argument('--firstdayfill', type=str, default="red")
    parser.add_argument('--firstdaycolor', type=str, default="white")
    args = parser.parse_args()

    days = list(get_days_in_year(args.year))

    svg = SVG(10, 10)

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

    svg.text(Point(((max_x + 1) * 40) / 2, textpaddingy), str(args.year), yearsize)

    for d in days:
        draw_date(
            svg, Point(x * w, (y * h) + tablepaddingy), w, h, d, textsize, textadjusty, args.weekendfill, args.firstdayfill, args.firstdaycolor
        )
        if x >= max_x:
            x = 0
            y += 1
        else:
            x += 1

    print(str(svg))


if __name__ == "__main__":
    main()
