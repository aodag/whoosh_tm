from setuptools import setup


__version__ = '0.1'


requires = [
    "transaction",
    "whoosh",
]


setup(
    name="whoosh_tm",
    version=__version__,
    packages=["whoosh_tm"],
    install_requires=requires,
)
