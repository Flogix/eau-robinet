# Project automation tasks: setup virtual environment, rebuild data, run test suite, and launch app.
# Usage: make setup | make data | make test | make run
# Windows without make: see make.ps1 (.\make.ps1 setup, etc.)
ifeq ($(OS),Windows_NT)
PY := .venv/Scripts/python.exe
else
PY := .venv/bin/python
endif

.PHONY: setup data test run clean-interim

setup:
	python -m venv .venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

data:
	$(PY) scripts/01_download.py
	$(PY) scripts/02_build_parquet.py
	$(PY) scripts/03_build_aggregates.py
	$(PY) scripts/04_referentiels.py
	$(PY) scripts/05_build_scores.py
	$(PY) scripts/06_build_app_tables.py
	$(PY) scripts/07_build_explore_tables.py

test:
	$(PY) -m pytest -q

run:
	$(PY) -m streamlit run app.py
