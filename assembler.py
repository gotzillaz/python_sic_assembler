from sys import argv

class Assembler:
    file_all_line = []
    opcode = {}
    label = {}
    TA = 0
    PC = 0
    LOCCTR = 0
    start = 0
    length = 0

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
                if(line_col[1] == 'START'):
                    self.LOCCTR = int(line_col[2], 16)
                    self.start = self.LOCCTR
                # Store new label here
                label[line_col[0]] = self.LOCCTR 
            elif len(line_col) == 2:
                line_col = [''] + line_col
            elif len(line_col) == 1:
                line_col = [''] + line_col + ['']
            if line_col[1] == 'END':
                break
            elif line_col[1] == 'WORD':
                self.LOCCTR += 3
            elif line_col[1] == 'RESW':
                self.LOCCTR += 3 * int(line_col[2], 16)
            elif line_col[1] == 'RESW':
                self.LOCCTR += int(line_col[2], 16)
            elif line_col[1] == 'BYTE':
                if line_col[2][0] == 'X':
                    self.LOCCTR += len(line_col[2]-3)/2
                elif line_col[2][0] == 'C':
                    self.LOCCTR += len(line_col[2]-3)
            else:
                self.LOCCTR += 3
        self.length = self.LOCCTR - self.start
        
#### Pass 2 ####
    def passTwo(self):
        pass

#### Get & Set ####
    def getOpCode(self, mnemonic):
        return self.opcode[mnemonic]

obj = Assembler('1.in')
print obj.file_all_line
print obj.getOpCode('ADD')
