import ply.yacc as yacc
import mylexer
import argparse
import pprint as pp
from utils import Node, SymbolTable
from scope import *
import ast
import cPickle as pickle

argparser = argparse.ArgumentParser()
argparser.add_argument("--input",help = "Specify the input file to parse.")
argparser.add_argument("--code",help = "Specify the 3AC output file.")
argparser.add_argument("--table",help = "Specify the symbol table output file.")
args = argparser.parse_args()
infile = args.input
codefile = args.code
tablefile = args.table

tokens = mylexer.tokens

def make_node(label):
	None

def make_edge(node1, node2, label=''):
	None

def getIdInfo(ide):
	if not inScope(ide):
		return None 
	else:
		id_scope = getScope(ide)
		if id_scope is not None:
			return id_scope.getEntry(ide)
		else:
			return None

def type_size(t):
			
	if t == 'int':
		return 4
	elif t == 'float':
		return 8
	elif t[0:6] == 'Struct':
		res = 0
		field_dic = ast.literal_eval(t[6:])
		for variables in field_dic:
			res += type_size(field_dic[variables])
		return res
	elif t[0:5] == 'Array':
		try:
			length = int(t[6:-1].split(',')[0])
			element_type = ','.join(t[6:-1].split(',')[1:])[1:]
			return length*type_size(element_type)
		except:
			length = t[6:-1].split(',')[0]
			element_type = ','.join(t[6:-1].split(',')[1:])[1:]
			return 4
	return 1

def insertId(idname, idtype):
	err = ""
	if len(idname) >= 8 and idname[:8] == 'TEMP_VAR':
		err = "Can't use temp_var as variable name: Reserved"
		return err 
	if inCurrentScope(idname):
		err = "Variable already exists in current scope"
		return err
	else:
		
		curr_scope = scope_stack[-1]
		curr_scope.insert(idname, idtype)
		# TODO struct types etc??
		insertInfo(idname, 'offset', curr_scope.offset)
		curr_scope.offset += type_size(idtype)

def insertType(name, ttype):
	err = ""
	curr_types = scope_stack[-1].types
	if name in curr_types:
		err = "type variable already exists"
		return err
	scope_stack[-1].types[name] = ttype

def insertInfo(idname, attr, value):
	if not inScope(idname):
		err = "variable does not exist", idname, attr, value
		print err
	else:
		curr_scope = getScope(idname)
		curr_scope.setArgs(idname, attr, value)

def typeInScope(name):
	for scope in scope_stack[::-1]:
		types = scope.types
		if name in types:
			return True
	return False

def validTypeConversion(type1, type2):
	if type1 == 'string':
		return False
	if type1 == 'float' and type2 == 'int':
		return False
	return True

temp_var_count = 0
function_expr_types = [] # used to store return types

def newTemp(idtype):
	curr_scope = scope_stack[-1]
	global temp_var_count
	new_temp = 'TEMP_VAR' + str(temp_var_count)
	curr_scope.insert(new_temp, idtype)
	insertInfo(new_temp, 'constant', False)
	temp_var_count += 1
	return new_temp
	# need to remove this from variable lists??

label_count = 0
def newLabel():
	global label_count
	new_label = 'label' + str(label_count)
	label_count += 1
	return new_label

global_symbol_table = SymbolTable(None)
scope_stack.append(global_symbol_table)
scope_list.append(global_symbol_table)

precedence = (
	('right','EQUAL', 'NOT'),
	('left', 'OROR'),
	('left', 'AMPAMP'),
	('left', 'EQEQ', 'NOTEQ', 'LESS', 'GREAT','LEQ','GEQ'),
	('left', 'PLUS', 'MINUS', 'OR', 'CARET'),
	('left', 'TIMES', 'DIVIDE', 'MOD', 'LL', 'GG', 'AMPERS', 'AMPCAR')
)

#-------------------------------Start------------------------------#

def p_start(p):
	'''start : Source'''
	p[0] = p[1]

#----------------------------------------------------------------------------------#


#-------------------------------Types------------------------------#

def p_type(p):
	'''Type : TypeName 
			| TypeLit 
			| LPAREN Type RPAREN'''
	if len(p) == 4:
		p[0] = p[2]
	else:
		p[0] = p[1]


def p_type_name(p):
	'''TypeName : TYPEX
				| TTYPE IDENTIFIER'''

	temp = Node()
	if len(p) == 3:
		temp.type = p[1] + '_' + p[2]
		if not typeInScope(p[2]):
			print 'error at line', p.lineno(0), 'type ' + temp.type + ' not in scope'
	else:
		temp.type = p[1]
	p[0] = temp

def p_type_lit(p):
	'''TypeLit : ArrayType
			   | StructType
			   | PointerType
			   | FunctionType'''
	p[0] = p[1]
	  
def p_type_opt(p):
	'''TypeOpt : Type
			   | epsilon'''
	if p[1] == 'epsilon':
		p[0] = None
	else:
		p[0] = p[1]

#----------------------------------------------------------------------------------#


#-------------------------------ArrayType------------------------------#

def p_array_type(p):
	'''ArrayType : LBRACK ArrayLength RBRACK ElementType'''
	p[0] = Node()
	p[0].type = 'Array(' + str(p[2].place) + ', ' + p[4].type + ')'

def p_array_length(p):
	''' ArrayLength : Expression '''
	p[0] = p[1]
	if p[1].expr.type != 'int':
		print 'error at line', p.lineno(0), "array size is of non-integral type"

def p_element_type(p):
	''' ElementType : Type '''
	p[0] = p[1]

#----------------------------------------------------------------------------------#


#-------------------------------StructType------------------------------#

def p_struct_type(p):
	'''StructType : STRUCT LBRACE FieldDeclRep RBRACE'''
	p[0] = Node()
	p[0].type = "Struct{" + p[3][1:] + "}"

def p_field_decl_rep(p):
  	''' FieldDeclRep : FieldDeclRep FieldDecl SEMICOL
				  | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0] += ',' + p[2]
	else:
		p[0] = ""

def p_field_decl(p):
	''' FieldDecl : IdentifierList Type TagOpt'''
	### TODO Embedded Field and TAG
	p[0] = ""
	for i in p[1].idlist:
		p[0] += "'" + i + "'" + ':' + "'" + p[2].type + "'"

def p_tag_opt(p):
  	''' TagOpt : Tag
			 | epsilon '''
	if p[1] == 'epsilon':
		p[0] = -1
	else:
		p[0] = p[1]

def p_tag(p):
	''' Tag : STRING '''
	p[0] = make_node(p[1])

#----------------------------------------------------------------------------------#


#-------------------------------PointerType------------------------------#

def p_pointer_type(p):
	'''PointerType : TIMES BaseType'''
	p[0] = Node()
	p[0].type = p[2].type + '*'

def p_base_type(p):
	'''BaseType : Type'''
	p[0] = p[1]

#----------------------------------------------------------------------------------#


#-------------------------------FunctionType------------------------------#

def p_function_type(p):
	'''FunctionType : FUNC Signature'''
	p[0] = p[2]

def p_signature(p):
	'''Signature : Parameters ResultOpt'''
	p[0] = [p[1], p[2]]
	addScope()
	insertInfo(current_func_name, 'func_signature', p[0])
	scope_stack[-1].is_func_table=True
	for var_dict in p[1]:
		for var_type in var_dict:
			variables = var_dict[var_type]
			for v in variables:
				insertId(v, var_type)
				insertInfo(v, 'constant', False)
	for var_dict in p[2]:
		if type(var_dict) == dict:
			for var_type in var_dict:
				variables = var_dict[var_type]
				for v in variables:
					insertId(v, var_type)
					insertInfo(v, 'constant', False)

def p_result_opt(p):
	'''ResultOpt : Result
				 | epsilon'''
	if p[1] == 'epsilon':
		p[0] = []
	else:
		p[0] = p[1]

def p_result(p):
	'''Result : Parameters
			  | Type'''
	if type(p[1]) == list:
		p[0] = p[1]
	else:
		p[0] = [p[1].type]

def p_parameters(p):
	'''Parameters : LPAREN ParameterListOpt RPAREN'''
	p[0] = p[2]

def p_parameter_list_opt(p):
	'''ParameterListOpt : ParametersList
						| epsilon'''
	if p[1] == 'epsilon':
		p[0] = []
	else:
		p[0] = p[1]

def p_parameter_list(p):
	'''ParametersList : Type
					  | IdentifierList Type
					  | ParameterDeclCommaRep'''
	if len(p) == 3:
		temp = {}
		temp[p[2].type] = []
		for i in p[1].idlist:
			temp[p[2].type].append(i)
		p[0] = [temp]
	elif type(p[1]) == list:
		p[0] = p[1]
	else:
		tempdict = {}
		tempdict[p[1].type] = []
		p[0] = [tempdict]

def p_parameter_decl_comma_rep(p):
	'''ParameterDeclCommaRep : ParameterDeclCommaRep COMMA ParameterDecl
							 | ParameterDecl COMMA ParameterDecl'''
	if type(p[1]) == list:
		p[0] = p[1]
		p[0].append(p[3])
	else:
		p[0] = [p[1], p[3]]

def p_parameter_decl(p):
	'''ParameterDecl : IdentifierList Type
					 | Type'''
	p[0] = {}
	if len(p) == 3:
		p[0][p[2].type] = []
		for i in p[1].idlist:
			p[0][p[2].type].append(i)
	else:
		p[0][p[1].type] = []

#----------------------------------------------------------------------------------#


#-----------------------Blocks---------------------------

def p_block(p):
	'''Block : CreateScope LBRACE StatementList RBRACE'''
	p[0] = p[3]
	p[0].extra['block_scope'] = currentScopelabel()
	deleteScope()


def p_create_scope(p):
	'''CreateScope : epsilon '''
	if not (scope_stack[-1].is_func_table or scope_stack[-1].is_for_table):
		addScope()
	scope_stack[-1].is_func_table = False
	scope_stack[-1].is_for_table = False
def p_statement_list(p):
	'''StatementList : StatementRep'''
	p[0] = p[1]

def p_statement_rep(p):
	'''StatementRep : StatementRep Statement SEMICOL
					| epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].code += p[2].code
		p[2].forclause.next[0] = p[0].forclause.next
		p[2].forclause.begin[0] = p[0].forclause.begin
		if p[2].extra:
			if 'is_continue' in p[2].extra and p[2].extra['is_continue']:
				p[2].next[0] = p[0].forclause.begin
			if 'is_break' in p[2].extra and p[2].extra['is_break']:
				p[2].next[0] = p[0].forclause.next
	else:
		p[0] = Node()

# -------------------------------------------------------


# ------------------DECLARATIONS and SCOPE------------------------

def p_decl(p):
	'''Declaration : ConstDecl
					| TypeDecl
					| VarDecl'''
	p[0] = p[1]

def p_toplevel_decl(p):
	'''TopLevelDecl : Declaration
					| FunctionDecl'''
		### TODO Method Declaration
	p[0] = p[1]

# -------------------------------------------------------


# ------------------CONSTANT DECLARATIONS----------------

def p_const_decl(p):
	'''ConstDecl : CONST ConstSpec
				 | CONST LPAREN ConstSpecRep RPAREN'''
	p[0] = Node()
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = p[3]

def p_const_spec_rep(p):
	'''ConstSpecRep : ConstSpecRep ConstSpec SEMICOL
					| epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].code += p[2].code
	else:
		p[0] = Node()

### TODO check constant modification
def p_const_spec(p):
	'''ConstSpec : IdentifierList TypeExprListOpt'''
	p[0] = Node()
	if p[2] is None:
		print "error: at line", p.lineno(0), "No assigned values to constants"
	else: 
		if len(p[2].exprlist) != len(p[1].idlist):
			lineno = p.lineno(0)
			print "error: unequal number of arguments on lhs and rhs at line", lineno
		else:
			if p[2].type:
				for i in range(len(p[2].exprlist)):
					if p[2].exprlist[i].expr.type != p[2].type:
						print 'error: at line', p.lineno(0), 'type mismatch in variable and expression'
					err = insertId(p[1].idlist[i], p[2].type)
					if err:
						print 'error: at line', p.lineno(0), err
					insertInfo(p[1].idlist[i], 'value', p[2].exprlist[i].place)
					insertInfo(p[1].idlist[i], 'constant', True)
					scope_label = scope_stack[-1].label
					p[0].code += p[2].exprlist[i].code + ['(' + str(scope_label) + ')' ] + [p[1].idlist[i] + ' := ' + p[2].exprlist[i].place]
			else:
				for i in range(len(p[2].exprlist)):
					err = insertId(p[1].idlist[i], p[2].exprlist[i].expr.type)
					if err:
						print 'error: at line', p.lineno(0), err
					insertInfo(p[1].idlist[i], 'value', p[2].exprlist[i].place)
					insertInfo(p[1].idlist[i], 'constant', True)
					scope_label = scope_stack[-1].label
					p[0].code += p[2].exprlist[i].code + ['(' + str(scope_label) + ')'] + [p[1].idlist[i] + ' := ' + p[2].exprlist[i].place]

def p_type_expr_list(p):
	'''TypeExprListOpt : TypeOpt EQUAL ExpressionList
					   | epsilon'''
	if len(p) == 4:
		p[0] = Node()
		if p[1] is not None:
			p[0].type = p[1].type
		
		p[0].exprlist = p[3].exprlist 
	else:
		p[0] = None

def p_identifier_list(p):
	'''IdentifierList : IDENTIFIER IdentifierRep'''
	p[0] = p[2]
	p[0].idlist.append(p[1])

def p_identifier_rep(p):
	'''IdentifierRep : IdentifierRep COMMA IDENTIFIER
					 | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].idlist.append(p[3])
	else:
		p[0] = Node()

# -------------------------------------------------------


# ------------------TYPE DECLARATIONS-------------------

def p_type_decl(p):
	'''TypeDecl : TYPE TypeSpec
				| TYPE LPAREN TypeSpecRep RPAREN'''
	p[0] = Node()

def p_type_spec_rep(p):
	'''TypeSpecRep : TypeSpecRep TypeSpec SEMICOL
				   | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = []

def p_type_spec(p):
	'''TypeSpec : AliasDecl
				| TypeDef'''
	p[0] = p[1]

def p_alias_decl(p):
	'''AliasDecl : IDENTIFIER EQUAL Type'''
	err = insertType(p[1], p[3].type)
	if err:
		print 'error at line', p.lineno(0), err 
	p[0] = None

# -------------------------------------------------------


# -------------------TYPE DEFINITIONS--------------------

def p_type_def(p):
	'''TypeDef : TTYPE IDENTIFIER Type'''
	err = insertType(p[1] + '_' + p[2], p[3].type)
	if err:
		print 'error at line', p.lineno(0), err
	p[0] = None

# -------------------------------------------------------


# ----------------VARIABLE DECLARATIONS------------------

def p_var_decl(p):
	'''VarDecl : VAR VarSpec
			   | VAR LPAREN VarSpecRep RPAREN'''	
	p[0] = Node()
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = p[3]

def p_var_spec_rep(p):
	'''VarSpecRep : VarSpecRep VarSpec SEMICOL
				  | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].code += p[2].code 
	else:
		p[0] = Node()

def p_var_spec(p):
	'''VarSpec : IdentifierList Type ExpressionListOpt
			   | IdentifierList EQUAL ExpressionList'''
	p[0] = Node()
	if p[2] == '=':
		if len(p[3].exprlist) != len(p[1].idlist):
			lineno = p.lineno(2)
			print "error: unequal number of arguments on lhs and rhs at line", lineno 
		else:
			for i in range(len(p[3].exprlist)):
				err = insertId(p[1].idlist[i], p[3].exprlist[i].expr.type)
				if err:
					print 'error: at line', p.lineno(0), err
				insertInfo(p[1].idlist[i], 'value', p[3].exprlist[i].place)
				insertInfo(p[1].idlist[i], 'constant', False)
				# need to add scope label lable to identifier
				scope_label = scope_stack[-1].label
				p[0].code += p[3].exprlist[i].code + [p[1].idlist[i] + '(' + str(scope_label) + ')' + ' := ' + p[3].exprlist[i].place]
	else:
		p[0] = Node()
		if not p[3]:
			for i in p[1].idlist:
				if p[2].type[0:5] == 'Array':
					try:
						int(p[2].type[6:-1].split(',')[0])
					except:
						element_type = ','.join(p[2].type[6:-1].split(',')[1:])[1:]
						p[0].code += ['Allocate ' + i + ' ' +  p[2].type[6:-1].split(',')[0] + ' ' + element_type]
				
				err = insertId(i, p[2].type)
				if p[2].type == 'int':
					insertInfo(i, 'value', 0)
				elif p[2].type == 'float':
					insertInfo(i, 'value', 0.0)
				elif p[2].type == 'string':
					insertInfo(i, 'value', '')
				### TODO bool type
				insertInfo(i, 'constant', False)

				if err:
					print 'error: at line', p.lineno(0), err
		else:
			if len(p[3].exprlist) != len(p[1].idlist):
				lineno = p.lineno(2) # TODO correct line send up where actual token is
				print "error: unequal number of arguments on lhs and rhs at line", lineno 
			else:
				for i in range(len(p[3].exprlist)):
					if p[3].exprlist[i].expr.type != p[2].type:
						print 'error: at line', p.lineno(0), 'type mismatch in variable and expression'
					err = insertId(p[1].idlist[i], p[2].type)
					if err:
						print 'error: at line', p.lineno(0), err
					insertInfo(p[1].idlist[i], 'value', p[3].exprlist[i].place)
					insertInfo(p[1].idlist[i], 'constant', False)
					scope_label = scope_stack[-1].label
					p[0].code += p[3].exprlist[i].code + [p[1].idlist[i] + '(' + str(scope_label) + ')' + ' := ' + p[3].exprlist[i].place]
					
					#TODO always insert info? what is attribute value?
					#TODO which attributes to be added in symbol table!

def p_expr_list_opt(p):
	'''ExpressionListOpt : EQUAL ExpressionList
						 | epsilon'''
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = None

# -------------------------------------------------------
	

# ----------------SHORT VARIABLE DECLARATIONS-------------

def p_short_var_decl(p):
	''' ShortVarDecl : IDENTIFIER COLONEQ Expression '''
	p[0] = Node()
	err = insertId(p[1], p[3].expr.type)
	if err:
		print 'error: at line', p.lineno(0), err
		return
	insertInfo(p[1], 'constant', False)
	scope_label = scope_stack[-1].label
	p[0].code += p[3].code + [p[1] + '(' + str(scope_label) + ')' + ' := ' + p[3].place]

# -------------------------------------------------------


# ----------------FUNCTION DECLARATIONS------------------

current_func_name = None

def p_func_decl(p):
	'''FunctionDecl : FUNC FunctionName Function
					| FUNC FunctionName Signature'''
					
	p[0] = p[3][1]
	if type(p[3]) == tuple:
		
		# return_types = p[3][0][1]
		# correct_types = []
		# for ret_dict in return_types:
		# 	for ret_type in ret_dict:
		# 		correct_types += [ret_type] * len(ret_dict[ret_type])
		# print correct_types
		# print function_expr_types
		
		# if function_expr_types:
		# 	if correct_types != function_expr_types[0]:
		# 		print 'error at line', p.lineno(0), "type mismatch in return value in function", p[2]
		# 	function_expr_types.pop()
		# else:
		# 	# TODO 
		# 	if correct_types:
		# 		print 'error at line', p.lineno(0), 'expected return value for function', p[2]

		func_dict = {}
		func_dict['symbol_table'] = p[3][1].extra['block_scope']
		insertInfo(p[2], 'func_dict', func_dict)
		# insertInfo(p[2], 'func_signature', p[3][0]) # CHANGED!!
		p[0].code = [newLabel() + ' function ' + p[2] + ":" ] + p[0].code
	else:
		insertInfo(p[2], 'func_signature', p[3])
		# TODO
		print p[3]



def p_func_name(p):
	'''FunctionName : IDENTIFIER'''
	p[0] = p[1]
	err = insertId(p[1], 'func')
	global current_func_name
	current_func_name = p[1]
	if err:
		print 'error at line', p.lineno(0), err
		return 

def p_func(p):
	'''Function : Signature FunctionBody'''
	p[0] = (p[1], p[2])

def p_func_body(p):
	'''FunctionBody : Block'''
	p[0] = p[1]
	

# -------------------------------------------------------


# -------------------QUALIFIED IDENTIFIER----------------

# def p_quali_ident(p):
# 	'''QualifiedIdent : IDENTIFIER DOT TypeName'''
# 	p[0] = ['QualifiedIdent', p[1], '.', p[3]]

# -------------------------------------------------------


# ----------------------OPERAND----------------------------

def p_operand(p):
	'''Operand : Literal
			   | OperandName
			   | LPAREN Expression RPAREN'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[2]

def p_literal(p):
	'''Literal : BasicLit'''
			   #| CompositeLit'''
	p[0] = p[1]

def p_basic_lit(p):
	'''BasicLit : IntLiteral
				| FloatLiteral
				| ImgLiteral
				| RuneLiteral
				| StringLiteral'''
	p[0] = p[1]

def p_int_literal(p):
	'''IntLiteral : INTEGER'''
	p[0] = Node()
	p[0].expr.value = p[1]
	p[0].expr.type = 'int'
	p[0].expr.is_constant = True
	p[0].place = str(p[0].expr.value)

def p_float_literal(p):
	'''FloatLiteral : FLOAT'''
	p[0] = Node()
	p[0].expr.value = p[1]
	p[0].expr.type = 'float'
	p[0].expr.is_constant = True
	p[0].place = str(p[0].expr.value)

def p_img_literal(p):
	'''ImgLiteral : IMAGINARY'''
	p[0] = Node()
	p[0].expr.value = p[1]
	p[0].expr.type = 'imaginary'
	p[0].expr.is_constant = True
	p[0].place = str(p[0].expr.value)

def p_rune_literal(p):
	'''RuneLiteral : RUNE'''
	p[0] = Node()
	p[0].expr.value = p[1]
	p[0].expr.type = 'rune'
	p[0].expr.is_constant = True
	p[0].place = str(p[0].expr.value)

def p_string_literal(p):
	'''StringLiteral : STRING'''
	p[0] = Node()
	p[0].expr.value = p[1]
	p[0].expr.type = 'string'
	p[0].expr.is_constant = True
	p[0].place = str(p[0].expr.value)

def p_operand_name(p):
	'''OperandName : IDENTIFIER'''
	p[0] = Node()
	if not inScope(p[1]):
		print "error at line", p.lineno(0), 'Variable not Declared'
	scope_label = getScope(p[1]).label	 
	# we are proceeding forward assumng the variable had already been declared!
	p[0] = Node()
	p[0].expr.value = p[1]
	temp = getIdInfo(p[1])
	p[0].place = str(p[0].expr.value) + '(' + str(scope_label) + ')'
	if temp is not None:
		p[0].expr.type = temp['type']

# ---------------------------------------------------------


# -----------------CONVERSIONS-----------------------------

def p_conversion(p):
	'''Conversion : Type LPAREN Expression RPAREN'''
	p[0] = Node() 
	if not validTypeConversion(p[3].expr.type, p[1].type):
		print 'error at line', p.lineno(0), 'invalid type conversion'
		return
	p[0].place = newTemp(p[1].type)
	p[0].code += p[3].code + [p[0].place + ' := ' + p[3].expr.type + 'TO' + p[1].type + ' ' + p[3].place]
	p[0].expr.type = p[1].type

# ---------------------------------------------------------


# ------------------PRIMARY EXPRESSIONS--------------------

def p_prim_expr(p):
	'''PrimaryExpr : Operand
				   | Conversion
				   | PrimaryExpr Selector
				   | PrimaryExpr Index
				   | PrimaryExpr Slice
				   | PrimaryExpr Arguments'''
				  #  | PrimaryExpr TypeAssertion'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = Node()

		if 'is_index' in p[2].extra:
			temp_type = p[1].expr.type
			if temp_type[0:5] != 'Array':
				print 'error at line', p.lineno(0), "can't index non-array types"

			if p[2].expr.type != 'int':
				print 'error at line', p.lineno(0), "array index is of non-integral type"

			try:
				length = int(temp_type[6:-1].split(',')[0])
				if type(p[2].expr.value) == int and p[2].expr.value >= length:
					print 'error at line', p.lineno(0), "index out of bounds"
			except:
				pass
				
			element_type = ','.join(temp_type[6:-1].split(',')[1:])[1:]
			p[0].expr.type = element_type
			# p[0].place = newTemp(element_type)
			p[0].place = p[1].place + '[' + p[2].place + ']'
			p[0].expr.value = p[1].expr.value
			
			# p[0].code = p[1].code + p[2].code + [p[0].place + ' := ' + p[1].place + '[' + p[2].place + ']']
			p[0].code = p[1].code + p[2].code

		if 'selector' in p[2].extra:
			selector = p[2].extra['selector']
			temp_type = p[1].expr.type
			if temp_type[0:6] != 'Struct':
				print 'error at line', p.lineno(0), "can't selct on non-struct types"
				return
			field_dic = ast.literal_eval(temp_type[6:])
			if selector not in field_dic:
				print 'error at line', p.lineno(0), "invalid selector"
				return
			p[0].expr.type = field_dic[selector]
			p[0].place = newTemp(p[0].expr.type)
			p[0].code = p[1].code + [p[0].place + ' := ' + p[1].place + '.' + selector]

		if 'is_argument' in p[2].extra:
			temp_type = p[1].expr.type
			if temp_type != 'func':
				print 'error at line', p.lineno(0), "need function type"
				return
			
			p[1].place = p[1].place.split('(')[0]
			func_params = getIdInfo(p[1].place)['func_signature'][0]
			func_result = getIdInfo(p[1].place)['func_signature'][1]
			params_type_list = []
			
			for args in func_params:
				key = args.keys()[0]
				value = args[key]
				if not value: # checking empty list
					params_type_list.append(key)
				for v in value:
					params_type_list.append(key)
			exprlist = p[2].exprlist
			exprlist.insert(0, exprlist[-1])
			exprlist.pop()
			exprlist_types = [a.expr.type for a in exprlist]
			if len(params_type_list) != len(exprlist_types):
				print 'error at line', p.lineno(0), "unequal number of arguments"
				return
			if params_type_list != exprlist_types:
				print 'error at line', p.lineno(0), 'type mismatch in argument'
			arguments = [a.place for a in exprlist]
			for i in exprlist:
				p[0].code += i.code
			for arg in arguments:
				p[0].code += ['param ' + arg]
			if not func_result:
				p[0].code += ['callvoid ' + p[1].place + ', ' + str(arguments)]
				p[0].expr.type = 'void'
			else: ### TODO multiple return values
				for arg in func_result:
					result = arg
					break
				if type(result) == dict:
					new_place = newTemp(result.keys()[0])
					p[0].expr.type = result.keys()[0]
					p[0].place = new_place
					p[0].code += ['call' + result.keys()[0] + ', ' + new_place + ', ' + p[1].place]
				else:
					new_place = newTemp(result)
					p[0].expr.type = result
					p[0].place = new_place
					p[0].code += ['call' + result + ', ' + new_place + ', ' + p[1].place]


def p_selector(p):
	'''Selector : DOT IDENTIFIER'''
	p[0] = Node()
	p[0].extra['selector'] = p[2]

def p_index(p):
	'''Index : LBRACK Expression RBRACK'''
	p[0] = p[2]
	p[0].extra['is_index'] = True

def p_slice(p):
	'''Slice : LBRACK ExpressionOpt COLON ExpressionOpt RBRACK'''
			#  | LBRACK ExpressionOpt COLON Expression COLON Expression RBRACK'''
	p[0] = make_node('slice')
	if p[2] != - 1:
		make_edge(p[0], p[2], 'low')
	if p[4] != - 1:
		make_edge(p[0], p[4], 'high')
	

# def p_type_assert(p):
# 	'''TypeAssertion : DOT LPAREN Type RPAREN'''
# 	p[0] = ['TypeAssertion', '.', '(', p[3], ')']

def p_argument(p):
	'''Arguments : LPAREN ExpressionListTypeOpt RPAREN'''
	p[0] = p[2]
	p[0].extra['is_argument'] = True


def p_expr_list_type_opt(p):
	'''ExpressionListTypeOpt : ExpressionList
							 | epsilon'''
	if p[1] == 'epsilon':
		p[0] = Node()
	else:
		p[0] = p[1]

#def p_comma_opt(p):
#    '''CommaOpt : COMMA
#                | epsilon'''
#    if p[1] == ',':
#        p[0] = ['CommaOpt', ',']
#    else:
#        p[0] = ['CommaOpt', p[1]]

# def p_expr_list_comma_opt(p):
# 	'''ExpressionListCommaOpt : COMMA ExpressionList
# 							  | epsilon'''
# 	if len(p) == 3:
# 		p[0] = ['ExpressionListCommaOpt', ',', p[2]]
# 	else:
# 		p[0] = ['ExpressionListCommaOpt', p[1]]

def p_expr_list(p):
	'''ExpressionList : Expression ExpressionRep'''
	p[0] = p[2]
	p[0].exprlist.append(p[1])

def p_expr_rep(p):
	'''ExpressionRep : ExpressionRep COMMA Expression
					 | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].exprlist.append(p[3])
	else:
		p[0] = Node()

# ---------------------------------------------------------


#----------------------OPERATORS-------------------------

def p_expression(p):
	'''Expression : UnaryExpr
				  | Expression OROR Expression
					| Expression AMPAMP Expression
					| Expression EQEQ Expression
					| Expression NOTEQ Expression
					| Expression LESS Expression
					| Expression GREAT Expression
					| Expression LEQ Expression
					| Expression GEQ Expression
					| Expression PLUS Expression
					| Expression MINUS Expression
					| Expression OR Expression
					| Expression CARET Expression
					| Expression TIMES Expression
					| Expression DIVIDE Expression
					| Expression MOD Expression
					| Expression AMPERS Expression
					| Expression LL Expression
					| Expression GG Expression
					| Expression AMPCAR Expression'''
	if len(p) == 4:
		p[0] = Node()

		binary_ops = ['+', '-', '*', '/', '%']
		if p[2] in binary_ops:
			exprtypes = ['int', 'float', 'imaginary']
			if p[1].expr.type != p[3].expr.type:
				# TODO int/float typecasting
				print 'error: at line', p.lineno(0), "type mismatch in comparison"
				return
			exprtype = p[1].expr.type
			if exprtype not in exprtypes:
				print 'error: at line', p.lineno(0), "operation not supported on the given type"
				return
			else:
				if p[1].expr.is_constant and p[3].expr.is_constant:
					p[0].expr.type = exprtype
					p[0].expr.is_constant = True
					if p[2] == '+':
						p[0].expr.value = p[1].expr.value + p[3].expr.value
					if p[2] == '-':
						p[0].expr.value = p[1].expr.value - p[3].expr.value
					if p[2] == '*':
						p[0].expr.value = p[1].expr.value * p[3].expr.value
					if p[2] == '/':
						p[0].expr.value = p[1].expr.value / p[3].expr.value
					if p[2] == '%':
						p[0].expr.value = p[1].expr.value % p[3].expr.value
					p[0].place = str(p[0].expr.value)
				elif p[1].expr.is_constant:
					p[0].place = newTemp(exprtype)
					p[0].code = p[1].code + p[3].code + [p[0].place + ' := ' + p[3].place +' ' + exprtype + p[2]+ 'i ' + p[1].place]  #second operand is the immediate operand
					p[0].expr.type = exprtype
				elif p[3].expr.is_constant:
					p[0].place = newTemp(exprtype)
					p[0].code = p[1].code + p[3].code + [p[0].place + ' := ' + p[1].place + ' ' + exprtype + p[2]+ 'i '+ p[3].place]  #second operand is the immediate operand
					p[0].expr.type = exprtype
				else:
					p[0].place = newTemp(exprtype)
					p[0].code = p[1].code + p[3].code + [p[0].place + ' := ' + p[1].place + ' ' + exprtype + p[2]+ ' ' +  p[3].place]  #second operand is the immediate operand
					p[0].expr.type = exprtype
		
		rel_ops = ['==', '!=', '<', '>', '<=', '>=']
		if p[2] in rel_ops:
			#TODO check expression mismatch
			if p[1].expr.type != p[3].expr.type:
				print 'error: at line', p.lineno(0), "type mismatch in comparison"
				return 
			p[0].code = p[1].code + p[3].code + [['if ' + p[1].place + p[2] + p[3].place + ' goto ', p[0].expr.true_label]] + [['goto ', p[0].expr.false_label]]

		if p[2] == '||':
			p[1].expr.true_label[0] = p[0].expr.true_label
			p[1].expr.false_label[0] = newLabel()
			p[3].expr.true_label[0] = p[0].expr.true_label
			p[3].expr.false_label[0] = p[0].expr.false_label
			p[0].code = p[1].code + [p[1].expr.false_label[0] + ':'] + p[3].code
		if p[2] == '&&':
			p[1].expr.true_label[0] = newLabel()
			p[1].expr.false_label[0] = p[0].expr.false_label
			p[3].expr.true_label[0] = p[0].expr.true_label
			p[3].expr.false_label[0] = p[0].expr.false_label
			p[0].code = p[1].code + [p[1].expr.true_label[0] + ':'] + p[3].code



	else:
		p[0] = p[1]

def p_expr_opt(p):
	'''ExpressionOpt : Expression
					 | epsilon'''
	if p[1] == 'epsilon':
		p[0] = -1
	else:
		p[0] = p[1]

def p_unary_expr(p):
	'''UnaryExpr : PrimaryExpr
				 | UnaryOp UnaryExpr'''
				#  | NOT UnaryExpr'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = Node()
		if p[1] == '+':
			p[0] = p[2]
		if p[1] == '-':
			p[0] = p[2]
			old_place = p[2].place
			if p[2].expr.is_constant:
				p[0].expr.value = -p[2].expr.value
			p[0].place = newTemp(p[0].expr.type)
			p[0].code += p[2].code + [p[0].place + ' := 0 - ' + old_place]
		if p[1] == '*':
			p[0] = Node()
			if p[2].expr.type[-1] != '*':
				print 'error at line', p.lineno(0), "can't dereference: invalid type"
				return
			p[0].expr.type = p[2].expr.type[:-1]
			p[0].place = newTemp(p[0].expr.type)
			p[0].code = p[2].code + [p[0].place + ' := *' + p[2].place]

		if p[1] == '&':
			p[0] = Node()
			p[0].expr.type = p[2].expr.type + '*'
			p[0].place = newTemp(p[0].expr.type)
			p[0].code = p[2].code + [p[0].place + ' := &' + p[2].place] 
		if p[1] == '!':
			p[0] = Node()
			p[0].code = p[1].code
			p[1].expr.true_label[0] = p[0].expr.false_label
			p[1].expr.false_label[0] = p[0].expr.true_label

def p_unary_op(p):
	'''UnaryOp : PLUS
			   | MINUS
			   | TIMES
			   | AMPERS
			   | NOT '''
	p[0] = p[1]
	
# ---------------------------------------------------


# ---------------- STATEMENTS -----------------------

def p_statement(p):
	'''Statement : Declaration
				 | LabeledStmt
				 | SimpleStmt
				 | ReturnStmt
				 | BreakStmt
				 | ContinueStmt
				 | GotoStmt
				 | Block
				 | IfStmt
				 | ForStmt '''
				#  SwitchStmt'''
	p[0] = p[1] 
	
	if p[0].next[0][0] == 'l': 
		p[0].code += [p[0].next[0] + ':'] # otherwise not labelx

def p_simple_stmt(p):
	'''SimpleStmt : epsilon
				  | ExpressionStmt
				  | IncDecStmt
				  | Assignment
				  | ShortVarDecl '''
	if p[1] == 'epsilon':
		p[0] = -1
	else:
		p[0] = p[1]

def p_labeled_statements(p):
	''' LabeledStmt : Label COLON Statement '''
	p[0] = make_node(':')
	make_edge(p[0], p[1])
	if p[3] != -1:
		make_edge(p[0], p[3])

def p_label(p):
	''' Label : IDENTIFIER '''
	p[0] = make_node(p[1])

def p_expression_stmt(p):
	''' ExpressionStmt : Expression '''
	p[0] = p[1]

def p_inc_dec(p):
	''' IncDecStmt : PrimaryExpr PLUSPLUS
					| PrimaryExpr MINUSMIN '''
	# ''' IncDecStmt : Expression PLUSPLUS
	# 				| Expression MINUSMIN '''
	p[0] = p[1]
	if p[0].expr.type != 'int':
		print "error at line", p.lineno(0), 'can not increment non-int variable'
		return
	new_temp = newTemp('int')
	p[0].code += p[1].code + [new_temp + ' := ' + p[1].place + ' int'+p[2][0] + 'i 1'] + [p[1].place + ' := ' + new_temp]


def p_assignment(p):
	'''Assignment : ExpressionList assign_op ExpressionList'''
	# TODO restriction on LHS expressions
	p[0] = Node()
	if len(p[1].exprlist) != len(p[3].exprlist):
		print "error: at line", p.lineno(0), "Unequal number of arguments"
	else:
		for i in range(len(p[1].exprlist)):
			if not inScope(p[1].exprlist[i].expr.value):
				print "error: at line", p.lineno(0), "variable not in scope"
			else:
				if p[1].exprlist[i].expr.type != p[3].exprlist[i].expr.type:
					print "error: at line", p.lineno(0), "type mismatch is assighment"
					return
				exprtype = p[1].exprlist[i].expr.type
				p[0].expr.type = exprtype
				if p[2] == '=':
					p[0].code += p[1].exprlist[i].code + p[3].exprlist[i].code + [p[1].exprlist[i].place + ' := ' + p[3].exprlist[i].place]
				ops = ['+=', '-=', '*=', '/=', '%=']
				if p[2] in ops:
					new_temp = newTemp(exprtype)			
					p[0].code = p[1].exprlist[i].code + p[3].exprlist[i].code + [new_temp + ' := ' + p[1].exprlist[i].place + ' ' + exprtype + p[2][0] + ' ' +  p[3].exprlist[i].place]
					p[0].code += [p[1].exprlist[i].expr.value + ' := ' + new_temp]

def p_assign_op(p):
	''' assign_op : AssignOp'''
	p[0] = p[1]

def p_AssignOp(p):
	'''AssignOp : PLUSEQ
				| MINUSEQ
				| TIMESEQ
				| DIVIDEEQ
				| MODEQ
				| AMPEQ
				| OREQ
				| CAREQ
				| LLEQ
				| GGEQ
				| EQUAL '''
	p[0] = p[1]

 #----------------------------------------------------


 #--------------------IF STATEMENTS-------------------

def p_if_statement(p):
	''' IfStmt : IF Expression Block ElseOpt '''
	# no else statement
	p[0] = Node()
	p[3].forclause.next[0] = p[0].forclause.next
	p[3].forclause.begin[0] = p[0].forclause.begin

	if p[4] is None:
		new_label = newLabel()
		p[2].expr.true_label[0] = new_label
		p[2].expr.false_label[0] = p[0].next
		p[3].next[0] = p[0].next
		p[0].code += p[2].code + [new_label + ":"] + p[3].code
	
	else:
		p[4].forclause.next[0] = p[0].forclause.next
		p[4].forclause.begin[0] = p[0].forclause.begin
		p[2].expr.true_label[0] = newLabel()
		p[2].expr.false_label[0] = newLabel()
		p[3].next[0] = p[0].next
		p[4].next[0] = p[0].next
		p[0].code += p[2].code + [p[2].expr.true_label[0] + ":"] + p[3].code + [['goto ', p[0].next]] + [p[2].expr.false_label[0] + ":"] + p[4].code
	p[0].next[0] = newLabel()

# def p_SimpleStmtOpt(p):
# 	''' SimpleStmtOpt : SimpleStmt SEMICOL
# 						| epsilon '''
# 	if len(p) == 3:
# 		p[0] = ['SimpleStmtOpt', p[1], ';']
# 	else :
# 		p[0] = ['SimpleStmtOpt', p[1]]

def p_else_opt(p):
	''' ElseOpt : ELSE IfStmt
				| ELSE Block
				| epsilon '''
	if len(p) == 3:
		p[0] = p[2]
		p[2].forclause.next[0] = p[0].forclause.next
		p[2].forclause.begin[0] = p[0].forclause.begin
	else:
		p[0] = None

# ----------------------------------------------------------------


# ----------- SWITCH STATEMENTS ---------------------------------

# def p_switch_statement(p):
# 	''' SwitchStmt : ExprSwitchStmt
# 					| TypeSwitchStmt '''
# 	p[0] = ['SwitchStmt', p[1]]

# def p_expr_switch_stmt(p):
# 	''' ExprSwitchStmt : SWITCH ExpressionOpt LBRACE ExprCaseClauseRep RBRACE'''
# 	p[0] = ['ExpressionStmt', 'switch', p[2], p[3], '{', p[5], '}']

# def p_expr_case_clause_rep(p):
# 	''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
# 							| epsilon'''
# 	if len(p) == 3:
# 		p[0] = ['ExprCaseClauseRep', p[1], p[2]]
# 	else:
# 		p[0] = ['ExprCaseClauseRep', p[1]]

# def p_expr_case_clause(p):
# 	''' ExprCaseClause : ExprSwitchCase COLON StatementList'''
# 	p[0] = ['ExprCaseClause', p[1], ':', p[3]]

# def p_expr_switch_case(p):
# 	''' ExprSwitchCase : CASE ExpressionList
# 						| DEFAULT '''
# 	if len(p) == 3:
# 		p[0] = ['ExprSwitchCase', 'case', p[2]]
# 	else:
# 		p[0] = ['ExprSwitchCase', p[1]]

# def p_type_switch_stmt(p):
# 	''' TypeSwitchStmt : SWITCH SimpleStmtOpt TypeSwitchGuard LBRACE TypeCaseClauseOpt RBRACE'''
# 	p[0] = ['TypeSwitchStmt', 'switch', p[2], p[3],'{', p[5], '}']

# def p_type_switch_guard(p):
# 	''' TypeSwitchGuard : IdentifierOpt PrimaryExpr DOT LPAREN TYPE RPAREN '''

# 	p[0] = ['TypeSwitchGuard', p[1], p[2], '.', '(', 'type', ')']

# def p_identifier_opt(p):
# 	''' IdentifierOpt : IDENTIFIER COLONEQ
# 						| epsilon '''

# 	if len(p) == 3:
# 		p[0] = ['IdentifierOpt', p[1], ':=']
# 	else:
# 		p[0] = ['IdentifierOpt', p[1]]

# def p_type_case_clause_opt(p):
# 	''' TypeCaseClauseOpt : TypeCaseClauseOpt TypeCaseClause
# 							| epsilon '''
# 	if len(p) == 3:
# 		p[0] = ['TypeCaseClauseOpt', p[1], p[2]]
# 	else:
# 		p[0] = ['TypeCaseClauseOpt', p[1]]

# def p_type_case_clause(p):
# 	''' TypeCaseClause : TypeSwitchCase COLON StatementList'''
# 	p[0] = ['TypeCaseClause', p[1], ':', p[3]]

# def p_type_switch_case(p):
# 	''' TypeSwitchCase : CASE TypeList
# 						| DEFAULT '''
# 	if len(p) == 3:
# 		p[0] = ['TypeSwitchCase', p[1], p[2]]
# 	else:
# 		p[0] = ['TypeSwitchCase', p[1]]

# def p_type_list(p):
# 	''' TypeList : Type TypeRep'''
# 	p[0] = ['TypeList', p[1], p[2]]

# def p_type_rep(p):
# 	''' TypeRep : TypeRep COMMA Type
# 				| epsilon '''
# 	if len(p) == 4:
# 		p[0] = ['TypeRep', p[1], ',', p[3]]
# 	else:
# 		p[0] = ['TypeRep', p[1]]

# -----------------------------------------------------------


# --------- FOR STATEMENTS---------------

def p_for(p):
	'''ForStmt : CreateForScope FOR ConditionBlockOpt Block'''
	p[0] = Node()
	if p[3] is not None:
		p[0].begin = [newLabel()]
		p[4].forclause.next[0] = p[0].next
		if p[3].forclause.isClause:			
			cond = p[3].forclause.condition
			cond.expr.true_label[0] = newLabel()
			cond.expr.false_label[0] = p[0].next
			p[4].next[0] = p[0].begin # TODO TODO TODO check confirm
			p[4].begin[0] = p[0].begin
			update_label = [newLabel()]
			p[4].forclause.begin[0] = update_label
			p[0].code += p[3].forclause.initialise
			p[0].code += [[p[0].begin , ":"]] + cond.code + [cond.expr.true_label[0] + ":"] 
			p[0].code += p[4].code + [[update_label, ":"]] + p[3].forclause.update + [['goto: ',p[0].begin]]
		else:
			p[3].expr.true_label[0] = newLabel()
			p[3].expr.false_label[0] = p[0].next
			p[4].next[0] = p[0].begin # TODO TODO TODO check confirm
			p[4].forclause.begin[0] = p[0].begin 
			p[4].begin[0] = p[0].begin
			p[0].code += [[p[0].begin , ":"]] + p[3].code + [p[3].expr.true_label[0] + ":"] + p[4].code + [['goto: ',p[0].begin]]
	p[0].next[0] = newLabel()

def p_for_create_scope(p):
	''' CreateForScope : epsilon '''
	addScope()
	scope_stack[-1].is_for_table = True

def p_conditionblockopt(p):
	'''ConditionBlockOpt : epsilon
				| Condition
				| ForClause'''
				# | RangeClause'''
	if p[1] == 'epsilon':
		p[0] = None
	else:
		p[0] = p[1]

def p_condition(p):
	'''Condition : Expression '''
	p[0] = p[1]

def p_forclause(p):
	'''ForClause : SimpleStmt SEMICOL ConditionOpt SEMICOL SimpleStmt'''
	p[0] = Node()
	p[0].forclause.initialise = p[1].code
	p[0].forclause.update = p[5].code
	p[0].forclause.condition = p[3]
	p[0].forclause.isClause = True

def p_conditionopt(p):
	'''ConditionOpt : epsilon
			| Condition '''
	if p[1] == 'epsilon':
		p[0] = Node()
	else:
		p[0] = p[1]

def p_rageclause(p):
	'''RangeClause : ExpressionIdentListOpt RANGE Expression'''
	p[0] = ['RangeClause', p[1], 'range', p[3]]

def p_expression_ident_listopt(p):
	'''ExpressionIdentListOpt : epsilon
				| ExpressionIdentifier'''
	p[0] = ['ExpressionIdentListOpt', p[1]]

def p_expressionidentifier(p):
	'''ExpressionIdentifier : ExpressionList EQUAL'''
	if p[2] == '=':
		p[0] = ['ExpressionIdentifier', p[1], '=']
	else:
		### TODO how ??
		p[0] = ['ExpressionIdentifier', p[1], ':=']

#----------------------------------------------------------


#----------------------MISC--------------------------------

def p_return(p):
	'''ReturnStmt : RETURN ExpressionListPureOpt'''
	expr_types = []
	p[0] = Node()
	for expr in p[2].exprlist:
		p[0].code += expr.code
		expr_types.append(expr.expr.type)
	for index, expr in enumerate(p[2].exprlist):
		p[0].code += ['ret' + str(index+1) + ": " + expr.place]

	p[0].code += ['ret']
	p[0].extra['is_return'] = True
	function_expr_types.append(expr_types)
	

def p_expressionlist_pure_opt(p):
	'''ExpressionListPureOpt : ExpressionList
				| epsilon'''
	if p[0] != 'epsilon':
		p[0] = p[1]
	else:
		p[0] = []

def p_break(p):
	'''BreakStmt : BREAK LabelOpt'''
	p[0] = Node()
	p[0].code = [['goto ', p[0].next]]
	p[0].extra['is_break'] = True

def p_continue(p):
	'''ContinueStmt : CONTINUE LabelOpt'''
	p[0] = Node()
	
	p[0].code = [['goto ', p[0].next]]
	p[0].extra['is_continue'] = True

def p_labelopt(p):
	'''LabelOpt : Label
			| epsilon '''
	if p[1] != 'epsilon':
		p[0] = p[1]
	else:
		p[0] = -1

def p_goto(p):
	'''GotoStmt : GOTO Label '''
	p[0] = make_node(p[1])
	if p[2] != -1:
		make_edge(p[0], p[2])

# -----------------------------------------------------------


# ----------------  SOURCE FILE --------------------------------

def p_source_file(p):
	'''Source : PackageClause SEMICOL ImportDeclRep TopLevelDeclRep'''
	p[0] = p[4]

def p_import_decl_rep(p):
	'''ImportDeclRep : epsilon
			| ImportDeclRep ImportDecl SEMICOL'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = []

def p_toplevel_decl_rep(p):
	'''TopLevelDeclRep : TopLevelDeclRep TopLevelDecl SEMICOL
						| epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].code += p[2].code 
	else:
		p[0] = Node()
# --------------------------------------------------------


# ---------- PACKAGE CLAUSE --------------------

def p_package_clause(p):
	'''PackageClause : PACKAGE PackageName'''
	p[0] = make_node(p[1])
	temp = make_node(p[2])
	make_edge(p[0], temp)

def p_package_name(p):
	'''PackageName : IDENTIFIER'''
	p[0] = p[1]

# -----------------------------------------------


# --------- IMPORT DECLARATIONS ---------------

def p_import_decl(p):
	'''ImportDecl : IMPORT ImportSpec
			| IMPORT LPAREN ImportSpecRep RPAREN '''
	p[0] = make_node(p[1])
	if len(p) == 3:
		make_edge(p[0], p[2])
	else:
		for i in p[3]:
			make_edge(p[0], i)

def p_import_spec_rep(p):
	''' ImportSpecRep : ImportSpecRep ImportSpec SEMICOL
				| epsilon '''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = []

def p_import_spec(p):
	''' ImportSpec : PackageNameDotOpt ImportPath '''
	p[0] = p[2]
	if p[1] != -1:
		make_edge(p[0], p[1], 'as')

def p_package_name_dot_opt(p):
	''' PackageNameDotOpt : DOT
							| PackageName
							| epsilon'''
	if p[1] == 'epsilon':
		p[0] = -1
	else:
		p[0] = make_node(p[1])

def p_import_path(p):
	''' ImportPath : STRING '''
	p[0] = make_node(p[1])

# -------------------------------------------------------

def p_error(p):
  print('[SYNTAX ERROR] at line no. ' + str(p.lineno) + ' with token ' + str(p.type) + ' near \"' + str(p.value) + '\"')

def p_empty(p):
	'''epsilon : '''
	p[0] = 'epsilon'

# -------------------------------------------------------

parser = yacc.yacc()

f = open(infile, 'r')
input_str = f.read()
f.close()

try:
	t = parser.parse(input_str, tracking=True)
except Exception as e:
	print str(e)
	if str(e) == "\'NoneType\' object has no attribute \'lineno\'":
		print '[SYNTAX ERROR] SEMICOL missing at end of MAIN'

def retstring(item):
	if type(item) == list:
		out = ''
		for i in item:
			if type(i) == list:
				out += retstring(i)
			else:
				out += i
		return out
	else:
		return item

# for scope in scope_list[::-1]:
# 	entries = scope.getAllEntries()
# 	print 'offset***', scope.offset, scope.label
# 	pp.pprint(entries[0])

entries = global_symbol_table.getAllEntries()[0]
function_symtable = []
for entry in entries:
	if 'func_dict' in entries[entry]:
		function_symtable.append(entries[entry]['func_dict']['symbol_table'])


def computeOffsets(off_sum, parent):
	for scope in parent.children:
		# print off_sum
		# print 'parent', parent.label, parent.offset, 'child', scope.label, scope.offset
		# child_offset = scope.offset
		# parent_offset = parent.offset
		for entries in scope.table:
			if 'offset' in scope.table[entries]:
				scope.table[entries]['offset'] += off_sum
		# scope.offset += parent.offset
		off_sum += scope.offset
		off_sum = computeOffsets(off_sum, scope)
	return off_sum
		# parent.offset += child_offset 

# print function_symtable
for table in function_symtable:
	computeOffsets(scope_list[table].offset, scope_list[table])

f = open(codefile, 'w')
buf = ''
for item in t.code:
	buf += retstring(item) + '\n'
f.write(buf)
f.close()

f = open(tablefile, 'w').close()
f = open(tablefile, 'a')
for scope in scope_list[::-1]:
	entries = scope.getAllEntries()
	f.write('scope: ' + str(entries[1]) + '\n')
	f.write('parent: ' + str(entries[3]) + '\n')
	pp.pprint(entries[0], stream=f)
	pp.pprint(entries[2], stream=f)
	f.write('\n')
f.close()

f = open('symtab_pickle', 'w')
pickle.dump(scope_list, f)
f.close()