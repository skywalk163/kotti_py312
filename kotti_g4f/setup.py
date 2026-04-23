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

# Lock dependency versions for security
install_requires = [
    "Kotti2>=3.0.0,<4.0.0",
    "g4f>=0.3.0,<1.0.0",
]

tests_require = [
    "WebTest>=3.0.0",
    "mock>=5.0.0",
    "pytest>=7.0.0,<9.0.0",
    "pytest-cov>=4.0.0",
    "zope.testbrowser>=5.0.0,<7.0.0",
]

setup(
    name="kotti2_g4f",
    version=version,
    description="GPT4Free integration for Kotti2 CMS - Add AI chat content type",
    long_description="\n\n".join([README, CHANGES]),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
    ],
    author="Kotti Developers",
    author_email="kotti@googlegroups.com",
    url="https://github.com/Kotti/kotti2_g4f",
    keywords="kotti kotti2 gpt4free ai chat gpt llm",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={},
    extras_require={
        "testing": tests_require,
    },
)
