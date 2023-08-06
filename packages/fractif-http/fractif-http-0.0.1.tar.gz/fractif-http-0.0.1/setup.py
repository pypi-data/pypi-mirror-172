from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'An http package'
LONG_DESCRIPTION = 'An http package that makes it easy to send http requests'

setup(
    name="fractif-http",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Tom LARGE",
    author_email="tom@fractif.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'user_agent',
        'coloredlogs',
    ],
    keywords='http',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
