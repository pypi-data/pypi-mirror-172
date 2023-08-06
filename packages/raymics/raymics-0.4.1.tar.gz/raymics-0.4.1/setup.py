from setuptools import setup
from pathlib import Path

# with open(Path(__file__).parent / 'requirements.txt') as f:
#     requires_list = [x.strip() for x in f.readlines()]


def get_install_requires():
    """Returns requirements.txt parsed to a list"""
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setup(
    name="raymics",
    version="0.4.1",
    description="Raymics Tools",
    install_requires=get_install_requires(),
    packages=["raymics"]
)
