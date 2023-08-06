from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="gy_multiprocessing",
    version="0.0.1",
    author="Guangyu He",
    author_email="me@heguangyu.net",
    description="Run function in multiple processes",
    long_description="A basic library that run functions in parallel multiple processes",
    long_description_content_type="text/markdown",
    url="https://github.com/guangyu-he/gy-multiprocessing",
    install_requires=[],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    tests_require=["pytest"]
)
