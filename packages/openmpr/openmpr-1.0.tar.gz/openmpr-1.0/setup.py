from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # name of the library
    name="openmpr",
    version="0.0.1",
    description="Publish whatever you want",
    # py-file that will be uploaded to PyPI
    py_modules=["mpr", "rmpr"],
    package_dir={"": "src"},
    #
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    # project url
    # url = ’https://github.com/username/project_repository’,
    author="Zhuokai Zhao",
    author_email="zhuokai@uchicago.edu",
)
