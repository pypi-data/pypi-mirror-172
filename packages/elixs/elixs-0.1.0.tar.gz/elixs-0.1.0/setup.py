import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elixs",
    version="0.1.0",                               # The initial release version
    author="Elias Kremer",                         # Full name of the author
    description="Standart Library for elixs.dev",
    long_description=long_description,             # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),           # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
    ],                                             # Information to filter the project on PyPi website
    python_requires='>=3.8',                       # Minimum version requirement of the package
    py_modules=["elixs"],                          # Name of the python package
    package_dir={"elixs": "elixs"},                         # Directory of the source code of the package
    install_requires=["mysql-connector-python"]    # Install other dependencies if any
)
