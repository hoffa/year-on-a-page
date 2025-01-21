#!/bin/sh
set -eux

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
for year in 2024 2025 2026; do
	.venv/bin/python main.py --year "$year" >"renders/svg/$year-default.svg"
	# A4 PDF
	.venv/bin/python -c "import cairosvg; cairosvg.svg2pdf(url='renders/svg/$year-default.svg', write_to='renders/pdf/$year-default.pdf', output_width=595, output_height=842)"
done

.venv/bin/python main.py --year 2025 --highlight-past >"renders/svg/latest.svg"
