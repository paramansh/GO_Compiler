from utils import SymbolTable

scope_stack = []
scope_label = 0

def getScope(ide):
	for scope in scope_stack[::-1]:
		if scope.lookup(ide):
			return scope
	return None

def scopeCheck(ide):
	for scope in scope_stack[::-1]:
		if scope.lookup(ide):
			return True
	return False

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

def deleteScope():
	if not scope_stack:
		print "scope stack empty: global symbol table not initialised"
	else:
		scope_stack.pop()
