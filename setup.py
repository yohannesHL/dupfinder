from distutils.core import setup

setup(
    name='dupfinder',
    version='0.1.0',
    description='Finds duplicate files using sha256 hashes.',
    long_description='Finds duplicate files using sha256 hash comparisons.',
    keywords='find duplicate files deduplicate dedup deduplication',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        'Programming Language :: Python :: 3.8'
    ],
    author='Yohannes Libanos',
    license='MIT',
    packages=['dupfinder'],
    entry_points={
        'console_scripts': [
            'dupfinder = dupfinder.cli:main'
        ]
    },
)
