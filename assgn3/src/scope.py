from utils import SymbolTable

scope_stack = []
scope_list = []
scope_label = 0

# returns current or enclosing scope of the variable
def getScope(ide):
	for scope in scope_stack[::-1]:
		if scope.lookup(ide):
			return scope
	return None

#checks if the variable is in current or some other enclosing scope
def inScope(ide):
	for scope in scope_stack[::-1]:
		if scope.lookup(ide):
			return True
	return False

#checks if variable is in current scope
def inCurrentScope(ide):
	scope = scope_stack[-1]
	return scope.lookup(ide)

def currentScopelabel():
	return scope_stack[-1].label

def addScope():
	if not scope_stack:
		print "scope stack empty: global symbol table not initialised"
	else:
		curr_scope = scope_stack[-1]
		new_scope = SymbolTable(curr_scope)
		global scope_label
		scope_label += 1
		new_scope.label = scope_label
		scope_stack.append(new_scope)
		scope_list.append(new_scope)

def deleteScope():
	if not scope_stack:
		print "scope stack empty: global symbol table not initialised"
	else:
		scope_stack.pop()
