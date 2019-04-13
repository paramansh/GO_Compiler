def getType(instr):
    temp = instr.split(' ')[0]
    if temp == 'goto':
        return 'goto'
    elif temp == 'if':
        return 'if'
    elif temp[0:5] == 'label':
        return 'label'
    elif temp[0:4] == 'call':
        return 'call'
    return "simpls stmt"

class instruction:
    def __init__(self, instr):
        self.instr = instr
        self.type = getType(instr)
        self.src1 = None
        self.src2 = None
        self.dest = None


def genInstrObject(ir):
    result = []
    for instr in ir:
        temp = instruction(instr)
        result.append(temp)
    return result
