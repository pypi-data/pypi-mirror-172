from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = '''Simple, yet elegant, HTTP library. As like as Requests.
Actually, it is based on requests package...'''


def read(file_name: str):
    with open(file_name) as fi:
        return fi.read()


setup(
    name="fractif-http",
    version=VERSION,
    description=DESCRIPTION,
    author="Tom LARGE",
    author_email="tom@fractif.com",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
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
    ],
    url="https://github.com/Fractif/fractif-http",
)
