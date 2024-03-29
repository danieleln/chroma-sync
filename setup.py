from setuptools import setup, find_packages

setup(
    name="chromasync",
    version="0.1.0",
    description="Syncs themes for various CLI tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniele Monzani",
    author_email="daniele.monzani@outlook.com",
    url="https://github.com/danieleln/chromasync",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "chromasync = chromasync.__main__:main"
        ],
    },
    python_requires=">=3.4",
    install_requires=[
        # TODO: create a compat.py package that manages libraries for
        #       python versions <3.4 . Check out the following:
        # "argparse",                       # Included in Python standard library since version 3.2
        # "pathlib2; python_version<'3.4'", # pathlib2 provides pathlib for older Python versions
        # "enum34; python_version<'3.4'",   # enum34 backport for Python versions older than 3.4
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
