from setuptools import setup


with open("README.md" , "r")as fh:
    long_description = fh.read()

setup(
    name='LoadPredConverge',
    version='0.0.1',
    description='Residential electricity forecasting and disaggregation module',
    py_modules=["LoadPredConverge"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type = "text/markdown",
    install_requires = [
        'skforecast==0.4.2',
        'sklearn',
        'more_itertools',
        'multiprocess',
        'pyomo'
    ]
)