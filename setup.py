# -*- encoding: utf-8 -*-

import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
from setuptools import setup, Command


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='django-remdow',
    version='0.0.0',
    author='Alexander Sapronov',
    author_email='a@sapronov.me',
    keywords='django static templatetags downloader',
    packages=['django_remdow'],
    include_package_data=True,
    url='https://django-remdow.readthedocs.org',
    license='MIT',
    description='  ',
    long_description=README,
    install_requires=['django>=1.7', 'bs4', 'lxml'],
    test_requires=['pytest', 'pytest-django', ],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
