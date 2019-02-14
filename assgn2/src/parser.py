import ply.yacc as yacc
import mylexer            # Import lexer information
tokens = mylexer.tokens   # Need token list

from graphviz import Digraph 

nodecount = 0
dot = Digraph()

def makenode(label):
	global nodecount
	dot.node(str(nodecount), label)
	nodecount += 1
	return nodecount - 1

def makeedge(node1, node2):
	dot.edge(str(node1), str(node2))


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
	p[0] = ["start", p[1]]

# def p_start(p):
# 	'''start : Type '''
# 	p[0] = ["start", p[1]]

#----------------------------------------------------------------------------------#



#-------------------------------Types------------------------------#

def p_type(p):
	'''Type : TypeName 
			| TypeLit 
			| LPAREN Type RPAREN'''
	p[0] = ["start", p[1]]
	if (len(p) == 4):
		p[0] = ["Type", "(", p[2], ")"]
	else:
		p[0] = ["Type", p[1]]

def p_type_name(p):
	'''TypeName : TYPE
				| QualifiedIdent'''
	# '''TypeName : identifier
	# 			| QualifiedIdent'''
	# TODO
	p[0] = ["TypeName", p[1]]

def p_type_lit(p):
	'''TypeLit : ArrayType
			   | StructType
			   | PointerType
			   | FunctionType'''
	p[0] = ["TypeLit", p[1]]
#TODO#############           
def p_type_opt(p):
	'''TypeOpt : Type
			   | epsilon'''
	p[0] = ["TypeOpt", p[1]]

#----------------------------------------------------------------------------------#


#-------------------------------ArrayType------------------------------#

def p_array_type(p):
	'''ArrayType : LBRACK ArrayLength RBRACK ElementType'''
	p[0] = ["ArrayType", "[", p[2], "]", p[4]]

def p_array_length(p):
	''' ArrayLength : Expression '''
	p[0] = ["ArrayLength", p[1]]

def p_element_type(p):
	''' ElementType : Type '''
	p[0] = ["ElementType", p[1]]

#----------------------------------------------------------------------------------#

#-------------------------------StructType------------------------------#

def p_struct_type(p):
	'''StructType : STRUCT LBRACE FieldDeclRep RBRACE'''
	p[0] = ["StructType", "struct", "{", p[3], "}"]
	print(p[0])

# FeildDeclRep to include multiple rows in struct fields

def p_field_decl_rep(p):
  	''' FieldDeclRep : FieldDeclRep FieldDecl SEMICOL
				  | epsilon'''
	# print (p[1])
	if len(p) == 4:
		p[0] = ["FieldDeclRep", p[1], p[2], ";"]
	else:
		p[0] = ["FieldDeclRep", p[1]]

def p_field_decl(p):
	''' FieldDecl : IdentifierList Type TagOpt'''
	#########????????????Embedded Field TODO
	p[0] = ["FieldDecl", p[1], p[2], p[3]]

def p_tag_opt(p):
  	''' TagOpt : Tag
			 | epsilon '''
	p[0] = ["TagOpt", p[1]]

def p_tag(p):
	''' Tag : STRING '''
	p[0] = ["Tag", p[1]]
#----------------------------------------------------------------------------------#

#-------------------------------PointerType------------------------------#

def p_pointer_type(p):
	'''PointerType : TIMES BaseType'''
	# '''PointerType : STAR BaseType'''
	#########TODO times or star
	p[0] = ["PointerType", "*", p[2]]

def p_base_type(p):
	'''BaseType : Type'''
	p[0] = ["BaseType", p[1]]

#----------------------------------------------------------------------------------#

#-------------------------------FunctionType------------------------------#

def p_function_type(p):
	'''FunctionType : FUNC Signature'''
	p[0] = ["FunctionType", "func", p[2]]

def p_signature(p):
	'''Signature : Parameters ResultOpt'''
	p[0] = ["Signature", p[1], p[2]]

def p_result_opt(p):
	'''ResultOpt : Result
				 | epsilon'''
	p[0] = ["ResultOpt", p[1]]

def p_result(p):
	'''Result : Parameters
			  | Type'''
	p[0] = ["Result", p[1]]

def p_parameters(p):
	'''Parameters : LPAREN ParameterListOpt RPAREN'''
	p[0] = ["Parameters", "(", p[2], ")"]

def p_parameter_list_opt(p):
	'''ParameterListOpt : ParametersList
						| epsilon'''
	p[0] = ["ParameterListOpt", p[1]]

def p_parameter_list(p):
	'''ParametersList : Type
					  | IdentifierList Type
					  | ParameterDeclCommaRep'''
	if len(p) == 3:
		p[0] = ["ParametersList", p[1], p[2]]
	else:
		p[0] = ["ParametersList", p[1]]

######### TODO possible conflicts?????
def p_parameter_decl_comma_rep(p):
	'''ParameterDeclCommaRep : ParameterDeclCommaRep COMMA ParameterDecl
							 | ParameterDecl COMMA ParameterDecl'''
	p[0] = ["ParameterDeclCommaRep", p[1], ",", p[3]]

def p_parameter_decl(p):
	'''ParameterDecl : IdentifierList Type
					 | Type'''
	if len(p) == 3:
		p[0] = ["ParameterDecl", p[1], p[2]]
	else:
		p[0] = ["ParameterDecl", p[1]]

#----------------------------------------------------------------------------------#

#-----------------------Blocks---------------------------

def p_block(p):
	'''Block : LBRACE StatementList RBRACE'''
	# p[0] = ["Blocks", "{" , p[2], "}"]
	p[0] = makenode("Block")
	for i in p[2]:
		makeedge(p[0], i)

def p_statement_list(p):
	'''StatementList : StatementRep'''
	p[0] = p[1]
	# p[0] = ["StatementList", p[1]]


#########TODO different!!!
def p_statement_rep(p):
	'''StatementRep : StatementRep Statement SEMICOL
					| epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[2])
		# p[0] =  str(p[1]) + str(p[2]) + ';'
	else:
		p[0] = []
		# p[0] = "";
		# p[0] = ["StatementRep", p[1]]

# 
# -------------------------------------------------------

# ------------------DECLARATIONS and SCOPE------------------------
def p_decl(p):
	'''Declaration : ConstDecl
					| TypeDecl
					| VarDecl'''
	p[0] = ["Declaration", p[1]]

def p_toplevel_decl(p):
	'''TopLevelDecl : Declaration
					| FunctionDecl'''
		##TODO?????Method Declaration
	p[0] = ["TopLevelDecl", p[1]]
# -------------------------------------------------------

# ------------------CONSTANT DECLARATIONS----------------
def p_const_decl(p):
	'''ConstDecl : CONST ConstSpec
				 | CONST LPAREN ConstSpecRep RPAREN'''
	if len(p) == 3:
		p[0] = ["ConstDecl", "const", p[2]]
	else:
		p[0] = ["ConstDecl", "const", '(', p[3], ')']


##### TODO Can be changed!!
# def p_const_spec_rep(p):
#     '''ConstSpecRep : ConstSpecRep ConstSpec SEMICOL
#                     | epsilon'''
#     if len(p) == 4:
#         p[0] = ["ConstSpecRep", p[1], p[2], ';']
#     else:
#         p[0] = ["ConstSpecRep", p[1]]
def p_const_spec_rep(p):
	'''ConstSpecRep : ConstSpecRep ConstSpec SEMICOL
					| epsilon'''
	if len(p) == 4:
		p[0] = ["ConstSpecRep", p[1], p[2], ';']
	else:
		p[0] = ["ConstSpecRep", p[1]]

def p_const_spec(p):
	'''ConstSpec : IdentifierList TypeExprListOpt'''
	p[0] = ["ConstSpec", p[1], p[2]]

def p_type_expr_list(p):
	'''TypeExprListOpt : TypeOpt EQUAL ExpressionList
					   | epsilon'''
	if len(p) == 4:
		p[0] = ["TypeExprListOpt", p[1], "=", p[3]]
	else:
		p[0] = ["TypeExprListOpt", p[1]]

def p_identifier_list(p):
	'''IdentifierList : IDENTIFIER IdentifierRep'''
	p[0] = ["IdentifierList", p[1], p[2]]

def p_identifier_rep(p):
	'''IdentifierRep : IdentifierRep COMMA IDENTIFIER
					 | epsilon'''
	if len(p) == 4:
		p[0] = ["IdentifierRep", p[1], ",", p[3]]
	else:
		p[0] = ["IdentifierRep", p[1]]

# def p_expr_list(p):
#     '''ExpressionList : Expression ExpressionRep'''
#     p[0] = ["ExpressionList", p[1], p[2]]

# def p_expr_rep(p):
#     '''ExpressionRep : ExpressionRep COMMA Expression
#                      | epsilon'''
#     if len(p) == 4:
#         p[0] = ["ExpressionRep", p[1], ',', p[3]]
#     else:
#         p[0] = ["ExpressionRep", p[1]]

	###?????????How to guarantee same number of idetifiers and expressions TODO
# -------------------------------------------------------

# ------------------TYPE DECLARATIONS-------------------
def p_type_decl(p):
	'''TypeDecl : TYPE TypeSpec
				| TYPE LPAREN TypeSpecRep RPAREN'''
	if len(p) == 5:
		p[0] = ["TypeDecl", "type", "(", p[3], ")"]
	else:
		p[0] = ["TypeDecl", "type", p[2]]

def p_type_spec_rep(p):
	'''TypeSpecRep : TypeSpecRep TypeSpec SEMICOL
				   | epsilon'''
	if len(p) == 4:
		p[0] = ["TypeSpecRep", p[1], p[2], ";"]
	else:
		p[0] = ["TypeSpecRep", p[1]]

def p_type_spec(p):
	'''TypeSpec : AliasDecl
				| TypeDef'''
	p[0] = ["TypeSpec", p[1]]

def p_alias_decl(p):
	'''AliasDecl : IDENTIFIER EQUAL Type'''
	p[0] = ["AliasDecl", p[1], '=', p[3]]
# -------------------------------------------------------


# -------------------TYPE DEFINITIONS--------------------
def p_type_def(p):
	'''TypeDef : IDENTIFIER Type'''
	p[0] = ["TypeDef", p[1], p[2]]
# -------------------------------------------------------


# ----------------VARIABLE DECLARATIONS------------------
def p_var_decl(p):
	'''VarDecl : VAR VarSpec
			   | VAR LPAREN VarSpecRep RPAREN'''
	if len(p) == 3:
		p[0] = ["VarDecl", "var", p[2]]
	else:
		p[0] = ["VarDecl", "var", "(", p[3], ")"]

def p_var_spec_rep(p):
	'''VarSpecRep : VarSpecRep VarSpec SEMICOL
				  | epsilon'''
	if len(p) == 4:
		p[0] = ["VarSpecRep", p[1], p[2], ";"]
	else:
		p[0] = ["VarSpecRep", p[1]]

def p_var_spec(p):
	'''VarSpec : IdentifierList Type ExpressionListOpt
			   | IdentifierList EQUAL ExpressionList'''
	if p[2] == '=':
		p[0] = ["VarSpec", p[1], "=", p[3]]
	else:
		p[0] = ["VarSpec", p[1], p[2], p[3]]

def p_expr_list_opt(p):
	'''ExpressionListOpt : EQUAL ExpressionList
						 | epsilon'''
	if len(p) == 3:
		p[0] = ["ExpressionListOpt", "=", p[2]]
	else:
		p[0] = ["ExpressionListOpt", p[1]]
# -------------------------------------------------------

	
# ----------------SHORT VARIABLE DECLARATIONS-------------
def p_short_var_decl(p):
  ''' ShortVarDecl : IDENTIFIER COLONEQ Expression '''
  p[0] = ["ShortVarDecl", p[1], ":=", p[3]]
# -------------------------------------------------------

# ----------------FUNCTION DECLARATIONS------------------
def p_func_decl(p):
	'''FunctionDecl : FUNC FunctionName Function
					| FUNC FunctionName Signature'''
	p[0] = ["FunctionDecl", "func", p[2], p[3]]

def p_func_name(p):
	'''FunctionName : IDENTIFIER'''
	p[0] = ["FunctionName", p[1]]

def p_func(p):
	'''Function : Signature FunctionBody'''
	p[0] = ["Function", p[1], p[2]]

def p_func_body(p):
	'''FunctionBody : Block'''
	p[0] = ["FunctionBody", p[1]]
# -------------------------------------------------------

# -------------------QUALIFIED IDENTIFIER----------------
def p_quali_ident(p):
	'''QualifiedIdent : IDENTIFIER DOT TypeName'''
	p[0] = ["QualifiedIdent", p[1], ".", p[3]]
# -------------------------------------------------------

def p_empty(p):
	'''epsilon : '''
	p[0] = "epsilon"

# ----------------------OPERAND----------------------------
def p_operand(p):
	'''Operand : Literal
			   | OperandName
			   | LPAREN Expression RPAREN'''
	if len(p) == 2:
		p[0] = p[1]
		# p[0] = ["Operand", p[1]]
	else:
		# p[0] = ["Operand", "(", p[2], ")"]
		p[0] = p[2]

def p_literal(p):
	'''Literal : BasicLit'''
			   #| CompositeLit'''
	# p[0] = ["Literal", p[1]]
	p[0] = p[1]

def p_basic_lit(p):
	'''BasicLit : INTEGER
				| FLOAT
				| IMAGINARY
				| RUNE
				| STRING'''
	# p[0] = ["BasicLit",str(p[1])]
	# p[0] = str(p[1])
	p[0] = makenode(str(p[1]))

def p_operand_name(p):
	'''OperandName : IDENTIFIER'''
	p[0] = makenode(str(p[1]))
	# p[0] = ["OperandName", p[1]]
# ---------------------------------------------------------

# -----------------COMPOSITE LITERALS----------------------
def p_comp_lit(p):
	'''CompositeLit : LiteralType LiteralValue'''
	p[0] = ["CompositeLit", p[1], p[2]]

def p_lit_type(p):
	'''LiteralType : ArrayType
				   | ElementType
				   | TypeName'''
	p[0] = ["LiteralType", p[1]]

def p_lit_val(p):
	'''LiteralValue : LBRACE ElementListOpt RBRACE'''
	p[0] = ["LiteralValue", "{", p[2], "}"]

def p_elem_list_comma_opt(p):
	'''ElementListOpt : ElementList
						   | epsilon'''
	p[0] = ["ElementListOpt", p[1]]

def p_elem_list(p):
	'''ElementList : KeyedElement KeyedElementCommaRep'''
	p[0] = ["ElementList", p[1], p[2]]

def p_key_elem_comma_rep(p):
	'''KeyedElementCommaRep : KeyedElementCommaRep COMMA KeyedElement
							| epsilon'''
	if len(p) == 4:
		p[0] = ["KeyedElementCommaRep", p[1], ",", p[3]]
	else:
		p[0] = ["KeyedElementCommaRep", p[1]]

def p_key_elem(p):
	'''KeyedElement : Key COLON Element
					| Element'''
	if len(p) == 4:
		p[0] = ["KeyedElement", p[1], ":", p[3]]
	else:
		p[0] = ["KeyedElement", p[1]]

def p_key(p):
	'''Key : FieldName
		   | Expression
		   | LiteralValue'''
	p[0] = ["Key", p[1]]

def p_field_name(p):
	'''FieldName : IDENTIFIER'''
	p[0] = ["FieldName", p[1]]

def p_elem(p):
	'''Element : Expression
			   | LiteralValue'''
	p[0] = ["Element", p[1]]
# ---------------------------------------------------------


# -----------------CONVERSIONS-----------------------------
def p_conversion(p):
	'''Conversion : Type LPAREN Expression RPAREN'''
	p[0] = ["Conversion", p[1],  "(", p[3], ")"]
# ---------------------------------------------------------


# ------------------PRIMARY EXPRESSIONS--------------------
def p_prim_expr(p):
	'''PrimaryExpr : Operand
				   | Conversion
				   | PrimaryExpr Selector
				   | PrimaryExpr Index
				   | PrimaryExpr Slice
				   | PrimaryExpr TypeAssertion
				   | PrimaryExpr Arguments'''
	if len(p) == 2:
		p[0] = p[1]
		# p[0] = ["PrimaryExpr", p[1]]
	else:
		p[0] = ["PrimaryExpr", p[1], p[2]]

def p_selector(p):
	'''Selector : DOT IDENTIFIER'''
	p[0] = ["Selector", ".", p[2]]

def p_index(p):
	'''Index : LBRACK Expression RBRACK'''
	p[0] = ["Index", "[", p[2], "]"]

def p_slice(p):
	'''Slice : LBRACK ExpressionOpt COLON ExpressionOpt RBRACK
			 | LBRACK ExpressionOpt COLON Expression COLON Expression RBRACK'''
			 ###### TODO Optional
	if len(p) == 6:
		p[0] = ["Slice", "[", p[2], ":", p[4], "]"]
	else:
		p[0] = ["Slice", "[", p[2], ":", p[4], ":", p[6], "]"]

def p_type_assert(p):
	'''TypeAssertion : DOT LPAREN Type RPAREN'''
	p[0] = ["TypeAssertion", ".", "(", p[3], ")"]

def p_argument(p):
	'''Arguments : LPAREN ExpressionListTypeOpt RPAREN'''
		#####?????????
	p[0] = ["Arguments", "(", p[2], ")"]

def p_expr_list_type_opt(p):
	'''ExpressionListTypeOpt : ExpressionList
							 | epsilon'''
	if len(p) == 3:
		p[0] = ["ExpressionListTypeOpt", p[1], p[2]]
	### TODO 
	else:
		p[0] = ["ExpressionListTypeOpt", p[1]]

#def p_comma_opt(p):
#    '''CommaOpt : COMMA
#                | epsilon'''
#    if p[1] == ",":
#        p[0] = ["CommaOpt", ","]
#    else:
#        p[0] = ["CommaOpt", p[1]]

def p_expr_list_comma_opt(p):
	'''ExpressionListCommaOpt : COMMA ExpressionList
							  | epsilon'''
	if len(p) == 3:
		p[0] = ["ExpressionListCommaOpt", ",", p[2]]
	else:
		p[0] = ["ExpressionListCommaOpt", p[1]]

def p_expr_list(p):
	'''ExpressionList : Expression ExpressionRep'''
	p[0] = p[2]
	p[0].append(p[1])
	# p[0] = ["ExpressionList", p[1], p[2]]

def p_expr_rep(p):
	'''ExpressionRep : ExpressionRep COMMA Expression
					 | epsilon'''
	if len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])
		#TODO   repetition
		# p[0] = str(p[1]) + ',' + str(p[3])
	else:
		p[0] = []
		# if (p[1] != "epsilon"):
		#     p[0] = p[1]
		# else:
		#     p[0] = ""
# ---------------------------------------------------------


#----------------------OPERATORS-------------------------
def p_expression(p):
	'''Expression : UnaryExpr
				  | Expression BinaryOp Expression'''
	if len(p) == 4:
		p[0] = makenode(p[2])
		makeedge(p[0], p[1])
		makeedge(p[0], p[3])

		# p[0] = ["BinaryOp", p[1], p[2], p[3]]
		# p[0] = ["Expression", p[1], p[2], p[3]]
		# p[0] = makenode(p[2])
		# p[0] -> child = p[1], p[2];
	else:
		p[0] = p[1]
		# p[0] = makenode(p[1]);
		# p[0] = p[1]
		# p[0] = makenode(p[1])
		# p[0] = ["Expression", p[1]]


##########TODO check requirement
def p_expr_opt(p):
	'''ExpressionOpt : Expression
					 | epsilon'''
	p[0] = ["ExpressionOpt", p[1]]

def p_unary_expr(p):
	'''UnaryExpr : PrimaryExpr
				 | UnaryOp UnaryExpr'''
				#  | NOT UnaryExpr'''
	if len(p) == 2:
		p[0] = p[1]
		# p[0] = ["UnaryExpr", p[1]]
	# elif p[1] == "!": # TODO !! not requried seperately
	# 	p[0] = ["UnaryExpr", "!", p[2]]
	else:
		p[0] = makenode(str(p[1]))
		makeedge(p[0], p[2])
		# p[0] = ["UnaryExpr", p[1], p[2]]

def p_binary_op(p):
	'''BinaryOp : OROR
				| AMPAMP
				| RelOp
				| AddOp
				| MulOp'''
	# p[0] = ["BinaryOp", p[1]]
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
	# p[0] = ["AddOp", p[1]]

def p_mul_op(p):
	'''MulOp : TIMES
			 | DIVIDE
			 | MOD
			 | AMPERS
			 | LL
			 | GG
			 | AMPCAR'''
	p[0] = p[1]
	# p[0] = ["MulOp", p[1]]

def p_unary_op(p):
	'''UnaryOp : PLUS
			   | MINUS
			   | TIMES
			   | AMPERS
			   | NOT '''
	p[0] = p[1]
	
# -------------------------------------------------------

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
	# p[0] = ["Statement", p[1]]
	p[0] = p[1]

def p_simple_stmt(p):
	'''SimpleStmt : epsilon
				  | ExpressionStmt
				  | IncDecStmt
				  | Assignment
				  | ShortVarDecl '''
	p[0] = p[1]


def p_labeled_statements(p):
	''' LabeledStmt : Label COLON Statement '''
	p[0] = ["LabeledStmt", p[1], ":", p[3]]

def p_label(p):
	''' Label : IDENTIFIER '''
	p[0] = ["Label", p[1]]


def p_expression_stmt(p):
	''' ExpressionStmt : Expression '''
	p[0] = ["ExpressionStmt", p[1]]

def p_inc_dec(p):
	''' IncDecStmt : Expression PLUSPLUS
					| Expression MINUSMIN '''
	if p[2] == '++':
		p[0] = ["IncDecStmt", p[1], "++"]
	else:
		p[0] = ["IncDecStmt", p[1], "--"]


def p_assignment(p):
	'''Assignment : ExpressionList assign_op ExpressionList'''
	p[0] = makenode(p[2])
	# print p[1]
	for i in p[1]:
	    makeedge(p[0], i)
	for i in p[3]:
		makeedge(p[0], i)

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


def p_if_statement(p):
	''' IfStmt : IF Expression Block ElseOpt '''
	p[0] = ["IfStmt", "if", p[2], p[3], p[4]]

def p_SimpleStmtOpt(p):
	''' SimpleStmtOpt : SimpleStmt SEMICOL
						| epsilon '''
	if len(p) == 3:
		p[0] = ["SimpleStmtOpt", p[1], ";"]
	else :
		p[0] = ["SimpleStmtOpt", p[1]]

def p_else_opt(p):
	''' ElseOpt : ELSE IfStmt
				| ELSE Block
				| epsilon '''
	if len(p) == 3:
		p[0] = ["ElseOpt", "else", p[2]]
	else:
		p[0] = ["ElseOpt", p[1]]

# ----------------------------------------------------------------



# ----------- SWITCH STATEMENTS ---------------------------------

def p_switch_statement(p):
	''' SwitchStmt : ExprSwitchStmt
					| TypeSwitchStmt '''
	p[0] = ["SwitchStmt", p[1]]


def p_expr_switch_stmt(p):
	''' ExprSwitchStmt : SWITCH ExpressionOpt LBRACE ExprCaseClauseRep RBRACE'''
	p[0] = ["ExpressionStmt", "switch", p[2], p[3], "{", p[5], "}"]

def p_expr_case_clause_rep(p):
	''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
							| epsilon'''
	if len(p) == 3:
		p[0] = ["ExprCaseClauseRep", p[1], p[2]]
	else:
		p[0] = ["ExprCaseClauseRep", p[1]]

def p_expr_case_clause(p):
	''' ExprCaseClause : ExprSwitchCase COLON StatementList'''
	p[0] = ["ExprCaseClause", p[1], ":", p[3]]

def p_expr_switch_case(p):
	''' ExprSwitchCase : CASE ExpressionList
						| DEFAULT '''
	if len(p) == 3:
		p[0] = ["ExprSwitchCase", "case", p[2]]
	else:
		p[0] = ["ExprSwitchCase", p[1]]

def p_type_switch_stmt(p):
	''' TypeSwitchStmt : SWITCH SimpleStmtOpt TypeSwitchGuard LBRACE TypeCaseClauseOpt RBRACE'''
	p[0] = ["TypeSwitchStmt", "switch", p[2], p[3],"{", p[5], "}"]


def p_type_switch_guard(p):
	''' TypeSwitchGuard : IdentifierOpt PrimaryExpr DOT LPAREN TYPE RPAREN '''

	p[0] = ["TypeSwitchGuard", p[1], p[2], ".", "(", "type", ")"]

def p_identifier_opt(p):
	''' IdentifierOpt : IDENTIFIER COLONEQ
						| epsilon '''

	if len(p) == 3:
		p[0] = ["IdentifierOpt", p[1], ":="]
	else:
		p[0] = ["IdentifierOpt", p[1]]

def p_type_case_clause_opt(p):
	''' TypeCaseClauseOpt : TypeCaseClauseOpt TypeCaseClause
							| epsilon '''
	if len(p) == 3:
		p[0] = ["TypeCaseClauseOpt", p[1], p[2]]
	else:
		p[0] = ["TypeCaseClauseOpt", p[1]]

def p_type_case_clause(p):
	''' TypeCaseClause : TypeSwitchCase COLON StatementList'''
	p[0] = ["TypeCaseClause", p[1], ":", p[3]]


def p_type_switch_case(p):
	''' TypeSwitchCase : CASE TypeList
						| DEFAULT '''
	if len(p) == 3:
		p[0] = ["TypeSwitchCase", p[1], p[2]]
	else:
		p[0] = ["TypeSwitchCase", p[1]]

def p_type_list(p):
	''' TypeList : Type TypeRep'''
	p[0] = ["TypeList", p[1], p[2]]

def p_type_rep(p):
	''' TypeRep : TypeRep COMMA Type
				| epsilon '''
	if len(p) == 4:
		p[0] = ["TypeRep", p[1], ",", p[3]]
	else:
		p[0] = ["TypeRep", p[1]]

# -----------------------------------------------------------


# --------- FOR STATEMENTS---------------

def p_for(p):
	'''ForStmt : FOR ConditionBlockOpt Block'''
	p[0] = ["ForStmt", "for", p[2], p[3]]

def p_conditionblockopt(p):
	'''ConditionBlockOpt : epsilon
				| Condition
				| ForClause
				| RangeClause'''
	p[0] = ["ConditionBlockOpt", p[1]]

def p_condition(p):
	'''Condition : Expression '''
	p[0] = ["Condition", p[1]]

def p_forclause(p):
	'''ForClause : SimpleStmt SEMICOL ConditionOpt SEMICOL SimpleStmt'''
	p[0] = ["ForClause", p[1], ";", p[3], ";", p[5]]

# def p_initstmtopt(p):
#   '''InitStmtOpt : epsilon
#            | InitStmt '''
#   p[0] = ["InitStmtOpt", p[1]]

# def p_init_stmt(p):
#   ''' InitStmt : SimpleStmt'''
#   p[0] = ["InitStmt", p[1]]


def p_conditionopt(p):
	'''ConditionOpt : epsilon
			| Condition '''
	p[0] = ["ConditionOpt", p[1]]

# def p_poststmtopt(p):
#   '''PostStmtOpt : epsilon
#            | PostStmt '''
#   p[0] = ["PostStmtOpt", p[1]]

# def p_post_stmt(p):
#   ''' PostStmt : SimpleStmt '''
#   # p[0] = ["PostStmt", p[1]]

def p_rageclause(p):
	'''RangeClause : ExpressionIdentListOpt RANGE Expression'''
	p[0] = ["RangeClause", p[1], "range", p[3]]

def p_expression_ident_listopt(p):
	'''ExpressionIdentListOpt : epsilon
				| ExpressionIdentifier'''
	p[0] = ["ExpressionIdentListOpt", p[1]]

def p_expressionidentifier(p):
	'''ExpressionIdentifier : ExpressionList EQUAL'''
	if p[2] == "=":
		p[0] = ["ExpressionIdentifier", p[1], "="]
	else:
		####TODO how????????? 
		p[0] = ["ExpressionIdentifier", p[1], ":="]

def p_return(p):
	'''ReturnStmt : RETURN ExpressionListPureOpt'''
	p[0] = ["ReturnStmt", "return", p[2]]

def p_expressionlist_pure_opt(p):
	'''ExpressionListPureOpt : ExpressionList
				| epsilon'''
	p[0] = ["ExpressionListPureOpt", p[1]]

def p_break(p):
	'''BreakStmt : BREAK LabelOpt'''
	p[0] = ["BreakStmt", "break", p[2]]

def p_continue(p):
	'''ContinueStmt : CONTINUE LabelOpt'''
	p[0] = ["ContinueStmt", "continue", p[2]]

def p_labelopt(p):
	'''LabelOpt : Label
			| epsilon '''
	p[0] = ["LabelOpt", p[1]]

def p_goto(p):
	'''GotoStmt : GOTO Label '''
	p[0] = ["GotoStmt", "goto", p[2]]
# -----------------------------------------------------------

# ----------------  SOURCE FILE --------------------------------
def p_source_file(p):
	'''Source : PackageClause SEMICOL ImportDeclRep TopLevelDeclRep'''
	p[0] = ["Source", p[1], ";", p[3], p[4]]

def p_import_decl_rep(p):
	'''ImportDeclRep : epsilon
			| ImportDeclRep ImportDecl SEMICOL'''
	if len(p) == 4:
		p[0] = ["ImportDeclRep", p[1], p[2], ";"]
	else:
		p[0] = ["ImportDeclRep", p[1]]

def p_toplevel_decl_rep(p):
	'''TopLevelDeclRep : TopLevelDeclRep TopLevelDecl SEMICOL
						| epsilon'''
	if len(p) == 4:
		p[0] = ["TopLevelDeclRep", p[1], p[2], ";"]
	else:
		p[0] = ["TopLevelDeclRep", p[1]]
# --------------------------------------------------------


# ---------- PACKAGE CLAUSE --------------------
def p_package_clause(p):
	'''PackageClause : PACKAGE PackageName'''
	p[0] = ["PackageClause", "package", p[2]]


def p_package_name(p):
	'''PackageName : IDENTIFIER'''
	p[0] = ["PackageName", p[1]]
# -----------------------------------------------

# --------- IMPORT DECLARATIONS ---------------
def p_import_decl(p):
	'''ImportDecl : IMPORT ImportSpec
			| IMPORT LPAREN ImportSpecRep RPAREN '''
	if len(p) == 3:
		p[0] = ["ImportDecl", "import", p[2]]
	else:
		p[0] = ["ImportDecl", "import", "(", p[3], ")"]

def p_import_spec_rep(p):
	''' ImportSpecRep : ImportSpecRep ImportSpec SEMICOL
				| epsilon '''
	if len(p) == 4:
		p[0] = ["ImportSpecRep", p[1], p[2], ";"]
	else:
		p[0] = ["ImportSpecRep", p[1]]

def p_import_spec(p):
	''' ImportSpec : PackageNameDotOpt ImportPath '''
	p[0] = ["ImportSpec", p[1], p[2]]

def p_package_name_dot_opt(p):
	''' PackageNameDotOpt : DOT
							| PackageName
							| epsilon'''
	if p[1]== '.':
		p[0] = ["PackageNameDotOpt", "."]
	else:
		p[0] = ["PackageNameDotOpt", p[1]]

def p_import_path(p):
	''' ImportPath : STRING '''
	p[0] = ["ImportPath", p[1]]
# -------------------------------------------------------ParametersParameters


# def p_error(p):
#   print("Syntax error in input!")
#   print(p)



parser = yacc.yacc()            # Build the parser

with open('inp','r') as f:
	input_str = f.read()

t = parser.parse(input_str)

import pprint as pp

pp.pprint(t)
dot.render('digraph.dot')