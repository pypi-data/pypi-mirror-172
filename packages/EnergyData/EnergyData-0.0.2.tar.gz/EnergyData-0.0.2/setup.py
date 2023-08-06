
import setuptools

setuptools.setup(
    name="EnergyData",
    version="0.0.2",
    url="https://github.com/Asmaa-khorkhash/Energydata",
    author="Asmaa khorkhash",
    author_email="asmaakhorkhash@gmail.com",
    description=" Measurements of electric power consumption in one household",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    package_data={'': ['data/*.csv']},)