init:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install black

format:
	.venv/bin/black .

test:
	.venv/bin/black --check .

clean:
	rm -r .venv
