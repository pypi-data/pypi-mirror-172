import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="arithmeticdk", # Replace with your own username
    version="0.0.1",
    author="dharmendrakariya",
    author_email="dharamendtra.kariya@gmail.com",
    description="A simple arithmeticdk package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
