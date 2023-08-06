from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="magiclondrina",
    version="0.0.8",
    author="Erick",
    author_email="erickomine67@gmail.com",
    description="Buscador de cartas de magic em londrina",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erickhiroyuki/pipinstallmagic",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)