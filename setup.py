from distutils.core import setup

setup(
    name='dupfinder',
    version='0.1.0',
    author='Yohannes Libanos',
    packages=['dupfinder'],
    entry_points={
        'console_scripts': [
            'dupfinder = dupfinder.main:main'
        ]
    },
    license='MIT',
    description='Finds duplicate files using sha256 hash comparisons.',
    long_description='Finds duplicate files using sha256 hash comparisons.'
)
