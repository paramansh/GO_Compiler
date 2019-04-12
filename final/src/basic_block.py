from codegen_utils import *

def genBlocks(instructions):
    start = 0
    blocks = []
    for index, instr in enumerate(instructions):
        # print instr.type
        if instr.type in ['goto', 'call', 'if']:
            blocks.append((start, index))
            start = index + 1
        elif instr.type in ['label']:
            if index > 0 and index > start:
                blocks.append((start, index-1))
            start = index
        elif index == len(instructions) - 1:
            blocks.append((start, index))
    return blocks


