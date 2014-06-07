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
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'corpuscreator = precisealtruism.corpuscreator:run'
        ]
    }
)
