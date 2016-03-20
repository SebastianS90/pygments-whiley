#!/usr/bin/env python

from setuptools import setup
 
setup(
    name = 'pygments-whiley',
    version = '0.1',
    description = 'Pygments lexer for Whiley',
    long_description = 'Pygments (http://pygments.org/) lexer for Whiley (http://whiley.org/)',
    keywords = 'pygments lexer whiley',
    license = 'BSD',

    author = 'Sebastian Schweizer',
    author_email = 'sebastian@schweizer.tel',

    url = 'https://github.com/SebastianS90/pygments-whiley',

    packages = ['whiley_lexer'],
    install_requires = ['pygments >= 2.0'],
    entry_points = '''[pygments.lexers]
                       whileylexer = whiley_lexer:WhileyLexer''',


    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
    ],
)
