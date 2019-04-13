from codegen_utils import *
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

for b in basic_blocks:
    print b, ircode[b[0]: b[1] + 1]

