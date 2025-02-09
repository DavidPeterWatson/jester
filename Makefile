VENV=.venv

.PHONY: setup run clean

setup:
	uv venv .venv
	uv pip install fastapi uvicorn

activeate:
	source .venv/bin/activate

run:
	$(VENV)/bin/uvicorn fastapi_backend:app --reload

clean:
	rm -rf $(VENV)