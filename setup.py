from distutils.core import setup

setup(
    name='dupfinder',
    version='0.1.0',
    author='Yohannes Libanos',
    packages=['dupfinder'],
    entry_points={
        'console_scripts': [
            'dupfinder = dupfinder.cli:main'
        ]
    },
    license='MIT',
    keywords='find duplicate files, duplicate files, remove duplicate files, deduplication'
    description='Finds duplicate files using sha256 hash comparisons.',
    long_description='Finds duplicate files using sha256 hash comparisons.',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ]
)
