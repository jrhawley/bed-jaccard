from setuptools import setup
from os import path

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bed-jaccard',
    version='0.1.2',
    description='Quickly calculate and plot Jaccard index for BED files',
    url='http://github.com/jrhawley/bed-jaccard',
    author='James Hawley',
    author_email='james.hawley@mail.utoronto.ca',
    license='GPLv3',
    packages=['bed_jaccard'],
    install_requires=[
        'numpy',
        'pandas',
        'pybedtools',
        'seaborn'
    ],
    entry_points={
        'console_scripts': ['bed-jaccard=bed_jaccard.command_line:main']
    },
    scripts=['bin/bed-jaccard'],
    zip_safe=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
