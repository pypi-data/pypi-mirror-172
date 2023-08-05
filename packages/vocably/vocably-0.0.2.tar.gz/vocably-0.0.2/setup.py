import setuptools
from setuptools import setup
from pathlib import Path
from src.vocably import __version__

core_requirements = [
    'numpy~=1.23.3',
    'pandas~=1.5.0',
    'click~=7.1.2',
    'torch~=1.12.1',
    'gensim~=4.2.0',
    'nltk~=3.7',
    'scipy==1.9.1',
    'scikit-learn==1.1.2',
    'transformers==4.22.1',
    'rich~=12.6.0',
    'spacy~=3.4.1',
    'smart-open==5.2.1',
]

setup(
    name='vocably',
    version=__version__,
    py_modules=['command', 'core'],
    install_requires=core_requirements,
    description='Vocably is a Natural Language Framework written in Python for Language based Tasks.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    python_requires='>=3.7,<4',
    author="Nandhini",
    author_email="nandhinisiva2561@gmail.com",
    url="https://github.com/Nandhini25S/Vocably",
    include_package_data=True,
    os_type=["linux", "Windows", "MacOS", "Unix"],
    license='MIT',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'vocably = vocably.cli.main:main',
        ],
    },
)
