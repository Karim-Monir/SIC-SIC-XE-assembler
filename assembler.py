import re, os , sys
# Data in the example_file.txt :
'''
Prog1   START   0000
        LDA     ZERO
        STA     INDEX
LOOP    LDX     INDEX
        LDA     ZERO
        STA     ALPHA,X
        LDA     INDEX
        ADD     THREE
        STA     INDEX
        COMP    K300
        TIX     TWENTY
        JLT     LOOP
INDEX   RESW    1
ALPHA   RESW    100
ZERO    WORD    0
K300    WORD    100
THREE   WORD    3
TWENTY  WORD    20
        BYTE    C'EOF'
        BYTE    X'F1', X'05' 
        END     Prog1
'''

# Listing the SIC & SIC/XE instructions and directives in a dictionary:
machine_instructions = dict()
machine_instructions = {
    "ADD":{"mnemonic": "ADD", "opcode":"18", "is_directive": False},
    "ADDF":{"mnemonic": "ADDF", "opcode":"58", "is_directive":False},
    "ADDR":{"mnemonic": "ADDR", "opcode":"90", "is_directive":False},
    "AND":{"mnemonic": "AND", "opcode":"40", "is_directive":False},
    "CLEAR":{"mnemonic": "CLEAR", "opcode":"B4", "is_directive":False},
    "COMP":{"mnemonic": "COMP", "opcode":"28", "is_directive":False},
    "COMPF":{"mnemonic": "COMPF", "opcode":"88", "is_directive":False},
    "COMPR":{"mnemonic": "COMPR", "opcode":"A0", "is_directive":False},
    "DIV":{"mnemonic": "DIV", "opcode":"24", "is_directive":False},
    "DIVF":{"mnemonic": "DIVF", "opcode":"64", "is_directive":False},
    "DIVR":{"mnemonic": "DIVR", "opcode":"9C", "is_directive":False},
    "FIX":{"mnemonic": "FIX", "opcode":"C4", "is_directive":False},
    "FLOAT":{"mnemonic": "FLOAT", "opcode":"C0", "is_directive":False},
    "HIO":{"mnemonic": "HIO", "opcode":"F4", "is_directive":False},
    "J":{"mnemonic": "J", "opcode":"3C", "is_directive":False},
    "JEQ":{"mnemonic": "JEQ", "opcode":"30", "is_directive":False},
    "JGT":{"mnemonic": "JGT", "opcode":"34", "is_directive":False},
    "JLT":{"mnemonic": "JLT", "opcode":"38", "is_directive":False},
    "JSUB":{"mnemonic": "JSUB", "opcode":"48", "is_directive":False},
    "LDA":{"mnemonic": "LDA", "opcode":"00", "is_directive":False},
    "LDB":{"mnemonic": "LDB", "opcode":"68", "is_directive":False},
    "LDCH":{"mnemonic": "LDCH", "opcode":"50", "is_directive":False},
    "LDF":{"mnemonic": "LDF", "opcode":"70", "is_directive":False},
    "LDL":{"mnemonic": "LDL", "opcode":"08", "is_directive":False},
    "LDS":{"mnemonic": "LDS", "opcode":"6C", "is_directive":False},
    "LDT":{"mnemonic": "LDT", "opcode":"74", "is_directive":False},
    "LDX":{"mnemonic": "LDX", "opcode":"04", "is_directive":False},
    "LPS":{"mnemonic": "LPS", "opcode":"D0", "is_directive":False},
    "MUL":{"mnemonic": "MUL", "opcode":"20", "is_directive":False},
    "MULF":{"mnemonic": "MULF", "opcode":"60", "is_directive":False},
    "MULR":{"mnemonic": "MULR", "opcode":"98", "is_directive":False},
    "NORM":{"mnemonic": "NORM", "opcode":"C8", "is_directive":False},
    "OR":{"mnemonic": "OR", "opcode":"44", "is_directive":False},
    "RD":{"mnemonic": "RD", "opcode":"D8", "is_directive":False},
    "RMO":{"mnemonic": "RMO", "opcode":"AC", "is_directive":False},
    "RSUB":{"mnemonic": "RSUB", "opcode":"4C", "is_directive":False},
    "SHIFTL":{"mnemonic": "SHIFTL", "opcode":"A4", "is_directive":False},
    "SHIFTR":{"mnemonic": "SHIFTR", "opcode":"A8", "is_directive":False},
    "SIO":{"mnemonic": "SIO", "opcode":"F0", "is_directive":False},
    "SSK":{"mnemonic": "SSK", "opcode":"EC", "is_directive":False},
    "STA":{"mnemonic": "STA", "opcode":"0C", "is_directive":False},
    "STB":{"mnemonic": "STB", "opcode":"78", "is_directive":False},
    "STCH":{"mnemonic": "STCH", "opcode":"54", "is_directive":False},
    "STF":{"mnemonic": "STF", "opcode":"80", "is_directive":False},
    "STI":{"mnemonic": "STI", "opcode":"D4", "is_directive":False},
    "STL":{"mnemonic": "STL", "opcode":"14", "is_directive":False},
    "STS":{"mnemonic": "STS", "opcode":"7C", "is_directive":False},
    "STSW":{"mnemonic": "STSW", "opcode":"E8", "is_directive":False},
    "STT":{"mnemonic": "STT", "opcode":"84", "is_directive":False},
    "STX":{"mnemonic": "STX", "opcode":"10", "is_directive":False},
    "SUB":{"mnemonic": "SUB", "opcode":"1C", "is_directive":False},
    "SUBF":{"mnemonic": "SUBF", "opcode":"5C", "is_directive":False},
    "SUBR":{"mnemonic": "SUBR", "opcode":"94", "is_directive":False},
    "SVC":{"mnemonic": "SVC", "opcode":"B0", "is_directive":False},
    "TD":{"mnemonic": "TD", "opcode":"E0", "is_directive":False},
    "TIO":{"mnemonic": "TIO", "opcode":"F8", "is_directive":False},
    "TIX":{"mnemonic": "TIX", "opcode":"2C", "is_directive":False},
    "TIXR":{"mnemonic": "TIXR", "opcode":"B8", "is_directive":False},
    "WD":{"mnemonic": "WD", "opcode":"DC", "is_directive":False},

    # Directives of SIC & SIC/XE machines
    "START":{"mnemonic": "START", "opcode":"", "is_directive":True},
    "END":{"mnemonic": "END", "opcode":"", "is_directive":True},
    "EQU":{"mnemonic": "EQU", "opcode":"", "is_directive":True},
    "ORG":{"mnemonic": "ORG", "opcode":"", "is_directive":True},
    "BASE":{"mnemonic": "BASE", "opcode":"", "is_directive":True},
    "LTORG":{"mnemonic": "LTORG", "opcode":"", "is_directive":True},
    "RESW":{"mnemonic": "RESW", "opcode":"", "is_directive":True},
    "RESB":{"mnemonic": "RESB", "opcode":"", "is_directive":True},
    "BYTE":{"mnemonic": "BYTE", "opcode":"", "is_directive":True},
    "NOBASE":{"mnemonic": "NOBASE", "opcode":"", "is_directive":True},
    "WORD":{"mnemonic": "WORD", "opcode":"", "is_directive":True},
}
# =================================
# Functions for operations on file:
# =================================


# =========================================================================
# Reading example_file.txt and making a list of each line in a prime list:
# "^\s" is a regular expression for lines starting with white spaces:
# =========================================================================
def create_prime_list (file_handle):
    for line in file_handle:
        line = line.rstrip()
        prime_list.append(line.split())
        match = re.search("^\s", line)
        if  match:
            prime_list[-1].insert(0, "    ")
    return prime_list
# ==============================================================
# To find the location of starting:
# Takes a list as an argument:
# To be used in the function that will return program length:
# ==============================================================
#checkStart
def find_starting_location(list) :
    for i in range(len(list)) :
        for j in range(len(list[i])) :
            if list[i][j] == "START" :
                #returns the starting location ("0000" in test file)
                return list[i][-1]


# ================================================================
# To determine the number of characters for byte instruction: 
# (BYTE 'EOF') & (BYTE  X'F1' , X'05'):
# To be used in the function of determining addresses of pass 1
# Takes a string as an argument
# ================================================================
#charnumber
def number_of_characters(string) :
    location_countersList_list = list()
    location_countersList_list = str.split("'")
    # Return the first split element after the " ' " :
    return len(location_countersList_list[1])



# ==============================================================
# finding the number of special charcters
def specialCharNumber(str) :
    l = list()
    l = str.split("X")
    return (len(l)) - 1



# ==============================================================
# To convert the size for each mnemonic into hexadecimal format
# before adding it to the previous one for pass 1:
# Takes string (from a split list), 
# value (to be determined depending on mnemonic's variable), and
# the constat instruction length of 3:
# "{:0>4s}" is 
# 16 is the hexadecimal format base:
# [2:] is 
# upper() is
# ===============================================================
# def addHex
def hexa_conversion(string, value, size = 3) :
    return "{:0>4s}".format(hex(int(string, 16) + value * size)[2:]).upper()



# ==============================================================
# To determine the program length to be used in HTE records
# Length = (the end location) - (the start location)
# takes the start and end locations of the program given
# "{:0>4s}" means 
# [2:] means 
# .upper() is to 
# 16 is the base for hexadecimal 
# ==============================================================
# calculateLength
def program_length(end, start) :
    return "{:0>4s}".format(hex(int(end, 16) - int(start, 16))[2:]).upper()

# =====================================================================
# Obtaining location counters and appending them into a temporary list:
# Takes the list of lists containing the lines split from the file:
# list is a list of lines from main file split as lists: 
# =====================================================================
#def calculateAdresses(list) :

def obt_location_counters(list) :
    location_countersList = []
    start = find_starting_location(list)
    for i in range(len(list)) :
        val = 1
        if i == len(list) - 1:
            break
        if i == 0 :
            location_countersList.append("    ")
            continue
        if i == 1:
            location_countersList.append(start)
        if list[i][1] == machine_instructions["RESW"]["mnemonic"] :
            val = int(list[i][2])
            location_countersList.append(hexa_conversion(location_countersList[-1], val))
            continue
        if list[i][1] == machine_instructions["RESB"]["mnemonic"] :
            val = int(list[i][2])
            location_countersList.append(hexa_conversion(location_countersList[-1], val, 1))
            continue
        if list[i][1] == machine_instructions["BYTE"]["mnemonic"] :
            if list[i][2].lower().startswith("C") :
                val = number_of_characters(list[i][2])
                location_countersList.append(hexa_conversion(location_countersList[-1], val, 1))
                continue
            if list[i][2].lower().startswith("X") :
                val = specialCharNumber(list[i][2])
                location_countersList.append(hexa_conversion(location_countersList[-1], val, 1))
                continue
        location_countersList.append(hexa_conversion(location_countersList[-1], val))
    return location_countersList


# ================================================================================
# This is to create the symbol table for pass 1:
# Puts the symbol and it's location counter in a dictionary as key-value respectively:
# Takes the primary list after appending location counters in it as an argument:
# ================================================================================
def symbol_table(prime_list) :
    symbol_tabDict = {}
    for i in range(len(prime_list)) :
        # To check on the line that it doesn't start with white spaces nor program name
        if not prime_list[i][0] == "    " and not prime_list[i][0] == prime_list[0][0]:
            symbol_tabDict[prime_list[i][0]] = prime_list[i][3]
            # st.append([prime_list[i][0], prime_list[i][3]])
    return symbol_tabDict




# ==================================================================================
# This function is to make the object code for pass 2:
# Obtains object code and appends it into a list:
# Returns a list of the object code:
# ==================================================================================
def obt_object_code(prime_list, symbol_tabDict) :
    objectCode = list()
    for i in range(len(prime_list)) :
        if prime_list[i][1] == "END" :
            objectCode.append("    ")
            break
        if i == 0 :
            objectCode.append("    ")
            continue

        if not machine_instructions[prime_list[i][1]]["is_directive"] :
            try :
                objectCode.append(machine_instructions[prime_list[i][1]]["opcode"] + symbol_tabDict[prime_list[i][2]])
            except :
                temp = prime_list[i][2].split(",")
                objectCode.append(machine_instructions[prime_list[i][1]]["opcode"] + symbol_tabDict[temp[0]])
        
        if machine_instructions[prime_list[i][1]]["is_directive"] :
            if prime_list[i][1].startswith("RES") :
                objectCode.append("No Object Code")
            elif prime_list[i][1] == "WORD" :
                objectCode.append("{:0>6s}".format(hex(int(prime_list[i][2]))[2:]))
            elif prime_list[i][1] == "BYTE" :
                if prime_list[i][2].startswith("C") :
                    objectCode.append("{:0>6s}".format(hex(int(number_of_characters(prime_list[i][2])))[2:]))
                elif prime_list[i][2].startswith("X") :
                    objectCode.append("{:0>6s}".format(hex(int(specialCharNumber(prime_list[i][2])))[2:]))
                else :
                    objectCode.append("{:0>6s}".format(hex(int(prime_list[i][2]))[2:]))    
    return objectCode
# =============================================================================================


# ==============================================================================
# This function is to create the output file:
# This is also for writing pass 1 and pass 2:
# Writing HTE Records:
# ==============================================================================
    
# ============================================================================================

# ==================================================================================

file_name = "example_file.txt"
file_handle = open(file_name)
prime_list = list()
symbol_tab = {}
prime_list = create_prime_list (file_handle)
#print(prime_list)

location_counters = obt_location_counters(prime_list)

for i in range(len(location_counters)) :
    prime_list[i].append(location_counters[i])

#print(prime_list)

symbol_tab = symbol_table(prime_list)
print(symbol_tab)
