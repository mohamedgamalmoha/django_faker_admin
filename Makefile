install-requirements:
	pip install -r requirements.txt

install-test-requirements:
	pip install -r test/requirements.txt

test:
	pytest -v -p no:warnings --tb=short --setup-show

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;

run-test: install-test-requirements test clean
