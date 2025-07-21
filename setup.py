# setup.py
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='glpi-explorer',
    version='0.1.0', # Notre version actuelle
    author='Timo',
    description='Un outil CLI pour explorer et analyser une infrastructure réseau GLPI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Lumosity23/glpi_explorer.git', # URL du dépôt GitHub
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
                'glpi = src.__main__:main',
            ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
