import re
from os import path
from setuptools import setup


# read() and find_version() taken from jezdez's python apps, ex:
# https://github.com/jezdez/django_compressor/blob/develop/setup.py


def read(*parts):
    return open(path.join(path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-datetimezone-field',
    version=find_version('datetimezone_field', '__init__.py'),
    author='Eric Man',
    author_email='eric@gradconnection.com',
    description=(
        'A Django app providing database and form fields for '
        'split datetime/time and pytz timezone objects.'
    ),
    long_description=read('README.rst'),
    url='https://github.com/GradConnection/django-datetimezone-field',
    license='BSD',
    packages=[
        'datetimezone_field',
    ],
    install_requires=['django>=1.5.2', 'pytz', 'django-timezone-field'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Framework :: Django',
    ],
)