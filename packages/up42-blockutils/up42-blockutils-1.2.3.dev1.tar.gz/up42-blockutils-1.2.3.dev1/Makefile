SRC := .

install:
	pip install up42-blockutils

install[dev]:
	pip install -r $(SRC)/requirements.txt
	pip install -e .
	pip install -r $(SRC)/requirements-testing.txt
	pip install -r $(SRC)/requirements-docs.txt

test:
	bash test.sh

update-docs-blockutils:
	mkdocs gh-deploy -f libs/python3/mkdocs.yml -m "update gh-pages [ci skip]"

serve:
	mkdocs serve

gh-pages:
	mkdocs gh-deploy -m "update gh-pages [ci skip]"

package:
	python setup.py sdist bdist_wheel
	twine check dist/*

upload:
	twine upload --skip-existing dist/*
