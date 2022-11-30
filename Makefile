
twine:
	python -m pip install --upgrade twine

build:
	python -m pip install --upgrade build pip
	python -m build

upload-test: twine
	python -m twine upload --repository pypitest dist/*

upload: twine
	python -m twine upload --repository pypi dist/*

version: build upload
	echo "Done"