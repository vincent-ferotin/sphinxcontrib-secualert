# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
    )


LONG_DESC = '''
This package contains the `secualert` Sphinx extension.

This extension was created to specifically list as security alerts
items previously targeted as `todo`, and allow listing all alerts
in one list, different from `todolist`.
'''
REQUIRES = [
    'Sphinx>=1.8',
]


setup(
    name='sphinxcontrib-secualert',
    version='0.1',
    license='BSD',
    author='Vincent Férotin',
    author_email='vincent.ferotin@gmail.com',
    description='Sphinx "secualert" extension',
    long_description=LONG_DESC,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRES,
    extras_require={
        'dev': [
            'Babel',
        ],
    },
    namespace_packages=['sphinxcontrib'],
)

