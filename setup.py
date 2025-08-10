import sys, os
from setuptools import setup

dependencies = ['Pillow', 'RPi.GPIO', 'spidev']

setup(
    name='waveshare-epd',
    description='Waveshare e-Paper Display',
    author='Waveshare',
    package_dir={'': 'lib'},
    packages=['waveshare_epd'],
    install_requires=dependencies,
)
