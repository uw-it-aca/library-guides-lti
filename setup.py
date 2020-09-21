import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/library-guides-lti>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'libguide/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='UW-Library-Guides-LTI',
    version=VERSION,
    packages=['libguide'],
    include_package_data=True,
    install_requires = [
        'Django>=2.1,<2.2',
        'django-blti>=2.2.1',
        'django-compressor',
        'python-memcached',
        'UW-RestClients-Core>=1.3.3,<2.0',
        'UW-RestClients-Libraries>=1.0,<2.0',
        'UW-RestClients-Canvas>=1.1.9,<2.0',
        'UW-RestClients-Django-Utils>=2.1.8,<3.0',
    ],
    license='Apache License, Version 2.0',
    description=(
        'An LTI app for displaying UW Library Subject Guides in Canvas'),
    long_description=README,
    url='https://github.com/uw-it-aca/library-guides-lti',
    author = "UW-IT AXDD",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
