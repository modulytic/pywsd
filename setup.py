import setuptools

# https://packaging.python.org/tutorials/packaging-projects/

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywsd",
    version="0.1.0",
    author="Noah Sandman",
    author_email="noah@modulytic.com",
    description="Python library for ws-daemon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/modulytic/pywsd",
    packages=setuptools.find_packages(),
    python_requires='>=2.7',
)
