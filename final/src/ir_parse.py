class instruction:
    def __init__(self, instr):
        self.instr = instr

        args = instr.split(' ')

        if len(args) == 6: # if src1 comp src2 goto dest
            self.type = ('if', args[2])
            self.dest = args[5]
            self.src1 = args[1]
            self.src2 = args[3]
        
        elif len(args) == 5: # dest := src1 op src2
            self.type = ('binop', args[3])
            self.dest = args[0]
            self.src1 = args[2]
            self.src2 = args[4]
        
        elif len(args) == 3 and args[0][0:5] == 'label': # label function dest:
            self.type = 'label'
            self.dest = args[2].split(':')[0]
            self.src1 = None
            self.src2 = None
        
        elif len(args) == 3: # dest := src1 OR dest const:= src1
            self.type = ('assign', args[1])
            self.dest = args[0]
            self.src1 = args[2]
            self.src2 = None
        
        elif len(args) == 2 and args[0] == 'goto': # goto dest
            self.type = 'goto'
            self.dest = args[1]
            self.src1 = None
            self.src2 = None

        elif len(args) == 1 and args[0][0:5] == 'label': # label:
            self.type = 'label'
            self.dest = None
            self.src1 = None
            self.src2 = None

def genInstrObject(ir):
    result = []
    for instr in ir:
        temp = instruction(instr)
        result.append(temp)
    return result