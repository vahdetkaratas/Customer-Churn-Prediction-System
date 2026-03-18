train:
	python -m src.pipeline.training_pipeline

run-api:
	uvicorn src.api.app:app --reload

test:
	pytest

# CLI inference (one customer from JSON)
predict:
	python -m src.cli.predict --input scripts/sample_customer.json
