import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, "README.rst"), encoding="utf-8").read()
except IOError:
    README = ""
try:
    CHANGES = open(os.path.join(here, "CHANGES.rst"), encoding="utf-8").read()
except IOError:
    CHANGES = ""

version = "3.0.0"

install_requires = [
    "Kotti2>=3.0.0",
    "Pillow",
    "plone.scale",
]

tests_require = [
    'WebTest',
    'mock',
    'Pillow',
    'pyquery',
    'pytest>=6.0.0',
    'pytest-cov',
    'zope.testbrowser>=5.0.0',
]

development_requires = [
    "Kotti[development]",
    "pyramid_debugtoolbar",
]

# setup_requires is no longer needed with modern setuptools
setup_requires = []

setup(
    name="kotti2_image",
    version=version,
    description="Image content type for Kotti2 (Python 3.12 + SQLAlchemy 2.0)",
    long_description="\n\n".join([README, CHANGES]),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Pylons",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
    ],
    author="Kotti Developers",
    author_email="kotti@googlegroups.com",
    url="https://github.com/Kotti/kotti_image",
    keywords="kotti kotti2 web cms image",
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    entry_points={},
    extras_require={
        "testing": tests_require,
        "development": development_requires,
    },
)
