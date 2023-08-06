import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asfpy-phd",
    version="0.5.0",
    author="Ari Dyckovsky",
    author_email="aridyckovsky@gmail.com",
    description="A collection of Python scripts for the Application Statement Feedback Program's logistics needs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asfpteam/asfpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
