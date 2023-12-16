.PHONY: test frontend demo serve

test:
	python3 -m unittest discover -s tests

frontend:
	cd frontend && npm ci && npm test && npm run build

demo:
	python3 scripts/demo.py

serve:
	python3 -m regression_workbench.cli serve --policy fixtures/gate-policy.json
