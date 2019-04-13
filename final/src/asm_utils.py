import pprint as pp
import cPickle as pickle

def init_globals(scope_list, fp):
    fp.write('.data\n\n')

    table = scope_list[0].table
    for entry in table:
        if table[entry]['type'] != 'func':
            fp.write(entry + ':\n\t.' + table[entry]['type'] + '\t' + str(table[entry]['value']) + '\n')
    
    fp.write('outFormatInt:\n\t.asciz\t"%d\\n"\n')
    fp.write('outFormatStr:\n\t.asciz\t"%s\\n"\n')
    fp.write('inFormat:\n\t.ascii\t"%d"\n')
    fp.write('\n.text\n\n.global main\n\nmain:\n\n')
    gen_instr('call __main__', fp)
    gen_instr('jmp exit', fp)
    fp.write('\n\n__main__:\n\n')
    gen_instr('pushl %ebp', fp)
    gen_instr('movl %esp, %ebp', fp)

    main_scope = scope_list[table['main']['func_dict']['symbol_table']]
    gen_instr('subl $' + str(main_scope.offset) + ', %esp', fp)

def gen_label(label, fp):
    fp.write('\n' + label + ':\n\n')

def gen_instr(instr, fp):
    fp.write('\t' + instr + '\n')

def closefile(fp):
    gen_label('exit', fp)
    gen_instr('movl $0, %ebx', fp)
    gen_instr('movl $1, %eax', fp)
    gen_instr('int $0x80', fp)
    fp.close()