<<<<<<< HEAD
from setuptools import setup, find_packages
=======
from setuptools import setup,find_packages
>>>>>>> fb74ba9e5ea1a37f37db3961a1b8c7e4d5e2f671

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
<<<<<<< HEAD
    name="flipkart_products_recommender",
    version="0.1",
    author="Vandana Gupta",
    packages=find_packages(),
    install_requires=requirements,
)
=======
    name="FLIPKART RECOMMENDER",
    version="0.1",
    author="Vandana Gupta",
    packages=find_packages(),
    install_requires = requirements,
)
>>>>>>> fb74ba9e5ea1a37f37db3961a1b8c7e4d5e2f671
