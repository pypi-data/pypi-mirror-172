"""
https://packaging.python.org/en/latest/tutorials/packaging-projects/?highlight=setup.py%20
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latest_earthquake_in_Indonesia_2022",
    version="0.1",
    author="Viko Aldi ",
    author_email="piccoaldi@gmail.com",
    description="This package will get the latest ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Learn-Python-Dev-Indonesia/latest-earthquake-in-indonesia",
    project_urls={
        "Website ": "https://github.com/viko-aldi",
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)