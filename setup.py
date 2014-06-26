#!/usr/bin/env python
from setuptools import setup

# get version
with open('precisealtruism/version.py') as version_file:
    exec(version_file.read())

setup(
    name='precisealtruism',
    version=__version__,
    author='Center for Precise Altruism',
    include_package_data=True,
    extras_require=dict(
        test=[],
    ),
    install_requires=[
        'python-tumblpy==1.0.2',
        'feedparser==5.1.3',
        'scikit-learn==0.15.0b1',
        'six==1.7.2',
        'PyStemmer==1.3.0',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'manual_classification = precisealtruism.corpuscreator:manual_classification',
            'corpus_generation = precisealtruism.corpuscreator:corpus_generation',
            'evaluation = precisealtruism.evaluation:run',
        ]
    }
)
