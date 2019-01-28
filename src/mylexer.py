import ply.lex as lex
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--cfg",help="takes the color configuration file")
parser.add_argument("input",help="takes the input program")
parser.add_argument("--output",help="takes the name of the output HTML file")
args=parser.parse_args()

cfg_file=args.cfg
inprgm=args.input
outfile=args.output
f1=open(inprgm)
f2=open(cfg_file)
mylist=f2.read()
mylist = [x.split(',') for x in mylist.splitlines()]

token_dic={}
for i in range(len(mylist)):
    x,y=mylist[i]
    token_dic[x]=y

keywords = ['var']
tokens = [ 'NAME','NUMBER','PLUS','MINUS','TIMES',
           'DIVIDE', 'EQUALS', 'SEMIC'] + [k.upper() for k in keywords]
t_ignore = ' |\t|\n'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_SEMIC  = r';'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lexer=lex.lex()         # Build the lexer

# Test it out
# data = '''
# 3 + 4 * 10
# + -20 *2
# '''

# Give the lexer some input
lexer.input(f1.read())

# Tokenize
tokens_lst=[]
while True:
 tok = lexer.token()
 if not tok:
     break      # No more input
 tokens_lst.append([tok.type,tok.value,token_dic[tok.type]])
print(tokens_lst)
