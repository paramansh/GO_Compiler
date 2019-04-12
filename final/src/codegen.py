from codegen_utils import *
from asm_utils import *
import basic_block
import ir_parse

ircode = []
with open('ircode', 'r') as f:
    line = f.readline()
    while line:
        ircode.append(line)
        line = f.readline().strip()

instructions = ir_parse.genInstrObject(ircode)

basic_blocks = basic_block.genBlocks(instructions)

# for b in basic_blocks:
#     print b, ircode[b[0]: b[1] + 1]

f = open('symtab_pickle', 'r')
scope_list = pickle.load(f)
f.close()

for scope in scope_list[::-1]:
	entries = scope.getAllEntries()
	pp.pprint(entries[1])
	pp.pprint(entries[0])
	pp.pprint(entries[2])

f = open('asmcode.s', 'w')
init_globals(scope_list[0], f)
closefile(f)
