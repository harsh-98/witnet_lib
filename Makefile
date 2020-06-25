publish:
	# https://realpython.com/pypi-publish-python-package/
	pip install -r setup_requirements.txt
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	rm -fr build dist .egg witnet_lib.egg-info