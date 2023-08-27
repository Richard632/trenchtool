from setuptools import setup, find_packages

# Get list of requirements from file
with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name='trenchtool',
    version='1.0',
    packages=find_packages(include=["trenchtool"]),
    install_requires=requirements,
)
