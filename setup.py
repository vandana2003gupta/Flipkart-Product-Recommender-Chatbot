from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="flipkart_products_recommender",
    version="0.1",
    author="Vandana Gupta",
    packages=find_packages(),
    install_requires=requirements,
)
