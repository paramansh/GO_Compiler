basic_types = ['int', 'float', 'char', 'string', 'rune']
def add_type(name, ttype):
	basic_types.append({name:ttype})

class Node:
	def __init__(self):
		self.code = []
		self.place = ""
		self.type = "" # this denotes type variable int/float etc
		self.idlist = []
		self.exprlist = []
		self.expr = Expr()
		self.next = ['not initialised next label']
		self.begin = ['begin not initialised']
		self.extra = {}
		self.forclause = ForClause()

	def __str__(self):
		print "code:", self.code
		print "place:", self.place 
		print "type:", self.type # denotes type of expression
		print "idlist:", self.idlist
		print "exprlist:"
		for i in self.exprlist:
			print i.__dict__
		print "expr:", self.expr
		print "extra:", self.extra
		return ""

class Expr:
	def __init__(self):
		self.value = "None"
		self.type = "None"
		self.is_constant = False # whether is expression an constant eg: 4
		# self.is_true = True # for bool expressions
		self.true_label = ['not initialise true label'] #list so as store pointer
		self.false_label = ['not initialised false label']
		
	def __str__(self):
		if self is None:
			return ""
		return str(self.__dict__)
		# print "value:", self.value 
		# print "type:", self.type

class ForClause:
	def __init__(self):
		self.isClause = False
		self.initialise = []
		self.condition = []
		self.update = []

	def __str__(self):
		if self is None:
			return ""
		return str(self.__dict__)



class SymbolTable:
	def __init__(self, parent):
		self.table = {}
		self.parent = parent
		self.types = {}
		self.label = 0

	#?? symbol table identifying name??
	# checks if name exists in the symbol table
	def lookup(self, name):
		if name in self.table:
			return True
		else:
			return False

	def insert(self, name, idtype):
		if self.lookup(name):
			print "error: can't update type"
		else:
			self.table[name] = {}
			self.table[name]['type'] = idtype 

	def setArgs(self, name, attribute, value):
		if self.lookup(name):
			(self.table)[name][attribute] = value
		else:
			print "error: entry does not exist"

	def getEntry(self, name):
		if (self.lookup)(name):
			return (self.table)[name]
		else:
			return None
			# return err TODO ????????
	
	def getAllEntries(self):
		if self.parent:
			return self.table, self.label, self.types, self.parent.label
		else:
			return self.table, self.label, self.types, None
	