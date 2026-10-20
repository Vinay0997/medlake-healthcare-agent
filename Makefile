setup:
	pip install -r requirements.txt && pip install -e .
data:
	python -m medlake.generate_data --rows 50000
pipeline:
	python -m medlake.run_pipeline
test:
	pytest -q
