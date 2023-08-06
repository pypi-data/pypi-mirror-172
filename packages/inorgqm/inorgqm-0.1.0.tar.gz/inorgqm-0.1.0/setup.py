import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "0.1.0"

setuptools.setup(
    name="inorgqm",
    version=__version__,
    author="Jon Kragskow",
    author_email="jonkragskow@gmail.com",
    description="A package for working with phenomenological spin operators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonkragskow/inorgqm",
    project_urls={
        "Bug Tracker": "https://github.com/jonkragskow/inorgqm/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"."},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["numpy", "scipy", "matplotlib"]
)
