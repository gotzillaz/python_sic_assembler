from sys import argv

class Assembler:
    file_all_line = []
    OPTAB = {}
    SYMTAB = {}
    LOCCTR = 0
    start = 0
    length = 0
    execute = 0
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
                if self.SYMTAB.has_key(line_col[2].strip()):
                    self.execute = self.SYMTAB[line_col[2].strip()]
                else :
                    if line_col[2].strip()[-1] == 'h':
                        self.execute = int(line_col[2].strip()[:-1],16)
                    elif line_col[2].strip()[:2] == '0x':
                        self.execute = int(line_col[2].strip()[2:],16)
                    else:
                        self.execute = int(line_col[2].strip())
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
                    object_code = hex(int(line_col[2].strip()[2:-1],16))[2:].upper().zfill(len(line_col[2].strip()[2:-1]))
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
                    if line_col[2].strip()[-1] == 'h':
                        object_code += bin(int(line_col[2].strip()[:-1],16))[2:].zfill(15)
                    elif line_col[2].strip()[:2] == '0x':
                        object_code += bin(int(line_col[2].strip()[2:],16))[2:].zfill(15)
                    else:
                        object_code += bin(int(line_col[2].strip()))[2:].zfill(15)
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
            if i+1 < len(self.file_all_line):
                print hex(self.location[i])[2:].zfill(4).upper() + '\t' + tmp + self.object_codes[i].upper()
            else:
                print '\t' + tmp
            #print i,len(self.file_all_line)
            i += 1

    def createObjectFile(self):
        i = 0
        object_line = ''
        object_head = ''
        object_list = []
        point = 0
        line_size = 999
        for line in self.file_all_line:
            line_col = line.split()
            if len(line_col) == 1:
                line_col = [''] + line_col + ['']
            elif len(line_col) == 2:
                line_col = [''] + line_col
            elif len(line_col) == 0:
                continue
            if line_col[1] == 'START':
                object_line = 'H' + line_col[0] + ' ' + hex(self.start)[2:].zfill(6) + hex(self.length)[2:].zfill(6)
                object_list.append(object_line)
                object_line = ''
            elif line_col[1] == 'END':
                if object_line != '':
                    object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + object_line
                    object_list.append(object_line)
                    object_line = ''
                object_line = 'E' + hex(self.execute)[2:].zfill(6)
                object_list.append(object_line)
            elif line_col[1] == 'RESW' or line_col[1] == 'RESB':
                if object_line != '':
                    object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + object_line
                    object_list.append(object_line)
                    object_line = ''
            else:
                if len(object_line) + len(self.object_codes[i]) > 60:
                    object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + object_line
                    object_list.append(object_line)
                    object_line = ''
                if object_line == '':
                    point = self.location[i]
                object_line += self.object_codes[i]
                    
            i += 1
        object_list = map(lambda x:x.upper(),object_list)
        print object_list

obj = Assembler('1.in')
obj.passOne()
obj.passTwo()
print obj.file_all_line ,len(obj.file_all_line)
print obj.object_codes, len(obj.object_codes)
print obj.length
print obj.location
obj.createListingFile()
obj.createObjectFile()
