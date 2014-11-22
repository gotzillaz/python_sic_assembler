from sys import argv

INSTR = ['ADD','AND','COMP', 'DIV', 'J', 'JEQ', 'JGT', 'JLT', 'JSUB', 'LDA', 'LDCH'
        ,'LDL', 'LDX', 'MUL', 'OR', 'RD', 'RSUB', 'STA', 'STCH', 'STL', 'STSW', 'STX'
        ,'SUB', 'TD', 'TIX', 'WD','START','BYTE','WORD','RESW','RESB','END']
CONST = ['WORD','RESB','RESW','BYTE']
CONST2 = ['WORD','BYTE']
CONST3 = ['RESB','RESW']
LS = [ i for i in INSTR if i not in CONST]
#name_label_instr_TA
data = []
count = 0
def prepare_data(f):
#    f = open('test.txt','r+')
    for line in f:
        line=line.replace("\n", "")
        x = line.split()[:3]
        if len(x)<3:
            x.insert(0,'0')
        if 'RSUB' in x:
            x.append('0')
        if len(x) == 3 or 'RSUB' in x:
            x = x[0]+' '+x[1]+' '+x[2]
            x = x.upper()
            data.append(x)     
      #  print x
        x=""
    return data

def check_mnemonic(data):
    for line in data:
        x=line.split()
        if x[1] not in INSTR:
            print 'no instruction support SIC',x
            exit()

def check_label(data):
    for line in data:
        x = line.split()
        if len(x[0])>6:
            print 'out of length Label',x
            exit()

def check_xmode(x):
    xmode = x[2].split(',')
    if len(xmode) == 2:
        if xmode[1] != 'X':
            print xmode[1],'?'
            exit()
        return 1
    elif len(xmode) == 1:
        return 0
    else:
        print 'xmode failed'
        exit()

def check_length_label(TA):
    if len(TA[0]) > 6 or (TA[0][0] in 'CX' and TA[0][-1] in '\''):
        print 'error'
        exit()

def check_all(data):

    for line in data:
        x = line.split()
        print x
        if x[1] == 'RSUB':
            if x[2] != '0':
                print 'RSUB dont need operand',x
                exit()
        elif x[1] in CONST :
            isX = check_xmode(x)
            if isX:
                print 'error BYTE WORD no Xmode'
                exit()
            TA = x[2].split(',')
            #check_length_label(TA)
            try:
                val = int(TA[0])
                
            except:
                #print x
                if x[1] in CONST2:
                    if TA[0][0] not in 'CX' or TA[0][-1] not in '\'':
                        print 'error',x
                        exit()
                elif x[1] in CONST3:
                    print 'error RESB RESW dec only'
                    exit()
            
        elif x[1] in LS:
            isX = check_xmode(x)
            TA = x[2].split(',')
            check_length_label(TA) 
           # TA[0] = TA[0][::-1]
           # print x
            try:  #only hex 
                val = int(TA[0],16)

            except: # another 's Label
                pass
                    
     #   print x   #         
                    

script, filename = argv
f = open(filename,'r+')
data = prepare_data(f)
check_mnemonic(data)
check_label(data)
check_all(data)
#print data 
f.close()
