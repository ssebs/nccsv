all:
	@python -m nccsv
publish:
	@rm -rf ./dist/*
	@python3 setup.py sdist bdist_wheel
	@twine upload ./dist/*