from setuptools import setup, find_packages

setup(
    name='getoptiondata',
    version='0.0.1',
    description=
    """
    A Python library for getting option data from Yahoo Finance 
    and saving it to Excel, 
    analyzing it, and plotting it.
    """,
    author='hank_deng',
    author_email='M1029009@cgu.edu.tw',
    packages=find_packages(),
    install_requires=[
        'yfinance',
        'pandas',
        'datetime',
    ],
)
