from setuptools import setup

with open ("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name="easygeo", 
    version="0.0.2",
    author="Joaquin Cubelli",
    author_email="jcubellidl@gmail.com",
    url="https://github.com/CubelliJ/easyGeo",
    description="Simple library that allows to geocode using Nominatim or Google V3 API",
    py_modules=["easygeo"],
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Operating System :: MacOS"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "geopy",
        "pandas"
    ],
    extra_require = {
        "dev": [
            "pytest>=7.0",
            "twine>4.0"
        ],
    },
)