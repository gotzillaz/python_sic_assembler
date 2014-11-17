from sys import argv

class Assembler:
    file_all_line = []
    OPTAB = {}
    SYMTAB = {}
    LOCCTR = 0
    start = 0
    length = 0
    object_codes = []
    location = []

#### Initalize ####
    def __init__(self, file_name):
        assembly_file = open(file_name, 'r')
        self.file_all_line = map(lambda x: x.strip(), assembly_file.readlines())
        self.initOpCode()
        print self.OPTAB
        assembly_file.close()

    def initOpCode(self):
        sic_instruction_file = open('sic_instructions.txt','r')
        sic_instruction_line = sic_instruction_file.readlines()
        for iterator in sic_instruction_line:
            key, value = iterator.split()
            self.OPTAB[key] = value
        sic_instruction_file.close()

#### Pass 1 ####
    def passOne(self):
        for line in self.file_all_line:
            line_col = line.split()
            if len(line_col) == 3:
                if(line_col[1] == 'START'):
                    self.LOCCTR = int(line_col[2], 16)
                    self.start = self.LOCCTR
                    self.SYMTAB[line_col[0]] = self.LOCCTR 
                    self.location.append(self.LOCCTR)
                    continue
                # Store new SYMTAB here
                self.SYMTAB[line_col[0]] = self.LOCCTR 
            elif len(line_col) == 2:
                line_col = [''] + line_col
            elif len(line_col) == 1:
                line_col = [''] + line_col + ['']
            elif len(line_col) == 0:
                continue
            self.location.append(self.LOCCTR) 
            print "NOW : " + line + " " + str(hex(self.LOCCTR))
            if line_col[1] == 'END':
                break
            elif line_col[1] == 'WORD':
                self.LOCCTR += 3
            elif line_col[1] == 'RESW':
                self.LOCCTR += 3 * int(line_col[2])
            elif line_col[1] == 'RESB':
                self.LOCCTR += int(line_col[2])
            elif line_col[1] == 'BYTE':
                #print len(line_col[2].strip()),
                if line_col[2].strip()[0] == 'X':
                    self.LOCCTR += (len(line_col[2].strip())-3)/2
                elif line_col[2].strip()[0] == 'C':
                    self.LOCCTR += len(line_col[2].strip())-3
            else:
                self.LOCCTR += 3
        self.length = self.LOCCTR - self.start
        
#### Pass 2 ####
    def passTwo(self):
        for line in self.file_all_line:
            line_col = line.split()
            x_bit = 0
            object_code = ''
            if len(line_col) == 3:
                if(line_col[1] == 'START'):
                    self.object_codes.append('')
                    continue
            elif len(line_col) == 2:
                line_col = [''] + line_col
            elif len(line_col) == 1:
                line_col = [''] + line_col + ['']
            elif len(line_col) == 0:
                continue    
            #print line
            if line_col[1] == 'END':
                pass
            elif line_col[1] == 'WORD':
                object_code = hex(int(line_col[2]))[2:].upper().zfill(6)
                self.object_codes.append(object_code)
            elif line_col[1] == 'RESW':
                self.object_codes.append('')
            elif line_col[1] == 'RESB':
                self.object_codes.append('')
            elif line_col[1] == 'BYTE':
                if line_col[2].strip()[0] == 'X':
                    object_code = hex(int(line_col[2].strip()[2:-1],16))[2:].upper()
                    self.object_codes.append(object_code)
                elif line_col[2].strip()[0] == 'C':
                    for i in line_col[2].strip()[2:-1]:
                        object_code += hex(ord(i))[2:].upper()
                    self.object_codes.append(object_code)
            else:
                object_code = bin(int(self.OPTAB[line_col[1]],16))[2:].zfill(8)
                if line_col[2].strip()[-2:] == ',X':
                    object_code += '1'
                else:
                    object_code += '0'
                line_col[2] = line_col[2].replace(',X','')
                if line_col[1] == 'RSUB':
                    line_col[2] = '0'
                if self.SYMTAB.has_key(line_col[2].strip()):
                    object_code += bin(self.SYMTAB[line_col[2].strip()])[2:].zfill(15)
                else:
                    object_code += bin(int(line_col[2].strip(),16))[2:].zfill(15)
                object_code = hex(int(object_code, 2))[2:].zfill(6)
                self.object_codes.append(object_code)
            #print object_code
                
#### Get & Set ####
    def getOpCode(self, mnemonic):
        return self.OPTAB[mnemonic]

    def createListingFile(self):
        i = 0
        for line in self.file_all_line:
            line_col = line.split()
            if len(line_col) == 1:
                line_col = [''] + line_col + ['']
            elif len(line_col) == 2:
                line_col = [''] + line_col
            elif len(line_col) == 0:
                continue
            tmp = '\t'.join(line_col)+'\t'
            if i != -1:
                print tmp + self.object_codes[i-1]
            else:
                print tmp
            i += 1

obj = Assembler('1.in')
obj.passOne()
obj.passTwo()
print obj.file_all_line
print obj.length
print obj.location
obj.createListingFile()
