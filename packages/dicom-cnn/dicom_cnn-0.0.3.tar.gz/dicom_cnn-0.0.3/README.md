# dicom_cnn

https://packaging.python.org/en/latest/flow/

pipenv run python setup.py sdist
pipenv run python setup.py bdist_wheel
pipenv run twine upload --repository pypi dist/*

//Install dependencies
pipenv install [dep]

//Generate requirements
pipenv requirements > requirements.txt