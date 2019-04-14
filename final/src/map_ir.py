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
	offset = table[name]['offset']
	if offset >= 0:
		return str(-(offset + 4))
	else:
		return str(-offset)

def is_immediate(var):
	if '(' in var and ')' in var:
		return False
	else:
		return True

def map_instr(instr, scope_list, fp):
	# print instr.instr, instr.type
	if type(instr.type) == tuple and instr.type[0] == 'if':
		jump = get_jump(instr.type[1])
		
		if is_immediate(instr.src1) and is_immediate(instr.src2):
			gen_instr('movl $' + str(instr.src2) + ', %edx', fp)
			gen_instr('cmp $' + str(instr.src1) + ', %edx', fp)
		elif is_immediate(instr.src1):
			src2_offset = get_offset(instr.src2, scope_list)
			gen_instr('movl ' + str(src2_offset) + '(%ebp), %edx', fp)
			gen_instr('cmp $' + str(instr.src1) + ', %edx', fp)
		elif is_immediate(instr.src2):
			src1_offset = get_offset(instr.src1, scope_list)
			gen_instr('movl ' + str(src1_offset) + '(%ebp), %ecx', fp)
			gen_instr('movl $' + str(instr.src2) + ', %edx', fp)
			gen_instr('cmp %ecx, %edx', fp)
		else:
			src1_offset = get_offset(instr.src1, scope_list)
			src2_offset = get_offset(instr.src2, scope_list)
			gen_instr('movl ' + str(src1_offset) + '(%ebp), %ecx', fp)
			gen_instr('movl ' + str(src2_offset) + '(%ebp), %edx', fp)
			gen_instr('cmp %ecx, %edx', fp)
		
		gen_instr(jump + ' ' +  instr.dest, fp)
		
	elif type(instr.type) == tuple and instr.type[0] == 'binop':
		arg = instr.type[1]
		if arg[-1] == 'i': # dest := 0 - src1
			if instr.src1 == '0':
				if arg[:-1] != 'int-':
					print 'error: negation expected'
				else:
					src2_offset = get_offset(instr.src2, scope_list)
					dest_offset = get_offset(instr.dest, scope_list)
					gen_instr('movl ' + str(src2_offset) + '(%ebp), %ecx', fp)
					gen_instr('neg %ecx', fp)
					gen_instr('movl %ecx, ' + str(dest_offset) + '(%ebp)', fp)
				
			else: # dest := src1 + imm
				opcode = get_opcode(arg[:-1])
				if not opcode:
					print 'operation not supported'
				else:
					src1_offset = get_offset(instr.src1, scope_list)
					dest_offset = get_offset(instr.dest, scope_list)
					gen_instr('movl ' + str(src1_offset) + '(%ebp), %edx', fp)
					gen_instr(opcode + ' $' + str(instr.src2) + ', %edx', fp)
					gen_instr('movl %edx, ' + str(dest_offset) + '(%ebp)', fp)
		
		else: # src1 and src2 are variables - temporary or otherwise
			opcode = get_opcode(arg)
			if not opcode:
				print 'operation not supported'
			else:
				src1_offset = get_offset(instr.src1, scope_list)
				src2_offset = get_offset(instr.src2, scope_list)
				dest_offset = get_offset(instr.dest, scope_list)
				gen_instr('movl ' + str(src1_offset) + '(%ebp), %ecx', fp)
				gen_instr('movl ' + str(src2_offset) + '(%ebp), %edx', fp)
				if opcode == 'subl':
					gen_instr(opcode + ' %edx, %ecx', fp)
					gen_instr('movl %ecx, ' + str(dest_offset) + '(%ebp)', fp)
				else:
					gen_instr(opcode + ' %ecx, %edx', fp)
					gen_instr('movl %edx, ' + str(dest_offset) + '(%ebp)', fp)

	elif instr.type == 'assign':
		dest_offset = get_offset(instr.dest, scope_list)

		if is_immediate(instr.src1):
			gen_instr('movl $' + str(instr.src1) + ', ' + str(dest_offset) + '(%ebp)', fp)
		else:
			src_offset = get_offset(instr.src1, scope_list)
			gen_instr('movl ' + str(src_offset) + '(%ebp), %edx', fp)
			gen_instr('movl %edx, ' + str(dest_offset) + '(%ebp)', fp)

	elif instr.type == 'goto':
		gen_instr('jmp ' + instr.dest, fp)

	elif instr.type == 'print':
		if instr.dest == 'int':
			src1_offset = get_offset(instr.src1, scope_list)
			gen_instr('pushl ' + str(src1_offset) + '(%ebp)', fp)
			gen_instr('pushl $outFormatInt', fp)
			gen_instr('call printf', fp)
			gen_instr('pop %ebx', fp)
			gen_instr('pop %ebx', fp)
		else:
			print 'unsupported types for print'

	elif instr.type == 'callvoid':
		gen_instr('call ' + instr.dest, fp)
		gen_instr('addl $' + instr.src1 + ', %esp', fp)

	elif instr.type == 'callint':
		gen_instr('call ' + instr.src1, fp)
		dest_offset = get_offset(instr.dest, scope_list)
		gen_instr('movl -12(%esp), %edx', fp)
		gen_instr('movl %edx, ' + dest_offset + '(%ebp)', fp)
		gen_instr('addl $' + '4' + ', %esp', fp) #TODO

	elif instr.type == 'parameter':
		if is_immediate(instr.dest):
			gen_instr('pushl $' + instr.dest, fp)
		else:
			dest_offset = get_offset(instr.dest, scope_list)
			gen_instr('pushl ' + dest_offset + '(%ebp)', fp)

	elif instr.type == 'retval':
		if is_immediate(instr.src1):
			gen_instr('movl $' + instr.src1 + ', %edx', fp)
		else:
			src_offset = get_offset(instr.src1, scope_list)
			gen_instr('movl ' + src_offset + '(%ebp), %edx', fp)
		gen_instr('movl %edx, -4(%ebp)', fp)

	elif instr.type == 'label':
		if not instr.dest:
			gen_label(instr.instr.split(':')[0], fp)
		else:
			if instr.dest == 'main':
				gen_label('__main__', fp)
			else:
				gen_label(instr.dest, fp)
			
			gen_instr('pushl %ebp', fp)
			gen_instr('movl %esp, %ebp', fp)
			table = scope_list[0].table
			scope = scope_list[table[instr.dest]['func_dict']['symbol_table']]
			gen_instr('subl $' + str(scope.offset) + ', %esp', fp)
	
	elif instr.type == 'retvoid':
		gen_instr("movl %ebp, %esp", fp)
  		gen_instr("pop %ebp", fp)
		gen_instr("ret", fp)

