from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "KitronikAirQualityControlHAT",
    version = "1.0.6",
    description = "Kitronik Raspberry Pi HAT for monitoring Air Quality",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ["KitronikAirQualityControlHAT"],
    python_requires = ">=3.7",
    install_requires = [
        "rpi_ws281x",
    ],
)