# -*- coding: utf-8 -*-
"""
    pygments.lexers.whiley
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Whiley language.

    :copyright: Copyright 2006-2016 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, words, include, default
from pygments.token import Comment, Keyword, Name, Number, Operator, \
    Punctuation, String, Text

__all__ = ['WhileyLexer']


class WhileyLexer(RegexLexer):
    """
    Lexer for the Whiley programming language.
    """
    name = 'Whiley'
    filenames = ['*.whiley']
    aliases = ['whiley']
    mimetypes = ['text/x-whiley']

    # See the language specification:
    # http://whiley.org/download/WhileyLanguageSpec.pdf

    tokens = {
        'default': [
            # Whitespace
            (r'\s+', Text),

            # Comments
            (r'//.*', Comment.Single),
            # don't parse empty comment as doc comment
            (r'/\*\*/', Comment.Multiline),
            (r'(?ms)/\*\*.*?\*/', Comment.Doc),
            (r'(?ms)/\*.*?\*/', Comment.Multiline),
        ],
        'keywords': [
            (words((
                'if', 'else', 'while', 'for', 'do', 'return',
                'switch', 'case', 'default', 'break', 'continue',
                'requires', 'ensures', 'where', 'assert', 'assume',
                'all', 'no', 'some', 'in', 'is', 'new',
                'throw', 'try', 'catch', 'debug', 'skip', 'fail',
                'finite', 'total',
             ), suffix=r'\b'), Keyword.Reserved),
            (words((
                'function', 'method', 'public', 'private', 'protected',
                'export', 'native',
             ), suffix=r'\b'), Keyword.Declaration),
            (r'(package|import)\b', Keyword.Namespace),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(bool|byte|int|real|any|void)\b', Keyword.Type),
        ],
        'root': [ # only for my thesis that I can use inline single word sourcecode
            ('^this$', Name.Lifetime.Builtin),
            default('root_normal'),
        ],
        'root_normal': [
            include('default'),

            # some keywords lead to special handling of what follows,
            # so don't include keywords here

            # "constant" and "type" are not keywords unless used in declarations
            (r'(constant|type)(\s+)([a-zA-Z_]\w*)(\s+)(is)\b',
             bygroups(Keyword.Declaration, Text, Name, Text, Keyword.Reserved)),
            # "from" is not a keyword unless used with import
            (r'(import)(\s+)(\*)([^\S\n]+)(from)\b',
             bygroups(Keyword.Namespace, Text, Punctuation, Text, Keyword.Namespace)),
            (r'(import)(\s+)([a-zA-Z_]\w*)([^\S\n]+)(from)\b',
             bygroups(Keyword.Namespace, Text, Name, Text, Keyword.Namespace)),

            # some keywords might be followed by a list of lifetimes
            (r'method\b', Keyword.Declaration, 'lifetimes'),
            (r'with\b', Keyword.Reserved, 'lifetimes'),

            # now we can include the keywords
            include('keywords'),

            # standard library: https://github.com/Whiley/WhileyLibs/
            (words((
                # types defined in whiley.lang.Int
                'i8', 'i16', 'i32', 'i64',
                'u8', 'u16', 'u32', 'u64',
                'uint', 'nat',

                # whiley.lang.Any
                'toString',
             ), suffix=r'\b'), Name.Builtin),

            # lambda expressions with lifetime parameters
            (r'(&)(\s*)(?=<)', bygroups(Punctuation, Text), 'lifetimes'),

            # reference type with lifetime annontation
            (r'(&)(\s*)(this|\*)(\s*)(:)([^\S\n]*)(?!\n)',
             bygroups(Punctuation, Text, Name.Lifetime.Builtin, Text, Punctuation, Text)),
            (r'(&)(\s*)([a-zA-Z_]\w*)(\s*)(:)([^\S\n]*)(?!\n)',
             bygroups(Punctuation, Text, Name.Lifetime, Text, Punctuation, Text)),

            # "new" expression with lifetime annontation
            (r'(this|\*)(\s*)(:)([^\S\n]*)(new)\b',
             bygroups(Name.Lifetime.Builtin, Text, Punctuation, Text, Keyword.Reserved)),
            (r'([a-zA-Z_]\w*)(\s*)(:)([^\S\n]*)(new)\b',
             bygroups(Name.Lifetime, Text, Punctuation, Text, Keyword.Reserved)),

            # named block
            (r'([a-zA-Z_]\w*)(\s*)(:)([^\S\n]*)(?=(//.*)?$)',
             bygroups(Name.Label, Text, Punctuation, Text)),

            # byte literal
            (r'[01]+b', Number.Bin),

            # decimal literal
            (r'[0-9]+\.[0-9]+', Number.Float),
            # match "1." but not ranges like "3..5"
            (r'[0-9]+\.(?!\.)', Number.Float),

            # integer literal
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),

            # character literal
            (r"""'[^\\]'""", String.Char),
            (r"""(')(\\['"\\btnfr])(')""",
             bygroups(String.Char, String.Escape, String.Char)),

            # string literal
            (r'"', String, 'string'),

            # operators and punctuation
            (r'[{}()\[\],.;]', Punctuation),
            (r'[+\-*/%&|<>^!~@=:?'
            # unicode operators
             r'\u2200\u2203\u2205\u2282\u2286\u2283\u2287'
             r'\u222A\u2229\u2264\u2265\u2208\u2227\u2228'
             r']', Operator),

            # identifier
            (r'[a-zA-Z_]\w*', Name),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\[btnfr]', String.Escape),
            (r'\\u[0-9a-fA-F]{4}', String.Escape),
            (r'\\.', String),
            (r'[^\\"]+', String),
        ],
        'lifetimes': [
            include('default'),
            (r'<', Punctuation, 'in_lifetimes_list'),
            default('#pop'),
        ],
        'in_lifetimes_list': [
            include('default'),
            (r'>', Punctuation, '#pop:2'),
            (r'this\b|\*', Name.Lifetime.Builtin),
            (r'[a-zA-Z_]\w*', Name.Lifetime),
            (r',', Punctuation),
        ],
    }
