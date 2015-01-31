from setuptools import setup


__version__ = '0.1'


requires = [
    "transaction",
    "whoosh",
]


tests_require = [
    "testfixtures",
]


setup(
    name="whoosh_tm",
    version=__version__,
    packages=["whoosh_tm"],
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": tests_require,
    },
)
