import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read().replace('\r\n', '\n').replace('\r', '\n')
CHANGES = open(os.path.join(here, 'CHANGES.txt'), encoding='utf-8').read().replace('\r\n', '\n').replace('\r', '\n')

install_requires = [
    # Kotti2 with ``kotti_image`` add on is required
    'Kotti2>=3.0.0',
]

# copied from Kotti, necessary because extras are not supported in
# ``extras_require``.  See https://github.com/pypa/pip/issues/3189
tests_require = [
    'kotti2_image>=3.0.0',
    'WebTest',
    'mock',
    'Pillow',  # thumbnail filter in depot tween tests
    'pyquery',
    'pytest>=6.0.0',
    'pytest-cov',
    'tox',
    'zope.testbrowser>=5.0.0',
]

# copied from Kotti, necessary because extras are not supported in
# ``extras_require``.  See https://github.com/pypa/pip/issues/3189
development_requires = [
    'check-manifest',
    'pipdeptree',
    'pyramid_debugtoolbar',
]

# setup_requires is no longer needed with modern setuptools
setup_requires = []

setup(
    name='kotti2_tinymce',
    version='3.0.1',
    description="TinyMCE plugins for Kotti2 (Python 3.12 + SQLAlchemy 2.0)",
    long_description=README + '\n\n' + CHANGES,
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
        "Framework :: Pylons",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: MIT License",
    ],
    author='Andreas Kaiser',
    author_email='disko@binary-punks.com',
    url='https://github.com/Kotti/kotti_tinymce',
    keywords='tinymce image browser kotti kotti2 cms',
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        'testing': tests_require,
        'development': development_requires,
    },
    entry_points={
        'fanstatic.libraries': [
            "kotti_tinymce = kotti_tinymce:library",
        ],
    },
    message_extractors={
        "kotti_tinymce": [
            ("**.py", "lingua_python", None),
            ("**.pt", "lingua_xml", None),
        ],
    },
)
