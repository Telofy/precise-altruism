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
        'six==1.7.3',  # Python 2 and 3 compatibility
        'PyStemmer==1.3.0',  # Stemming
        'SQLAlchemy==0.9.6',  # DB abstraction layer(s)
        'alembic==0.6.5',  # DB migration support
        'beautifulsoup4==4.3.2',  # Mostly just for decoding
        'readability-lxml==0.3.0.3',  # Boilerplate stripping
        'cssselect==0.9.1',  # lxml dependency
        'python-dateutil==2.2',  # Date parsing
        'sumy==0.3.0',  # Automatic summarization
        'setuptools',  # For breadability
        'awesome-slugify==1.5',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'manual_classification = precisealtruism.corpuscreator:manual_classification',
            'corpus_generation = precisealtruism.corpuscreator:corpus_generation',
            'evaluation = precisealtruism.evaluation:run',
            'daemon = precisealtruism.daemon:run',
        ]
    }
)
