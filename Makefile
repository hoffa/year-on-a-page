init:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install black

format:
	.venv/bin/black .

test:
	.venv/bin/black --check .

render:
	.venv/bin/python main.py --year 2024 > renders/2024-default.svg
	.venv/bin/python main.py --year 2024 --weekendfill white --firstdayfill white --firstdaycolor black > renders/2024-minimal.svg
	.venv/bin/python main.py --year 2024 --weekendfill white --firstdayfill black --firstdaycolor white > renders/2024-mono.svg

clean:
	rm -r .venv
