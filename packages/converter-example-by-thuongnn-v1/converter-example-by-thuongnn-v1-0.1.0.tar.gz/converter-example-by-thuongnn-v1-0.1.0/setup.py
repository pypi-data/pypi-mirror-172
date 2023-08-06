import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "0.1.0"

setuptools.setup(
    name="converter-example-by-thuongnn-v1",
    version=__version__,
    author="Nguyen Nhu Thuong",
    author_email="thuongnn@ssi.com.vn",
    description="Sort description",
    long_description="Full description",
    long_description_content_type="text/markdown",
    url="https://github.com/thuongnn/github-actions-learning-python.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
