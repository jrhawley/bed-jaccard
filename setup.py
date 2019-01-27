from setuptools import setup

setup(
    name='bed-jaccard',
    version='0.1.1',
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
    zip_safe=True)
