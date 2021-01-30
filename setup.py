from pathlib import Path

from setuptools import setup

long_description = Path(__file__).with_name('README.md').read_text(encoding='utf-8')

requirements = Path(__file__).with_name('requirements.txt').read_text().split()

setup(
    name='i4u',
    version='0.0.6',
    packages=['i4u'],
    url='https://github.com/ofersadan85/i4u',
    license='MIT License',
    author='Ofer Sadan',
    author_email='ofersadan85@gmail.com',
    description='Python package to interact with Invoice4U API',
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    install_requires=requirements + ["dataclasses;python_version<'3.7'"],
)
