import ply.yacc as yacc
import mylexer
from graphviz import Digraph
import argparse
import pprint as pp

argparser = argparse.ArgumentParser()
argparser.add_argument("--input",help = "Specify the input file to parse.")
argparser.add_argument("--output",help = "Specify the output dot file.")
args = argparser.parse_args()
infile = args.input
outfile = args.output

tokens = mylexer.tokens
nodecount = 0
dot = Digraph()

def make_node(label):
	global nodecount
	dot.node(str(nodecount), label)
	nodecount += 1
	return nodecount - 1

def make_edge(node1, node2, label=''):
	dot.edge(str(node1), str(node2), label=label)

precedence = (
	('right','EQUAL', 'NOT'),
	('left', 'OROR'),
	('left', 'AMPAMP'),
	('left', 'OR'),
	('left', 'CARET'),
	('left', 'AMPERS'),
	('left', 'EQEQ', 'NOTEQ'),
	('left', 'LESS', 'GREAT','LEQ','GEQ'),
	('left', 'LL', 'GG'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE','MOD'),
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
	'''TypeName : TYPEX'''
				# | QualifiedIdent'''
	p[0] = make_node(p[1])

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
		p[0] = -1
	else:
		p[0] = p[1]

#----------------------------------------------------------------------------------#


#-------------------------------ArrayType------------------------------#

def p_array_type(p):
	'''ArrayType : LBRACK ArrayLength RBRACK ElementType'''
	p[0] = make_node('ArrayType')
	make_edge(p[0], p[2])
	make_edge(p[0], p[4])

def p_array_length(p):
	''' ArrayLength : Expression '''
	p[0] = p[1]

def p_element_type(p):
	''' ElementType : Type '''
	p[0] = p[1]

#----------------------------------------------------------------------------------#


#-------------------------------StructType------------------------------#

def p_struct_type(p):
	'''StructType : STRUCT LBRACE FieldDeclRep RBRACE'''
	p[0] = make_node(p[1])
	for i in p[3]:
		make_edge(p[0], i)

def p_field_decl_rep(p):
  	''' FieldDeclRep : FieldDeclRep FieldDecl SEMICOL
				  | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = []

def p_field_decl(p):
	''' FieldDecl : IdentifierList Type TagOpt'''
	### TODO Embedded Field
	p[0] = make_node('field')
	for i in p[1]:
		make_edge(p[0], i)
	make_edge(p[0], p[2], 'type')
	if p[3] != -1:
		make_edge(p[0], p[3], 'tag')

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
	p[0] = make_node('pointer')
	make_edge(p[0], p[1])

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
	p[0] = make_node('func')
	for i in p[1]:
		make_edge(p[0], i, 'arg')
	for i in p[2]:
		make_edge(p[0], i, 'return')

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
		p[0] = [p[1]]

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
		temp = make_node('parameter')
		for i in p[1]:
			make_edge(temp, i)
		make_edge(temp, p[2], 'type')
		p[0] = [temp]
	elif type(p[1]) == list:
		p[0] = p[1]
	else:
		p[0] = [p[1]]

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
	p[0] = make_node('parameter')
	if len(p) == 3:
		for i in p[1]:
			make_edge(p[0], i)
		make_edge(p[0], p[2], 'type')
	else:
		make_edge(p[0], p[1], 'type')

#----------------------------------------------------------------------------------#


#-----------------------Blocks---------------------------

def p_block(p):
	'''Block : LBRACE StatementList RBRACE'''
	p[0] = make_node('Block')
	for i in p[2]:
		if i != -1:
			make_edge(p[0], i)

def p_statement_list(p):
	'''StatementList : StatementRep'''
	p[0] = p[1]

def p_statement_rep(p):
	'''StatementRep : StatementRep Statement SEMICOL
					| epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = []

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
	p[0] = make_node(p[1])
	if len(p) == 3:
		make_edge(p[0], p[2])
	else:
		for i in p[3]:
			make_edge(p[0], i)

def p_const_spec_rep(p):
	'''ConstSpecRep : ConstSpecRep ConstSpec SEMICOL
					| epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = []

def p_const_spec(p):
	'''ConstSpec : IdentifierList TypeExprListOpt'''
	p[0] = make_node('ConstSpec')
	for i in p[1]:
		make_edge(p[0], i)
	if p[2] != -1:
		make_edge(p[0], p[2])

def p_type_expr_list(p):
	'''TypeExprListOpt : TypeOpt EQUAL ExpressionList
					   | epsilon'''
	if len(p) == 4:
		p[0] = make_node(p[2])
		if p[1] != -1:
			make_edge(p[0], p[1], 'type')
		for i in p[3]:
			make_edge(p[0], i)
	else:
		p[0] = -1

def p_identifier_list(p):
	'''IdentifierList : IDENTIFIER IdentifierRep'''
	temp = make_node(p[1])
	p[0] = p[2]
	p[0].append(temp)

def p_identifier_rep(p):
	'''IdentifierRep : IdentifierRep COMMA IDENTIFIER
					 | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])
	else:
		p[0] = []

# -------------------------------------------------------


# ------------------TYPE DECLARATIONS-------------------

def p_type_decl(p):
	'''TypeDecl : TYPE TypeSpec
				| TYPE LPAREN TypeSpecRep RPAREN'''
	p[0] = make_node(p[1])
	if len(p) == 5:
		for i in p[3]:
			make_edge(p[0], i)
	else:
		make_edge(p[0], p[2])

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
	p[0] = make_node(p[2])
	temp = make_node(p[1])
	make_edge(p[0], temp, 'alias')
	make_edge(p[0], p[3])

# -------------------------------------------------------


# -------------------TYPE DEFINITIONS--------------------

def p_type_def(p):
	'''TypeDef : IDENTIFIER Type'''
	p[0] = make_node('typedef')
	temp = make_node(p[1])
	make_edge(p[0], temp)
	make_edge(p[0], p[2])

# -------------------------------------------------------


# ----------------VARIABLE DECLARATIONS------------------

def p_var_decl(p):
	'''VarDecl : VAR VarSpec
			   | VAR LPAREN VarSpecRep RPAREN'''
	p[0] = make_node(p[1])
	if len(p) == 3:
		make_edge(p[0], p[2])
	else:
		for i in p[3]:
			make_edge(p[0], i)

def p_var_spec_rep(p):
	'''VarSpecRep : VarSpecRep VarSpec SEMICOL
				  | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = []

def p_var_spec(p):
	'''VarSpec : IdentifierList Type ExpressionListOpt
			   | IdentifierList EQUAL ExpressionList'''
	p[0] = make_node('VarSpec')
	if p[2] == '=':
		for i in p[1]:
			make_edge(p[0], i, 'id')
		for i in p[3]:
			make_edge(p[0], i, 'exp')
	else:
		for i in p[1]:
			make_edge(p[0], i, 'id')
		make_edge(p[0], p[2], 'type')
		for i in p[3]:
			make_edge(p[0], i, 'exp')

def p_expr_list_opt(p):
	'''ExpressionListOpt : EQUAL ExpressionList
						 | epsilon'''
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = []

# -------------------------------------------------------
	

# ----------------SHORT VARIABLE DECLARATIONS-------------

def p_short_var_decl(p):
	''' ShortVarDecl : IDENTIFIER COLONEQ Expression '''
	p[0] = make_node(p[2])
	temp = make_node(p[1])
	make_edge(p[0], temp, 'id')
	make_edge(p[0], p[3], 'exp')

# -------------------------------------------------------


# ----------------FUNCTION DECLARATIONS------------------

def p_func_decl(p):
	'''FunctionDecl : FUNC FunctionName Function
					| FUNC FunctionName Signature'''
	p[0] = p[3]
	make_edge(p[3], p[2])

def p_func_name(p):
	'''FunctionName : IDENTIFIER'''
	p[0] = make_node(p[1])

def p_func(p):
	'''Function : Signature FunctionBody'''
	p[0] = p[1]
	make_edge(p[1], p[2])

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
	'''BasicLit : INTEGER
				| FLOAT
				| IMAGINARY
				| RUNE
				| STRING'''
	p[0] = make_node(str(p[1]))

def p_operand_name(p):
	'''OperandName : IDENTIFIER'''
	p[0] = make_node(p[1])

# ---------------------------------------------------------


# -----------------COMPOSITE LITERALS----------------------

# def p_comp_lit(p):
# 	'''CompositeLit : LiteralType LiteralValue'''
# 	p[0] = ['CompositeLit', p[1], p[2]]

# def p_lit_type(p):
# 	'''LiteralType : ArrayType
# 				   | ElementType
# 				   | TypeName'''
# 	p[0] = ['LiteralType', p[1]]

# def p_lit_val(p):
# 	'''LiteralValue : LBRACE ElementListOpt RBRACE'''
# 	p[0] = ['LiteralValue', '{', p[2], '}']

# def p_elem_list_comma_opt(p):
# 	'''ElementListOpt : ElementList
# 						   | epsilon'''
# 	p[0] = ['ElementListOpt', p[1]]

# def p_elem_list(p):
# 	'''ElementList : KeyedElement KeyedElementCommaRep'''
# 	p[0] = ['ElementList', p[1], p[2]]

# def p_key_elem_comma_rep(p):
# 	'''KeyedElementCommaRep : KeyedElementCommaRep COMMA KeyedElement
# 							| epsilon'''
# 	if len(p) == 4:
# 		p[0] = ['KeyedElementCommaRep', p[1], ',', p[3]]
# 	else:
# 		p[0] = ['KeyedElementCommaRep', p[1]]

# def p_key_elem(p):
# 	'''KeyedElement : Key COLON Element
# 					| Element'''
# 	if len(p) == 4:
# 		p[0] = ['KeyedElement', p[1], ':', p[3]]
# 	else:
# 		p[0] = ['KeyedElement', p[1]]

# def p_key(p):
# 	'''Key : FieldName
# 		   | Expression
# 		   | LiteralValue'''
# 	p[0] = ['Key', p[1]]

# def p_field_name(p):
# 	'''FieldName : IDENTIFIER'''
# 	p[0] = ['FieldName', p[1]]

# def p_elem(p):
# 	'''Element : Expression
# 			   | LiteralValue'''
# 	p[0] = ['Element', p[1]]

# ---------------------------------------------------------


# -----------------CONVERSIONS-----------------------------

def p_conversion(p):
	'''Conversion : Type LPAREN Expression RPAREN'''
	p[0] = p[1]
	make_edge(p[0], p[3])

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
		p[0] = p[1]
		make_edge(p[0], p[2])

def p_selector(p):
	'''Selector : DOT IDENTIFIER'''
	p[0] = make_node(p[1])
	temp = make_node(p[2])
	make_edge(p[0], temp, 'select')

def p_index(p):
	'''Index : LBRACK Expression RBRACK'''
	p[0] = make_node('[]')
	make_edge(p[0], p[2], 'index')

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
	# p[0] = ['Arguments', '(', p[2], ')']
	p[0] = make_node('args')
	for i in p[2]:
		make_edge(p[0], i)

def p_expr_list_type_opt(p):
	'''ExpressionListTypeOpt : ExpressionList
							 | epsilon'''
	if p[1] == 'epsilon':
		# p[0] = ['ExpressionListTypeOpt', p[1], p[2]]
		p[0] = []
	else:
		# p[0] = ['ExpressionListTypeOpt', p[1]]
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
	p[0].append(p[1])

def p_expr_rep(p):
	'''ExpressionRep : ExpressionRep COMMA Expression
					 | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])
	else:
		p[0] = []

# ---------------------------------------------------------


#----------------------OPERATORS-------------------------

def p_expression(p):
	'''Expression : UnaryExpr
				  | Expression BinaryOp Expression'''
	if len(p) == 4:
		p[0] = make_node(p[2])
		make_edge(p[0], p[1])
		make_edge(p[0], p[3])
	else:
		p[0] = p[1]

### TODO requirement ??
def p_expr_opt(p):
	'''ExpressionOpt : Expression
					 | epsilon'''
	# p[0] = ['ExpressionOpt', p[1]]
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
		p[0] = make_node(str(p[1]))
		make_edge(p[0], p[2])

def p_binary_op(p):
	'''BinaryOp : OROR
				| AMPAMP
				| RelOp
				| AddOp
				| MulOp'''
	p[0] = p[1]

def p_rel_op(p):
	'''RelOp : EQEQ
			 | NOTEQ
			 | LESS
			 | GREAT
			 | LEQ
			 | GEQ'''
	p[0] = p[1]

def p_add_op(p):
	'''AddOp : PLUS
			 | MINUS
			 | OR
			 | CARET'''
	p[0] = p[1]

def p_mul_op(p):
	'''MulOp : TIMES
			 | DIVIDE
			 | MOD
			 | AMPERS
			 | LL
			 | GG
			 | AMPCAR'''
	p[0] = p[1]

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
				 | SwitchStmt
				 | ForStmt '''
	p[0] = p[1]

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
	''' IncDecStmt : Expression PLUSPLUS
					| Expression MINUSMIN '''
	p[0] = p[1]
	temp = make_node(p[2])
	make_edge(p[1], temp)

def p_assignment(p):
	'''Assignment : ExpressionList assign_op ExpressionList'''
	p[0] = make_node(p[2])
	for i in p[1]:
	    make_edge(p[0], i)
	for i in p[3]:
		make_edge(p[0], i)

def p_assign_op(p):
	''' assign_op : AssignOp'''
	p[0] = p[1]

def p_AssignOp(p):
	''' AssignOp : PLUSEQ
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
	p[0] = make_node(p[1])
	make_edge(p[0], p[2], 'condition')
	make_edge(p[0], p[3], 'then')
	if p[4] != -1:
		make_edge(p[0], p[4], 'else')

def p_SimpleStmtOpt(p):
	''' SimpleStmtOpt : SimpleStmt SEMICOL
						| epsilon '''
	if len(p) == 3:
		p[0] = ['SimpleStmtOpt', p[1], ';']
	else :
		p[0] = ['SimpleStmtOpt', p[1]]

def p_else_opt(p):
	''' ElseOpt : ELSE IfStmt
				| ELSE Block
				| epsilon '''
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = -1

# ----------------------------------------------------------------


# ----------- SWITCH STATEMENTS ---------------------------------

def p_switch_statement(p):
	''' SwitchStmt : ExprSwitchStmt
					| TypeSwitchStmt '''
	p[0] = ['SwitchStmt', p[1]]

def p_expr_switch_stmt(p):
	''' ExprSwitchStmt : SWITCH ExpressionOpt LBRACE ExprCaseClauseRep RBRACE'''
	p[0] = ['ExpressionStmt', 'switch', p[2], p[3], '{', p[5], '}']

def p_expr_case_clause_rep(p):
	''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
							| epsilon'''
	if len(p) == 3:
		p[0] = ['ExprCaseClauseRep', p[1], p[2]]
	else:
		p[0] = ['ExprCaseClauseRep', p[1]]

def p_expr_case_clause(p):
	''' ExprCaseClause : ExprSwitchCase COLON StatementList'''
	p[0] = ['ExprCaseClause', p[1], ':', p[3]]

def p_expr_switch_case(p):
	''' ExprSwitchCase : CASE ExpressionList
						| DEFAULT '''
	if len(p) == 3:
		p[0] = ['ExprSwitchCase', 'case', p[2]]
	else:
		p[0] = ['ExprSwitchCase', p[1]]

def p_type_switch_stmt(p):
	''' TypeSwitchStmt : SWITCH SimpleStmtOpt TypeSwitchGuard LBRACE TypeCaseClauseOpt RBRACE'''
	p[0] = ['TypeSwitchStmt', 'switch', p[2], p[3],'{', p[5], '}']

def p_type_switch_guard(p):
	''' TypeSwitchGuard : IdentifierOpt PrimaryExpr DOT LPAREN TYPE RPAREN '''

	p[0] = ['TypeSwitchGuard', p[1], p[2], '.', '(', 'type', ')']

def p_identifier_opt(p):
	''' IdentifierOpt : IDENTIFIER COLONEQ
						| epsilon '''

	if len(p) == 3:
		p[0] = ['IdentifierOpt', p[1], ':=']
	else:
		p[0] = ['IdentifierOpt', p[1]]

def p_type_case_clause_opt(p):
	''' TypeCaseClauseOpt : TypeCaseClauseOpt TypeCaseClause
							| epsilon '''
	if len(p) == 3:
		p[0] = ['TypeCaseClauseOpt', p[1], p[2]]
	else:
		p[0] = ['TypeCaseClauseOpt', p[1]]

def p_type_case_clause(p):
	''' TypeCaseClause : TypeSwitchCase COLON StatementList'''
	p[0] = ['TypeCaseClause', p[1], ':', p[3]]

def p_type_switch_case(p):
	''' TypeSwitchCase : CASE TypeList
						| DEFAULT '''
	if len(p) == 3:
		p[0] = ['TypeSwitchCase', p[1], p[2]]
	else:
		p[0] = ['TypeSwitchCase', p[1]]

def p_type_list(p):
	''' TypeList : Type TypeRep'''
	p[0] = ['TypeList', p[1], p[2]]

def p_type_rep(p):
	''' TypeRep : TypeRep COMMA Type
				| epsilon '''
	if len(p) == 4:
		p[0] = ['TypeRep', p[1], ',', p[3]]
	else:
		p[0] = ['TypeRep', p[1]]

# -----------------------------------------------------------


# --------- FOR STATEMENTS---------------

def p_for(p):
	'''ForStmt : FOR ConditionBlockOpt Block'''
	p[0] = make_node(p[1])
	make_edge(p[0], p[3])
	if p[2] != -1:
		make_edge(p[0], p[2])

def p_conditionblockopt(p):
	'''ConditionBlockOpt : epsilon
				| Condition
				| ForClause'''
				# | RangeClause'''
	if p[1] == 'epsilon':
		p[0] = -1
	else:
		p[0] = p[1]

def p_condition(p):
	'''Condition : Expression '''
	p[0] = p[1]

def p_forclause(p):
	'''ForClause : SimpleStmt SEMICOL ConditionOpt SEMICOL SimpleStmt'''
	p[0] = make_node('ForClause')
	make_edge(p[0], p[1])
	if p[3] != -1:
		make_edge(p[0], p[3])
	make_edge(p[0], p[5])

def p_conditionopt(p):
	'''ConditionOpt : epsilon
			| Condition '''
	if p[1] == 'epsilon':
		p[0] = -1
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
	p[0] = make_node(p[1])
	for i in p[2]:
		make_edge(p[0], i)

def p_expressionlist_pure_opt(p):
	'''ExpressionListPureOpt : ExpressionList
				| epsilon'''
	if p[0] != 'epsilon':
		p[0] = p[1]
	else:
		p[0] = []

def p_break(p):
	'''BreakStmt : BREAK LabelOpt'''
	p[0] = make_node(p[1])
	if p[2] != -1:
		make_edge(p[0], p[2])

def p_continue(p):
	'''ContinueStmt : CONTINUE LabelOpt'''
	p[0] = make_node(p[1])
	if p[2] != -1:
		make_edge(p[0], p[2])

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
	p[0] = make_node('Source')
	make_edge(p[0], p[1])
	for i in p[3]:
		make_edge(p[0], i)
	for i in p[4]:
		make_edge(p[0], i)

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
		p[0].append(p[2])
	else:
		p[0] = []
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

with open(infile,'r') as f:
	input_str = f.read()
t = parser.parse(input_str)

pp.pprint(t)
dot.render(outfile)