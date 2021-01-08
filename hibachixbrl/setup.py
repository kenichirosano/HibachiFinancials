import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hibachixbrl-WabiSabiKen", # Replace with your own username
    version="0.0.1",
    author="KenSano",
    author_email="kenfromkawasaki@gmail.com",
    description="XBRL(Japanese Edinet) extention python library",
    long_description=long_description,
    license='MIT License',
    long_description_content_type="text/markdown",
    url="https://github.com/WabiSabiKen/hibachixbrl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

