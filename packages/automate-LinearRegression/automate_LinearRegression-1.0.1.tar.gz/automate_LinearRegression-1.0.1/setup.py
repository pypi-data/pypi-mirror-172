from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'Linear-Regression-Automation'

# Setting up
setup(
    name="automate_LinearRegression",
    version=VERSION,
    author="Suryansh",
    author_email="<suryanshgrover1999@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['scikit-learn', 'numpy'],
    keywords=['python', 'machine learning', 'machine learning model', 'regression',
              'linear regression', 'lasso linear regression', 'elasticnet linear regression', 'regularization'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ]
)
