#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from sssauth/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("sssauth", "__init__.py")

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='sss-auth',
    version=version,
    description="""sssauth is a pluggable Django app that enables login/signup via an SSS Extension""",  # noqa: E501
    long_description=readme + '\n\n' + history,
    author='SSS-Extension',
    author_email='notify.monakaxym@bgmail.com',
    url='https://github.com/SafelySignSymbol/django-sss-auth-boilerplate',
    packages=[
        'sssauth',
    ],
    include_package_data=True,
    install_requires=['Django>=4.0'],
    license="MIT",
    zip_safe=False,
    keywords='sssauth',
    classifiers=[
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
    ],
)
