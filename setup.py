#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'Cython>=0.21.1',
    'PyYAML>=3.11',
    'numpy>=1.9.1'
]

dependency_links = [
    "git+https://github.com/mcedit/pymclevel.git@8bf7b3d76479e007a51f3055198a8bcddb626c84#egg=pymclevel",
]

test_requirements = [
    'Cython>=0.21.1',
    'PyYAML>=3.11',
    'numpy>=1.9.1'
]

setup(
    name='minepybs',
    version='0.1.0',
    description='Some predefined structures using yaml and pymclevel to build them on any minecraft map',
    long_description=readme + '\n\n' + history,
    author='Felipe Arruda Pontes',
    author_email='contato@arruda.blog.br',
    url='https://github.com/arruda/minecraft-pybuildings',
    packages=[
        'minepybs',
    ],
    package_dir={'minepybs':
                 'minepybs'},
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependency_links,
    license="BSD",
    zip_safe=False,
    keywords='minepybs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)