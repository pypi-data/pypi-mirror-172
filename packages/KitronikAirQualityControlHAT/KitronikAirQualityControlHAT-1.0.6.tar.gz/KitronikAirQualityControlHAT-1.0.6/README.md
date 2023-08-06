# air-quality-control-board
## Setup needed:
- pip install -U pip wheel setuptools
- pip install --no-cache-dir --force-reinstall --only-binary=cryptography cryptography
- pip install -U twine
## Upload wheel:
- python setup.py sdist bdist_wheel
- python -m twine check dist/*
- python -m twine upload dist/*
- pip install -i https://pypi.org/simple KitronikAirQualityControlHAT
- python test_all.py
## Upload test wheel:
- python -m twine upload -r testpypi dist/*
- pip install -i https://test.pypi.org/simple KitronikAirQualityControlHAT
- pip uninstall KitronikAirQualityControlHAT rpi_ws281x
