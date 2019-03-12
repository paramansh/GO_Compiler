class Node:
	def __init__(self):
		self.code = []
		self.type = ""
		self.idlist = []
		self.exprlist = []
		self.expr = Expr()
	def __str__(self):
		print "code:", self.code
		print "type:", self.type
		print "idlist:", self.idlist
		print "exprlist:"
		for i in self.exprlist:
			print i.__dict__
		print "expr:", self.expr.__dict__

class Expr:
	def __init__(self):
		self.value = "None"
		self.type = "None"
	def __str__(self):
		return str(self.__dict__)
		# print "value:", self.value 
		# print "type:", self.type

class SymbolTable:
	def __init__(self, parent):
		self.table = {}
		self.parent = parent
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
		return self.table, self.label
	