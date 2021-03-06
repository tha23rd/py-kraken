from setuptools import setup, find_packages

setup_args = dict(
    name='py-kraken',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/tha23rd/py-kraken',
    license='MIT',
    author='Zach Bluhm',
    author_email='zach@bluhm.io',
    description='An easy to use module designed to download files from Kraken'
)

install_requires = [
    'beautifulsoup4',
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
