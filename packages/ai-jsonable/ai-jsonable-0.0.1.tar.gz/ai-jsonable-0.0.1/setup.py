import setuptools

import pkg_resources
import pathlib
from distutils.util import convert_path

versions = {}
ver_path = convert_path('aijson/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), versions)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    with pathlib.Path(filename).open() as requirements_txt:
        return [str(requirement)
                for requirement in pkg_resources.parse_requirements(requirements_txt)]


setuptools.setup(
    name="ai-jsonable",
    version=versions['__version__'],
    author="Duncan Blythe",
    author_email="duncanblythe@gmail.com",
    description="Tracking model parameters and settings for AI using JSON.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blythed/aijson",
    packages=setuptools.find_packages(),
    setup_requires=[],
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.6',
    install_requires=parse_requirements('requirements.txt'),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'aijson = aijson.__main__:cli'
        ]
    }
)
