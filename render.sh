#!/bin/sh
set -eux

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
for year in 2024 2025 2026; do
    for variant in default month monthkorean emoji; do
        .venv/bin/python main.py --year "$year" --variant "$variant" > "renders/$year-$variant.svg"
        # A4 PDF
        .venv/bin/python -c "import cairosvg; cairosvg.svg2pdf(url='renders/$year-$variant.svg', write_to='renders/pdf/$year-$variant.pdf', output_width=595, output_height=842)"
    done
done
