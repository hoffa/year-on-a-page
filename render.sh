#!/bin/sh
set -eux

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
for year in {2000..2100}; do
	.venv/bin/python main.py --year "$year" >"renders/svg/$year.svg"
	# A4 PDF
	.venv/bin/python -c "import cairosvg; cairosvg.svg2pdf(url='renders/svg/$year.svg', write_to='renders/pdf/$year.pdf', output_width=595, output_height=842)"
done
