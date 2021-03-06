from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='py-kraken',
    version='1.5',
    packages=find_packages(),
    url='https://github.com/tha23rd/py-kraken',
    license='MIT',
    author='Zach Bluhm',
    author_email='zach@bluhm.io',
    description='An easy to use module designed to download files from Kraken',
    long_description_content_type="text/markdown",
    long_description=README,
    entry_points={
        'console_scripts': ['kraken-download=pykraken.command_line:main'],
    }
)

install_requires = [
    'bs4',
    'certifi',
    'chardet',
    'idna',
    'lxml',
    'requests',
    'soupsieve',
    'urllib3'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
