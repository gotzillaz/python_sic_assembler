from sys import argv

class Assembler:
    file_all_line = []
    opcode = {}
    label = {}
    TA = 0
    PC = 0

#### Initalize ####
    def __init__(self, file_name):
        assembly_file = open(file_name, 'r')
        self.file_all_line = map(lambda x: x.strip(), assembly_file.readlines())
        self.initOpCode()
        print self.opcode
        assembly_file.close()

    def initOpCode(self):
        sic_instruction_file = open('sic_instructions.txt','r')
        sic_instruction_line = sic_instruction_file.readlines()
        for iterator in sic_instruction_line:
            key, value = iterator.split()
            self.opcode[key] = value
        sic_instruction_file.close()

#### Pass 1 ####
    def passOne(self):
        for line in self.file_all_line:
            line_col = line.split():
            if len(line_col) == 3:
                pass
            elif len(line_col) == 2:
                pass
            elif len(line_col) == 1:
                pass
            else:
                pass
        
#### Pass 2 ####
    def passTwo(self):
        pass

#### Get & Set ####
    def getOpCode(self, mnemonic):
        return self.opcode[mnemonic]

obj = Assembler('1.in')
print obj.file_all_line
print obj.getOpCode('ADD')
