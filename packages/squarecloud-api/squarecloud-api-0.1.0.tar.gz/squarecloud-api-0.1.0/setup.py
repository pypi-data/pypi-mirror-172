from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(name=r'squarecloud-api',
    version='0.1.0',
    license='MIT License',
    author='Robert Nogueira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='robertlucasnogueira@gmail.com',
    keywords='squarecloud api python',
    description='SquareCloud API wrapper',
    packages=['squarecloud'],
    install_requires=['aiohttp~=3.8.3'],)
