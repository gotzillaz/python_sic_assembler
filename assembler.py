from sys import argv,stdout
from traceback import print_exc

class Assembler:
    file_all_line = []
    OPTAB = {}
    SYMTAB = {}
    LOCCTR = 0
    start = 0
    length = 0
    execute = 0
    bitmask = ''
    object_codes = []
    location = []

#### Initalize ####
    def __init__(self, file_name):
        try :
            assembly_file = open(file_name, 'r')
            self.file_all_line = map(lambda x: x.strip().upper(), assembly_file.readlines())
            self.initOpCode()
            print self.OPTAB
            assembly_file.close()
        except IOError:
            print '-' * 60
            print "ERROR : File not found"
            print '-' * 60
            exit()
        except :
            print '-' * 60
            print "ERROR : Unknow error"
            print_exc(file=stdout)
            print '-' * 60
            exit()

    def initOpCode(self):
        try :
            sic_instruction_file = open('sic_instructions.txt','r')
            sic_instruction_line = sic_instruction_file.readlines()
            for iterator in sic_instruction_line:
                key, value = iterator.split()
                self.OPTAB[key] = value
            sic_instruction_file.close()
        except IOError:
            print '-' * 60
            print "ERROR : sic_instructions.txt not found"
            print_exc(file=stdout)
            print '-' * 60
            exit()
        except :
            print '-' * 60
            print "ERROR : Unknow error"
            print '-' * 60
            exit()

#### Pass 1 ####
    def passOne(self):
        for line in self.file_all_line:
            try :
                line_col = line.split()
                if len(line_col) == 3:
                    if(line_col[1] == 'START'):
                        if line_col[2].strip()[-1] == 'H':
                            self.LOCCTR = int(line_col[2].strip()[:-1],16)
                        elif line_col[2].strip()[:2] == '0X':
                            self.LOCCTR = int(line_col[2].strip()[2:],16)
                        else:
                            self.LOCCTR = int(line_col[2].strip())
                        #self.LOCCTR = int(line_col[2], 16)
                        self.start = self.LOCCTR
                        self.SYMTAB[line_col[0]] = self.LOCCTR 
                        self.location.append(self.LOCCTR)
                        continue
                    # Store new SYMTAB here
                    self.SYMTAB[line_col[0]] = self.LOCCTR 
                elif len(line_col) == 2:
                    if line_col[1] == 'RSUB':
                        self.SYMTAB[line_col[0]] = self.LOCCTR
                        line_col = line_col + ['']
                    else:
                        line_col = [''] + line_col
                elif len(line_col) == 1:
                    line_col = [''] + line_col + ['']
                elif len(line_col) == 0:
                    continue
                self.location.append(self.LOCCTR) 
                print "NOW : " + line + " " + str(hex(self.LOCCTR)), len(self.location)
                if line_col[1] == 'END':
                    if self.SYMTAB.has_key(line_col[2].strip()):
                        self.execute = self.SYMTAB[line_col[2].strip()]
                    else :
                        if line_col[2].strip()[-1] == 'H':
                            self.execute = int(line_col[2].strip()[:-1],16)
                        elif line_col[2].strip()[:2] == '0X':
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
            except :
                print '-' * 60
                print "ERROR : Something went wrong in Pass I"
                print "Line : " + line
                print_exc(file=stdout)
                print '-' * 60
                exit()
        self.length = self.LOCCTR - self.start
        
#### Pass 2 ####
    def passTwo(self):
        for line in self.file_all_line:
            try :
                line_col = line.split()
                x_bit = 0
                object_code = ''
                if len(line_col) == 3:
                    if(line_col[1] == 'START'):
                        self.object_codes.append('')
                        self.bitmask += '0'
                        continue
                elif len(line_col) == 2:
                    if line_col[1] == 'RSUB':
                        line_col = line_col + ['']
                    else:
                        line_col = [''] + line_col
                elif len(line_col) == 1:
                    line_col = [''] + line_col + ['']
                elif len(line_col) == 0:
                    continue    
                #print line
                if line_col[1] == 'END':
                    self.bitmask += '0'
                    pass
                elif line_col[1] == 'WORD':
                    if self.SYMTAB.has_key(line_col[2].strip()):
                        object_code = hex(self.SYMTAB[line_col[2].strip()])[2:].zfill(6)
                        self.bitmask += '1'
                    else :
                        object_code = hex(int(line_col[2]))[2:].upper().zfill(6)
                        self.bitmask += '0'
                    self.object_codes.append(object_code)
                elif line_col[1] == 'RESW':
                    self.object_codes.append('')
                    self.bitmask += '0'
                elif line_col[1] == 'RESB':
                    self.object_codes.append('')
                    self.bitmask += '0'
                elif line_col[1] == 'BYTE':
                    if line_col[2].strip()[0] == 'X':
                        object_code = hex(int(line_col[2].strip()[2:-1],16))[2:].upper().zfill(len(line_col[2].strip()[2:-1]))
                        self.object_codes.append(object_code)
                        self.bitmask += '0'
                    elif line_col[2].strip()[0] == 'C':
                        for i in line_col[2].strip()[2:-1]:
                            object_code += hex(ord(i))[2:].upper()
                        self.object_codes.append(object_code)
                        self.bitmask += '0'
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
                        self.bitmask += '1'
                    else:
                        if line_col[2].strip()[-1] == 'H':
                            object_code += bin(int(line_col[2].strip()[:-1],16))[2:].zfill(15)
                        elif line_col[2].strip()[:2] == '0X':
                            object_code += bin(int(line_col[2].strip()[2:],16))[2:].zfill(15)
                        else:
                            object_code += bin(int(line_col[2].strip()))[2:].zfill(15)
                        self.bitmask += '0'
                    object_code = hex(int(object_code, 2))[2:].zfill(6)
                    self.object_codes.append(object_code)
                print self.object_codes[-1], line , self.bitmask[-1], len(self.object_codes)
            except :
                print '-' * 60
                print "ERROR : Something went wrong in Pass II"
                print "Line : " + line
                print_exc(file=stdout)
                print '-' * 60
                exit()
            #print object_code
                
#### Get & Set ####
    def getOpCode(self, mnemonic):
        return self.OPTAB[mnemonic]

    def createListingFile(self):
        i = 0
        listing_list = []
        for line in self.file_all_line:
            try :
                line_col = line.split()
                print len(self.location) , i, hex(self.location[i]), len(self.object_codes),line
                if len(line_col) == 1:
                    line_col = [''] + line_col + ['']
                elif len(line_col) == 2:
                    if line_col[1] == 'RSUB':
                        line_col = line_col + ['']
                    else:
                        line_col = [''] + line_col
                elif len(line_col) == 0:
                    continue
                tmp = '\t'.join(line_col)+'\t'
                if i < len(self.object_codes):
                    #print len(self.location) , i, hex(self.location[i]), len(self.object_codes),line
                    listing_list.append(hex(self.location[i])[2:].zfill(4).upper() + '\t' + tmp + self.object_codes[i].upper())
                else:
                    listing_list.append('\t' + tmp)
                i += 1
            except:
                print '-' * 60
                print "ERROR : Cannot create Listing file"
                print "Line : " + line
                print_exc(file=stdout)
                print '-' * 60
                exit()
        write_file = open(argv[1][:-4]+'.lst','w')
        for line in listing_list:
            write_file.write(line+'\n')
        write_file.close()
        print listing_list

    def createObjectFile(self):
        i = 0
        object_line = ''
        object_list = []
        point = 0
        print "ABSOLUTE ~"
        for line in self.file_all_line:
            try:
                line_col = line.split()
                if len(line_col) == 1:
                    line_col = [''] + line_col + ['']
                elif len(line_col) == 2:
                    if line_col[1] == 'RSUB':
                        line_col = line_col + ['']
                    else:
                        line_col = [''] + line_col
                elif len(line_col) == 0:
                    continue
                if line_col[1] == 'START':
                    object_line = 'H' + line_col[0] + ' '*(6-len(line_col[0])) + hex(self.start)[2:].zfill(6) + hex(self.length)[2:].zfill(6)
                    object_list.append(object_line)
                    object_line = ''
                elif line_col[1] == 'END':
                    if object_line != '':
                        object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) +'000' + object_line
                        object_list.append(object_line)
                        object_line = ''
                    object_line = 'E' + hex(self.execute)[2:].zfill(6)
                    object_list.append(object_line)
                elif line_col[1] == 'RESW' or line_col[1] == 'RESB':
                    if object_line != '':
                        object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) +'000' + object_line
                        object_list.append(object_line)
                        object_line = ''
                else:
                    if len(object_line) + len(self.object_codes[i]) > 60:
                        object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) +'000' + object_line
                        object_list.append(object_line)
                        object_line = ''
                    if object_line == '':
                        point = self.location[i]
                    object_line += self.object_codes[i]
                i += 1
            except :
                print '-' * 60
                print "ERROR : Cannot create Object file (absolute)"
                print "Line : " + line
                print_exc(file=stdout)
                print '-' * 60
                exit()

        object_list = map(lambda x:x.upper(),object_list)
        write_file = open(argv[1][:-4]+'.obj','w')
        for line in object_list:
            write_file.write(line+'\n')
        write_file.close()
        print object_list

    def createObjectFileRelocatable(self):
        i = 0
        object_line = ''
        bitmask_line = ''
        object_list = []
        point = 0
        print "RELOCATABLE ~"
        for line in self.file_all_line:
            try:
                line_col = line.split()
                if len(line_col) == 1:
                    line_col = [''] + line_col + ['']
                elif len(line_col) == 2:
                    if line_col[1] == 'RSUB':
                        line_col = line_col + ['']
                    else:
                        line_col = [''] + line_col
                elif len(line_col) == 0:
                    continue
                if line_col[1] == 'START':
                    object_line = 'H' + line_col[0] + ' '*(6-len(line_col[0])) + hex(self.start)[2:].zfill(6) + hex(self.length)[2:].zfill(6)
                    object_list.append(object_line)
                    object_line = ''
                elif line_col[1] == 'END':
                    if object_line != '':
                        calc_bitmask = hex(int(bitmask_line + '0'*(12-len(bitmask_line)), 2))[2:].zfill(3).upper()
                        bitmask_line = ''
                        object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + calc_bitmask + object_line
                        object_list.append(object_line)
                        object_line = ''
                    object_line = 'E' + hex(self.execute)[2:].zfill(6)
                    object_list.append(object_line)
                elif line_col[1] == 'RESW' or line_col[1] == 'RESB':
                    if object_line != '':
                        calc_bitmask = hex(int(bitmask_line + '0'*(12-len(bitmask_line)), 2))[2:].zfill(3).upper()
                        bitmask_line = ''
                        object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + calc_bitmask + object_line
                        object_list.append(object_line)
                        object_line = ''
                elif line_col[1] == 'WORD' or line_col[1] == 'BYTE':
                    print 'YYYY' , object_line
                    if object_line != '':
                        calc_bitmask = hex(int(bitmask_line + '0'*(12-len(bitmask_line)), 2))[2:].zfill(3).upper()
                        object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + calc_bitmask + object_line
                        object_list.append(object_line)
                    point = self.location[i]
                    bitmask_line = self.bitmask[i]
                    calc_bitmask = hex(int(bitmask_line + '0'*(12-len(bitmask_line)), 2))[2:].zfill(3).upper()
                    bitmask_line = ''
                    object_line = self.object_codes[i]
                    object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + calc_bitmask + object_line
                    object_list.append(object_line)
                    object_line = ''
                else:
                    if len(object_line) + len(self.object_codes[i]) > 60:
                        calc_bitmask = hex(int(bitmask_line + '0'*(12-len(bitmask_line)), 2))[2:].zfill(3).upper()
                        bitmask_line = ''
                        object_line = 'T' + hex(point)[2:].zfill(6) + hex(len(object_line)/2)[2:].zfill(2) + calc_bitmask + object_line
                        object_list.append(object_line)
                        object_line = ''
                    if object_line == '':
                        point = self.location[i]
                    object_line += self.object_codes[i]
                    bitmask_line += self.bitmask[i]
                i += 1
            except :
                print '-' * 60
                print "ERROR : Cannot create Object file (relocatable)"
                print "Line : " + line
                print_exc(file=stdout)
                print '-' * 60
                exit()

        object_list = map(lambda x:x.upper(),object_list)
        write_file = open(argv[1][:-4]+'.obj','w')
        for line in object_list:
            write_file.write(line+'\n')
        write_file.close()
        print object_list

if len(argv) <= 1:
    print '-' * 60
    print "ERROR : Invalid argrument"
    print '-' * 60
    exit()
if argv[1][-4:].upper() != '.ASM':
    print '-' * 60
    print "ERROR : Please Input file .ASM"
    print '-' * 60
    exit()
obj = Assembler(argv[1])
obj.passOne()
print obj.SYMTAB
obj.passTwo()
print obj.file_all_line ,len(obj.file_all_line)
print obj.object_codes, len(obj.object_codes)
print obj.length
print obj.location, len(obj.location)
obj.createListingFile()
if obj.start != 0:
    obj.createObjectFile()
else :
    obj.createObjectFileRelocatable()