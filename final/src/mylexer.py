import ply.lex as lex

# === RESERVED KEYWORDS === #
keywords = [
        'break',
        'case',
        'chan',
        'const',
        'continue',
        'default',
        'defer',
        'else',
        'fallthrough',
        'for',
        'func',
        'go',
        'goto',
        'if',
        'import',
        'interface',
        'map',
        'package',
        'print',
        'scan',
        'range',
        'return',
        'select',
        'struct',
        'switch',
        'type',
        'ttype',
        'var',
        'pointer',
        'malloc'
        ]

# === TOKENS LIST === #
tokens = [
        'IDENTIFIER',
        'RUNE',
        'STRING',
        'IMAGINARY',
        'FLOAT',
        'INTEGER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MOD',
        'AMPERS',
        'OR',
        'CARET',
        'LL',
        'GG',
        'AMPCAR',
        'MINUSEQ',
        'DIVIDEEQ',
        'MODEQ',
        'AMPEQ',
        'OREQ',
        'CAREQ',
        'LLEQ',
        'GGEQ',
        'AMPCAREQ',
        'AMPAMP',
        'OROR',
        'LMINUS',
        'PLUSPLUS',
        'MINUSMIN',
        'EQEQ',
        'LESS',
        'GREAT',
        'EQUAL',
        'NOT',
        'NOTEQ',
        'LEQ',
        'GEQ',
        'COLONEQ',
        'DDD',
        'LPAREN',
        'RPAREN',
        'LBRACK',
        'RBRACK',
        'LBRACE',
        'RBRACE',
        'COMMA',
        'DOT',
        'SEMICOL',
        'COLON',
        'PLUSEQ',
        'TIMESEQ',
        'CONSTANT',
        'TYPEX',
        'PD',
        'PS'
        ] + [k.upper() for k in keywords]

# === REGEX DEFINITIONS === #
t_ignore = ' \t'
t_ignore_COMMENT = r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'
t_AMPERS  = r'&'
t_OR 	  = r'\|'
t_CARET   = r'\^'
t_LL      = r'(<<)'
t_GG	  = r'(>>)'
t_AMPCAR  = r'&\^'
t_PLUSEQ  = r'(\+=)'
t_MINUSEQ = r'(-=)'
t_TIMESEQ = r'(\*=)'
t_DIVIDEEQ= r'/='
t_MODEQ   = r'(%=)'     
t_AMPEQ   = r'(&=)'
t_OREQ    = r'(\|=)'
t_CAREQ   = r'(\^=)'
t_LLEQ    = r'(<<=)'
t_GGEQ    = r'(>>=)'
t_AMPCAREQ= r'(&\^=)'
t_AMPAMP  = r'(&&)'
t_OROR    = r'(\|\|)'
t_LMINUS  = r'(<-)'
t_PLUSPLUS= r'(\+\+)'
t_MINUSMIN= r'(--)'
t_EQEQ    = r'(==)'
t_LESS    = r'<'
t_GREAT   = r'>'
t_EQUAL   = r'='
t_NOT     = r'!'
t_NOTEQ   = r'(!=)'
t_LEQ     = r'(<=)'
t_GEQ     = r'(>=)'
t_COLONEQ = r'(:=)'
t_DDD	  = r'(\.\.\.)'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_COMMA   = r'\,'
t_DOT     = r'\.'
t_SEMICOL = r'\;'
t_COLON   = r'\:'
t_PD      = r'%d'
t_PS      = r'%s'

# === REGEX DEFINITIONS WITH ACTIONS === #
def t_INTERFACE(t):
    r'interface'
    return t

def t_CONSTANT(t):
    r'true$|false$|iota$'
    return t

def t_TYPEX(t):
    r'\bint\b|\bfloat\b|\bstring\b|\bcomplex\b|\bbool\b'
    t.value=t.value.replace(" ","")
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

def t_RUNE(t):
    r'\'(.|(\\[abfnrtv]))\''
    t.value = (t.value[1:-1])
    return t

def t_STRING(t):
    r'(\"[^\"]*\")|(\`[^\`]*\`) '
    t.value=t.value[1:-1]
    return t

def t_IMAGINARY(t):
    r'(([0-9](_?[0-9]+)*(\.[0-9](_?[0-9]+)*)?)[eE]\-[0-9](_?[0-9]+)*)i|([0-9](_?[0-9]+)*\.[0-9](_?[0-9]+)*)([eE][\+]?[0-9](_?[0-9]+)*)?i|(\d+)i'
    t.value = complex(t.value.replace('i', 'j'))
    return t

def t_FLOAT(t):
    r'(([0-9](_?[0-9]+)*(\.[0-9](_?[0-9]+)*)?)[eE]\-[0-9](_?[0-9]+)*)|([0-9](_?[0-9]+)*\.[0-9](_?[0-9]+)*)([eE][\+]?[0-9](_?[0-9]+)*)?'
    t.value = float(t.value.replace("_",""))
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lex.lex()
