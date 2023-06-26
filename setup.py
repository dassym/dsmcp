import setuptools

import info


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=info.NAME,
    version=info.__version__,
    author="Fabrice Voillat",
    author_email="dev@dassym.com",
    description=info.DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ['lxml', 'pyserial', 'PyDapi2'],
    url="https://git.dassym.com/git/PyDapi2",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)