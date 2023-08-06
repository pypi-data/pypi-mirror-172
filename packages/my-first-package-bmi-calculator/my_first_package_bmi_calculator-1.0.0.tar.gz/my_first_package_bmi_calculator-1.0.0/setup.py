from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="my_first_package_bmi_calculator",
    version="1.0.0",
    author="Wiliam_Gomes",
    author_email="wiliam.gomes99@gmail.com",
    description="Calculates body mass index",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wiliam-G/introducao_criacao_de_pacotes",
    packages=find_packages(),
    python_requires=">=3.0",
)