from asm_utils import *

opcode = {
	'int+' : 'addl',
	'int-' : 'subl',
	'int*' : 'imul'
	# 'int/' : 'idiv',
}

jumps = {
	'<' : 'jg',
	'>' : 'jl',
	'<=' : 'jge',
	'>=' : 'jle',
	'==' : 'je',
	'!=' : 'jne'
}

def get_opcode(x):
	if x in opcode.keys():
		return opcode[x]
	else:
		return None

def get_jump(x):
	if x in jumps.keys():
		return jumps[x]
	else:
		return None
	
def separate(var):
	name = var.split('(')[0]
	scope = var.split('(')[1].split(')')[0]
	return name, int(scope)

def get_offset(var, scope_list):
	name, scope = separate(var)
	table = scope_list[scope].table
	return table[name]['offset'] + 8

def is_immediate(var):
	if '(' in var and ')' in var:
		return False
	else:
		return True

def map_instr(instr, scope_list, fp):
	# print instr.instr
	if type(instr.type) == tuple and instr.type[0] == 'if':
		jump = get_jump(instr.type[1])
		
		if is_immediate(instr.src1) and is_immediate(instr.src2):
			gen_instr('movl $' + str(instr.src2) + ', %edx', fp)
			gen_instr('cmp $' + str(instr.src1) + ', %edx', fp)
		elif is_immediate(instr.src1):
			src2_offset = get_offset(instr.src2, scope_list)
			gen_instr('movl -' + str(src2_offset) + '(%ebp), %edx', fp)
			gen_instr('cmp $' + str(instr.src1) + ', %edx', fp)
		elif is_immediate(instr.src2):
			src1_offset = get_offset(instr.src1, scope_list)
			gen_instr('movl -' + str(src1_offset) + '(%ebp), %ecx', fp)
			gen_instr('movl $' + str(instr.src2) + ', %edx', fp)
			gen_instr('cmp %ecx, %edx', fp)
		else:
			src1_offset = get_offset(instr.src1, scope_list)
			src2_offset = get_offset(instr.src2, scope_list)
			gen_instr('movl -' + str(src1_offset) + '(%ebp), %ecx', fp)
			gen_instr('movl -' + str(src2_offset) + '(%ebp), %edx', fp)
			gen_instr('cmp %ecx, %edx', fp)
		
		gen_instr(jump + ' ' +  instr.dest, fp)
		
	elif type(instr.type) == tuple and instr.type[0] == 'binop':
		arg = instr.type[1]
		if arg[-1] == 'i': # either src1 or src2 is immediate operand
			if instr.src1 == '0':
				if arg[:-1] != 'int-':
					print 'error in negation'
				else:
					src2_offset = get_offset(instr.src2, scope_list)
					dest_offset = get_offset(instr.dest, scope_list)
					gen_instr('movl -' + str(src2_offset) + '(%ebp), %ecx', fp)
					gen_instr('neg %ecx', fp)
					gen_instr('movl %ecx, -' + str(dest_offset) + '(%ebp)', fp)
				
			else:
				opcode = get_opcode(arg[:-1])
				if not opcode:
					print 'operation not supported'
				else:
					src1_offset = get_offset(instr.src1, scope_list)
					dest_offset = get_offset(instr.dest, scope_list)
					gen_instr('movl -' + str(src1_offset) + '(%ebp), %edx', fp)
					gen_instr(opcode + ' $' + str(instr.src2) + ', %edx', fp)
					gen_instr('movl %edx, -' + str(dest_offset) + '(%ebp)', fp)
		
		else: # src1 and src2 are variables - temporary or otherwise
			opcode = get_opcode(arg)
			if not opcode:
				print 'operation not supported'
			else:
				src1_offset = get_offset(instr.src1, scope_list)
				src2_offset = get_offset(instr.src2, scope_list)
				dest_offset = get_offset(instr.dest, scope_list)
				gen_instr('movl -' + str(src1_offset) + '(%ebp), %ecx', fp)
				gen_instr('movl -' + str(src2_offset) + '(%ebp), %edx', fp)
				gen_instr(opcode + ' %ecx, %edx', fp)
				gen_instr('movl %edx, -' + str(dest_offset) + '(%ebp)', fp)

	elif type(instr.type) == tuple  and instr.type[0] == 'assign':
		dest_offset = get_offset(instr.dest, scope_list)

		if instr.type[1] == ':=':
			src_offset = get_offset(instr.src1, scope_list)
			gen_instr('movl -' + str(src_offset) + '(%ebp), %edx', fp)
			gen_instr('movl %edx, -' + str(dest_offset) + '(%ebp)', fp)
		else:
			gen_instr('movl $' + str(instr.src1) + ', -' + str(dest_offset) + '(%ebp)', fp)

	elif instr.type == 'goto':
		gen_instr('jmp ' + instr.dest, fp)

	elif instr.type == 'print':
		if instr.dest == 'int':
			src1_offset = get_offset(instr.src1, scope_list)
			gen_instr('pushl -' + str(src1_offset) + '(%ebp)', fp)
			gen_instr('pushl $outFormatInt', fp)
			gen_instr('call printf', fp)
			gen_instr('pop %ebx', fp)
			gen_instr('pop %ebx', fp)
		else:
			print 'unsupported types for print'

	elif instr.type == 'label':
		if not instr.dest:
			gen_label(instr.instr.split(':')[0], fp)

