#!/usr/bin/env python3

'''
Vasileios Papasakellariou 1762
Ioannis Aristeidhs Papasakellariou 2520
'''
import sys
import os
import re
import pprint

''' global variables for intermidiate code'''
''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''
quads = []
changedQuads = []
fullCode = {}
quad = {}
nextquad = {}
labelNum = 0
tempBaseName = "T_"
tempVarCount = -1
tempLabName = "L_"
tempLabCount = -1
firstLabels = dict()

'''global variables for symbol table'''
'''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''

symbolTable = {"program" : {"scopeName" : "program",
                            "type"      : "int",
                            "returnType": "UNKNOWN",
							"nestingLevel"	:	0
                }

}

stackHistory = list()
stackOffset = [12] # every newe address for every different scope created
functionList = {'program' : symbolTable['program']}
scopeStack = [symbolTable["program"]]
nestingLevel = 0
''''''''''''''''''''''''''''''''''''''''''''''''''''''

counterFunRet = dict()
counterProcRet = dict()
#procedureName = ""   
functionName = ""
#programName = ""
numberid = "0"
wordid = ""
selectCounter = 1
checkExit = False
white_operators = ['\t', ' ']

keywords = ["and", "declare", "do", "else", "enddeclare",
            "exit", "procedure", "function", "print", "call",
            "if", "in", "inout", "not", "select", "program",
            "or", "return", "while", "default"]
keywords_found = []
identifiers_found = []
numbers_found = []

comparison = ["<", ">", "=", "<=", ">=", "<>"]
comparisons_found = []

numeric_operators = ["+", "-", "*", "/"]
numeric_operators_found = []

grouping_symbols = ["{", "}", "(", ")", "[", "]"]
grouping_symbols_found = []

delimetrs = [":",";", ","]
delimetrs_found = []


line_number = 0
f2_position = 0
token = None
EOF = ""

''' take the last argument of the command line'''
f1 = sys.argv[-1]
'''
f2_name = input("Enter the name of f2 u want to parse:")
'''
try:
    f2 = open(f1,"r")
except (OSError,IOError):
    print("The f2 does not exist!")
    sys.exit()

try:
	finalCode = open("finalCode.txt", "w")
except (OSError, IOError):
	print("Error!!")
	sys.exit()


'''moving one character back'''
def move_f2position(): 
    global f2_position
    f2.seek(0)
    f2_position-= 1
    f2.seek(f2_position)


def read_number():
    global f2_position
    number_digits = []
    char = f2.read(1)
    f2_position+= 1
    while char.isdigit():
        number_digits.append(char)
        char = f2.read(1)
        f2_position+= 1
    if char != EOF:
        move_f2position()

    number = ""
    return number.join(number_digits)


def read_identifier():
    global f2_position
    lexeme_characters = []
    full_identifier =[]
    char = f2.read(1)
    f2_position+= 1
    while char.isalpha() or char.isdigit():
        if len(lexeme_characters)<30:
            lexeme_characters.append(char)
            full_identifier.append(char)
            char = f2.read(1)
            f2_position+= 1
        else:
            full_identifier.append(char)
            char = f2.read(1)
            f2_position+= 1
    if char != EOF:
        move_f2position()
    if len(lexeme_characters)<len(full_identifier):
        print("the Identifier %s length is too big.Only first 30 characters will be taken %s" % ("".join(full_identifier),"".join(lexeme_characters)))
    lexeme = ""
    return lexeme.join(lexeme_characters)

def read_numeric_operator(char):
    if char == '+':
        numeric_operators_found.append(char)
        return True
    elif char == '-':
        numeric_operators_found.append(char)
    elif char == '/':
        numeric_operators_found.append(char)
        return True
    elif char == '*':
        numeric_operators_found.append(char)
        return True
    else:
        return False

def read_comparison(char):
    global f2_position
    comparison = []
    comparison.append(char)
    char = f2.read(1)
    f2_position+= 1
    if char == '=':
        comparison.append(char)
        return "".join(comparison)
    elif char == '>':
        comparison.append(char)
        return "".join(comparison)
    else:
        move_f2position()
        return "".join(comparison)

def check_number(number):
    if number >= -32768 and number <= 32767:
        return True
    else:
        return False
    
class Lectical_Unit(object):
    UNKNOWN = -1
    EOF = 1
    AND = 2
    DECLARE = 3
    DO = 4
    ELSE = 5
    ENDDECLARE = 6
    EXIT = 7
    PROCEDURE = 8
    FUNCTION = 9
    PRINT = 10
    CALL = 11
    IF = 12
    IN = 13
    INOUT = 14
    NOT = 15
    SELECT = 16
    PROGRAM = 17
    OR = 18
    RETURN = 19
    WHILE = 20
    DEFAULT = 21
    IDENTIFIER = 100
    NUMBER = 101
    PLUS = 102
    MINUS = 103
    MULTIP = 104
    DIV = 105
    #COMPARISON = 106
    SMALLER = 106
    BIGGER = 107
    EQUAL = 108
    SMALLEREQUAL = 109
    BIGGEREQUAL = 110
    NOTEQUAL = 111 
    DELIMETR = 199#:=
    COLON = 200 
    SEMICOLON = 201#;
    COMMA = 202
    LEFTHOOK = 300
    RIGHTHOOK = 301
    LEFTPARENTHESIS = 302
    RIGHTPARENTHESIS = 303
    LEFTBRACKET = 304
    RIGHTBRACKET = 305
    COMMENTSEPERATOR = 400
    
def commit_lectical_unit(lexeme):
    if lexeme == "and":
        return Lectical_Unit.AND
    elif lexeme == "declare":
        return Lectical_Unit.DECLARE
    elif lexeme == "do":
        return Lectical_Unit.DO
    elif lexeme == "else":
        return Lectical_Unit.ELSE
    elif lexeme == "enddeclare":
        return Lectical_Unit.ENDDECLARE
    elif lexeme == "exit":
        return Lectical_Unit.EXIT
    elif lexeme == "procedure":
        return Lectical_Unit.PROCEDURE
    elif lexeme == "function":
        return Lectical_Unit.FUNCTION
    elif lexeme == "print":
        return Lectical_Unit.PRINT
    elif lexeme == "call":
        return Lectical_Unit.CALL
    elif lexeme == "if":
        return Lectical_Unit.IF
    elif lexeme == "in":
        return Lectical_Unit.IN
    elif lexeme == "inout":
        return Lectical_Unit.INOUT
    elif lexeme == "not":
        return Lectical_Unit.NOT
    elif lexeme == "select":
        return Lectical_Unit.SELECT
    elif lexeme == "program":
        return Lectical_Unit.PROGRAM
    elif lexeme == "or":
        return Lectical_Unit.OR
    elif lexeme == "return":
        return Lectical_Unit.RETURN
    elif lexeme == "while":
        return Lectical_Unit.WHILE
    elif lexeme == "default":
        return Lectical_Unit.DEFAULT
    else:
        return Lectical_Unit.IDENTIFIER

def commit_delimetrs_unit(lexeme):
    if lexeme == ';':
        delimetrs_found.append(lexeme)
        return Lectical_Unit.SEMICOLON
    elif lexeme == ',':
        delimetrs_found.append(lexeme)
        return Lectical_Unit.COMMA

def commit_groupingsymbols_unit(lexeme):
    if lexeme == '{':
        grouping_symbols_found.append(lexeme)
        return Lectical_Unit.LEFTHOOK
    elif lexeme == '}':
        grouping_symbols_found.append(lexeme)
        return Lectical_Unit.RIGHTHOOK
    elif lexeme == '(':
        grouping_symbols_found.append(lexeme)
        return Lectical_Unit.LEFTPARENTHESIS
    elif lexeme == ')':
        grouping_symbols_found.append(lexeme)
        return Lectical_Unit.RIGHTPARENTHESIS
    elif lexeme == '[':
        grouping_symbols_found.append(lexeme)
        return Lectical_Unit.LEFTBRACKET
    elif lexeme == ']':
        grouping_symbols_found.append(lexeme)
        return Lectical_Unit.RIGHTBRACKET

def commit_comparison_unit(lexeme):
    if lexeme == '<':
        return Lectical_Unit.SMALLER
    elif lexeme == '>':
        return Lectical_Unit.BIGGER
    elif lexeme == '<=':
        return Lectical_Unit.SMALLEREQUAL
    elif lexeme == '>=':
        return Lectical_Unit.BIGGEREQUAL
    elif lexeme == '<>':
        return Lectical_Unit.NOTEQUAL

def print_arrays(array):
        print (array)

def lexicAnalysis():
        global f2_position,line_number, wordid, numberid

        token = None
        while not token:
            character = f2.read(1)
            f2_position+= 1
            if character in white_operators:
                pass
            elif character == '\n':
                line_number+= 1
            elif character.isalpha():
                move_f2position()
                lexeme = read_identifier()
                if lexeme == '':
                    continue 
                if lexeme in keywords:
                    keywords_found.append(lexeme)
                else:
                    identifiers_found.append(lexeme)
                token = commit_lectical_unit(lexeme)
                wordid = lexeme
            elif character.isdigit():
                move_f2position()
                lexeme = read_number()
                if lexeme == '':
                    continue
                numbers_found.append(lexeme)
                if check_number(int(lexeme)):
                      token = Lectical_Unit.NUMBER
                      numberid = lexeme
                else:
                      print("The number %d is not suported!" % (lexeme))
                      sys.exit(0)
            elif character in numeric_operators:
                if character == '+':
                    token = Lectical_Unit.PLUS
                elif character == '-':
                    token = Lectical_Unit.MINUS
                elif character == '*':
                    token = Lectical_Unit.MULTIP
                elif token == '/':
                    token = Lectical_Unit.DIV
            elif character == '<':
                lexeme = read_comparison(character)
                comparisons_found.append(lexeme)
                token = commit_comparison_unit(lexeme)
            elif character == '>':
                lexeme = read_comparison(character)
                comparisons_found.append(lexeme)
                token = commit_comparison_unit(lexeme)
            elif character == '=':
                token = Lectical_Unit.EQUAL
            elif character == ':':
                character = f2.read(1)
                f2_position+= 1
                if character == '=':
                    token = Lectical_Unit.DELIMETR
                else:
                    move_f2position()
                    token = Lectical_Unit.COLON          
            elif character in delimetrs:
                token = commit_delimetrs_unit(character)
            elif character in grouping_symbols:
               token = commit_groupingsymbols_unit(character)
            elif character == '\\':
                character = f2.read(1)
                f2_position+= 1
                if character == '*':
                    character = f2.read(1)
                    f2_position+= 1
                    while (character):
                        if character == '*':
                            character = f2.read(1)
                            f2_position+= 1
                            if character == '\\':
                                break
                        else:
                            character = f2.read(1)
                            f2_position+= 1
                            continue
                    else:
                        print("error: The f2 ended without end of comment")
                        sys.exit(0)
                else:
                    print("error: wrong viariable: comments started with '\*'")
                    sys.exit(0)
            elif character == EOF:
                #print("The f2 come to an end")
                token = Lectical_Unit.EOF
                #sys.exit(0)
            else:
                print("unrecognized symbol!")
                sys.exit(0)
        return token

'''''''''Functions for intermidiate code'''''''''
'''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''

def newTemp():
    global tempVarCount
    tempVarCount += 1
    return  tempBaseName + str(tempVarCount)

def incrementQuad(functionName):
    global quad, nextquad
    quad[functionName] = nextquad[functionName]
    nextquad[functionName] += 1
    return quad[functionName]

def nextQuad(functionName):
    return nextquad[functionName]

def genQuad(functionName, op, tel1, tel2, dest):
    global fullCode
    incrementQuad(functionName)
    fullCode[functionName].append([str(quad[functionName]) + ": " + op, tel1, tel2, dest])

def emptyList():
    newList = list()
    return newList


def makeList(arg):
    newList = list()
    newList.append(arg)
    return newList

def merge(list1, list2):
    return list1+list2

def backpatch(functionName, List, z):
    global fullCode
    for quad in List:
        fullCode[functionName][quad][3] = z

def printFullCode():
    for functionName in fullCode.keys():
        print(functionName + ":")
        for element in range(len(fullCode[functionName])):
            print(fullCode[functionName][element])

def printQuads():
    global quads
    for name in fullCode.keys():
        for quad in range(len(fullCode[name])):
            quads.append(fullCode[name][quad])
    for element in range(len(quads)-1, 0, -1):
         for i in range(element):
            Previus = int("".join(re.findall('\d+', quads[i][0])))
            Next = int("".join(re.findall('\d+', quads[i+1][0])))
            if  Previus > Next:
                temp = quads[i]
                quads[i] = quads[i+1]
                quads[i+1] = temp
    for quad in range(len(quads)):
        print(",".join(quads[quad]))
    

def createNewCode(functionName):
    global fullCode, quad, nextquad, labelNum
    fullCode[functionName] = list()
    quad[functionName] = -1
    nextquad[functionName] = labelNum

def changeQuads(quads):
    global changedQuads
    changedQuads = quads[:]
    for quad in range(len(changedQuads)):
        for character in [':','_']:
            if character in changedQuads[quad]: 
                newquad = ",".join(changedQuads[quad]).replace(character,'')
                changedQuads[quad] = newquad.split(",")

                

def writeInf2(f2Name):
    global tempLabCount, quads
    changeQuads(quads)
    name = f2Name.split(".")
    name = name[0]
    name1 = name + ".int"
    name2 = name + ".c"
    try:
        f21 = open(name1,"w")
        f22 = open(name2,"w")
    except (OSError,IOError):
        print("The f2 %s does not exist!" % f2Name)
        sys.exit()
    for quad in quads:
        f21.write(",".join(quad) + "\n")
    f21.close()
    for quad in changedQuads:
        if ":=" in quad[0]:
            tempLabCount += 1
            label = tempLabName + str(tempLabCount)
            f22.write(label + ": " + quad[3] + "=" + quad[1]
                        + ";" + "//(" + ",".join(quad) + ")" + "\n")
        elif "+" in quad[0] or "-" in quad[0] or "*" in quad[0] or "/" in quad[0]:
            tempLabCount += 1
            label = tempLabName + str(tempLabCount)
            f22.write(label + ": " + quad[3] + "=" + quad[1] + quad[0] + quad[2]
                        + ";" + "//(" + ",".join(quad) + ")" + "\n")
        elif "=" in quad[0] or "<" in quad[0] or ">" in quad[0] or "<>" in quad[0] or "<=" in quad[0] or ">=" in quad[0]:
            tempLabCount += 1
            label = tempLabName + str(tempLabCount)
            f22.write(label + ": " + "if " + "(" + quad[1] + quad[0] + quad[2] + ")"
                        + "goto" + tempLabName + quad[3] + ";" + "//(" + ",".join(quad)
                        + ")" + "\n")
        elif "jump" in quad[0]:
            tempLabCount += 1
            label = tempLabName + str(tempLabCount)
            f22.write(label + ": " + "goto" + tempLabName + quad[3] + ";" + "//("
                        + ",".join(quad) + ")" + "\n")
        
    f22.close()
    

'''''''''''function for semantic analysis'''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def checkReturns():
	retListF = list()
	retListP = list()
	for functionName in counterFunRet.keys():
		if len(counterFunRet[functionName]) < 1:
			retListF.append(functionName)
	for procedureName in counterProcRet.keys():
		if len(counterProcRet[procedureName]) > 0:
			retListP.append(procedureName)
	for functionName in retListF:
		print("the FUNCTION %s should contain at least one 'return'" % functionName)
	for procedureName in retListP:
		print("the PROCEDURE %s should not contain the keyword 'return' " % procedureName)
	if len(retListF) or len(retListP) > 0:
		sys.exit(0)    
        
        
    
    

''''''''''' functions for symbol table'''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''
def searchin(identifier):
    global scopeStack
    return searchinScopeStack(identifier, len(scopeStack) - 1)

def searchinScopeStack(identifier, position):
    global scopeStack
    if position == -1:
        return None
    scope = scopeStack[position]
    #ama den eini se auto to scope isws einai ston gonea
    if identifier in scope:
        return scope[identifier]
    else:
        return searchinScopeStack(identifier, position - 1)

def getCurrentScope():
    global scopeStack
    return scopeStack[len(scopeStack) - 1]["scopeName"]

def addScope(scopeName, functionType, nestingLevel):
    global scopeStack
    currentScope = scopeStack[len(scopeStack) - 1]
    newScope = {
                                "scopeName"     : scopeName,
                                "parentName"    : currentScope["scopeName"],
                                "type"          : functionType,
                                "returnType"    : "UNKNOWN",
								"nestingLevel"	: nestingLevel
                            }
    scopeStack.append(newScope)
    stackOffset.append(12)
    #functionList[scopeName] = currentScope[scopeName]

def addEntity(identifier, identifierType):
    global scopeStack
    currentScope = scopeStack[len(scopeStack) - 1]
    currentOffset = stackOffset.pop()
    if not identifier in currentScope:
        currentScope[identifier] = dict()
    if identifierType == "FUNCTION" or identifierType == "PROCEDURE":
         currentScope[identifier]["type"] = identifierType
         currentScope[identifier]["listOfArguments"] = list()
         currentScope[identifier]["startQuad"] = 0
         currentScope[identifier]["frameLength"] = 0
    else:
        currentScope[identifier]["offset"] = currentOffset
        currentScope[identifier]["type"] = identifierType
   
    stackOffset.append(currentOffset + 4)
    
def getEntity(scope, offset):
    for element in scope:
        if type(scope.get(element)) is dict:
            if element["offset"] == offset:
                return scope.get(element)
    
def addEntityAttr(identifier, key, value):
    ident = searchin(identifier)
    ident[key] = value

def getEntityAttr(identifier, key):
    ident = searchin(identifier)
    if key in ident:
        return ident[key]
    else:
        return None

def addEntityAttrToCurrentScope(identifier, key, value):
    global scopeStack
    currentScope = scopeStack[len(scopeStack) - 1]
    currentScope[identifier][key] = value

def addEntityArgToPreviusScope(identifier, key, value):
    global scopeStack
    currentScope = scopeStack[len(scopeStack) - 2]
    if key == "listOfArguments":
        currentScope[identifier][key].append(value)
    else:
        currentScope[identifier][key] = value
   
    
def getEntityAttrFromCurrentScope(identifier, key):
    global scopeStack
    currentScope = scopeStack[len(scopeStack) - 1]
    return currentSCope[identifier][key]

def identifierExists(identifier, nestinglevel):
	scopeList = list()
	for scope in scopeStack:
		if scope["nestingLevel"] == nestinglevel:
			if identifier in scope:
				return True
	return False

def identifierExistsInCurrentScope(identifier):
	currentScope = scopeStack[len(scopeStack) - 1]
	if identifier in currentScope:
		return True
	return False

def deleteCurrentScope():
    global scopeStack, stackHistory
    currentScope = scopeStack.pop()
    stackHistory.append(currentScope)


def printScopeStack():
    for x in stackHistory:
        print(x)
        print("|")

    
def printSymbolTable():
    print("SYMBOL TABLE \n")
    print("*************")
    for element in stackHistory:
        print("Scope: \n" + element["scopeName"])
        print("********************************")
        pprint.pprint(element)
        print("********************************")

''''''''''''''''''''''''''''''''''''''''''''''''''
'''functions for Final Code'''''''''''''''''''''''

def getScope(identifier):
    global scopeStack
    return searchinStack(identifier, len(scopeStack) - 1)

def searchinStack(identifier, position):
    global scopeStack
    if position == -1:
        return None
    scope = scopeStack[position]
    if identifier in scope:
        return scope
    else:
        return searchinStack(identifier, position - 1)

def getScopeAttribute(scope, attribute):
	return scope[attribute]

def gnlvcode(variable):
	global finalCode
	scope = getScope(variable)
	tempNestingLevel = getScopeAttribute(scope, "nestingLevel")
	finalCode.write("movi R[255], M[R[0] + 4]")
	for nestlevel in range(0, tempNestingLevel -1):
		finalCode.write("movi R[255], M[R[255] + 4]")
	finalCode.write("movi R[254]," + offset)
	finalCode.write("addi R[255], R[255], R[254]")

def loadvr(variable, register):
	global finalCode
	scope = getScope(variable)
	tempNestingLevel = getScopeAttribute(scope, "nestingLevel")
	if nestingLevel == 0:
		firstScope = scopeStack[1]
		offset = firstScope[variable]["offset"]
		finalCode.write("movi R["+ register +"], M["+(600+offset)+ "]")
	elif nestingLevel == tempNestingLevel:
		scope = scopeStack[nestingLevel + 1]
		offset = scope[variable]["offset"]
		entity = getEntity(scope, (offset-12)/4)
		if  "parMode" not in entity:
                        finalCode.write("movi R["+ register +"], M[R[0] +"+ offset + "]");
		elif "parMode" in entity:
			if entity["parMode"] == "in":
				finalCode.write("movi R["+ register +"], M[ R[0] +" + offset + "]")
			else:
				finalCode.write("movi R[255], M[ R[0] +" + offset + "]")
				finalCode.write("movi R[" + register + "], M[R[255]]")
	else:
		gnlvcode(variable)
		scope = scopeStack[nestingLevel + 1]
		offset = scope[variable]["offset"]
		entity = getEntity(scope, (offset-12)/4)
		if  "parMode" not in entity:
                        finalCode.write("movi R["+ register +"], M[R[255]]")
		elif "parMode" in entity:
			if entity["parMode"] == "in":
				finalCode.write("movi R["+ register +"], M[R[255]]")
			else:
				finalCode.write("movi R[255], M[R[255]]")
				finalCode.write("movi R[" + register + "], M[R[255]]")

def storevr(variable, register):
	global finalCode
	scope = getScope(variable)
	tempNestingLevel = getScopeAttribute(scope, "nestingLevel")
	if nestingLevel == 0:
		firstScope = scopeStack[1]
		offset = firstScope[variable]["offset"]
		finalCode.write("movi M["+(600+offset)+ "], R["+ register +"]")
	elif nestingLevel == tempNestingLevel:
		scope = scopeStack[nestingLevel + 1]
		offset = scope[variable]["offset"]
		entity = getEntity(scope, (offset-12)/4)
		if  "parMode" not in entity:
                        finalCode.write("movi M[R[0] +"+ offset + "], R["+ register +"]");
		elif "parMode" in entity:
			if entity["parMode"] == "in":
				finalCode.write("movi M[R[0] +", + offset + "], R["+ register +"]")
			else:
				finalCode.write("movi R[255], M[ R[0] +" + offset + "]")
				finalCode.write("movi M[R[255]], R["+ register +"]")
	else:
		gnlvcode(variable)
		scope = scopeStack[nestingLevel + 1]
		offset = scope[variable]["offset"]
		entity = getEntity(scope, (offset-12)/4)
		if  "parMode" not in entity:
                        finalCode.write("movi R["+ register +"], M[R[255]]")
		elif "parMode" in entity:
			if entity["parMode"] == "in":
				finalCode.write("movi M[R[255]], R["+ register +"]")
			else:
				finalCode.write("movi R[255], M[R[255]]")
				finalCode.write("movi M[R[255]], R["+ register +"]")
	
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def program():
    global token, wordid
    token = lexicAnalysis()
    if token == Lectical_Unit.PROGRAM:
        token = lexicAnalysis()
        if token == Lectical_Unit.IDENTIFIER:
            programName = wordid
            createNewCode(programName)
            token = lexicAnalysis()
            addScope(programName, "PROGRAMM", nestingLevel)
            block(programName, 1)
            checkReturns()
            while token != Lectical_Unit.EOF:
                token = lexicAnalysis()
            else:
                print("the f2 come to an and!")
                
        else:
            print("error:An Identifier was expected in line %d" % line_number)
            sys.exit(0) 
    else:
        print("the Keyword 'program' was expected in line %d" % line_number)
        sys.exit(0)

def block(name, main):
    global token, labelNum, nestingLevel
    if token == Lectical_Unit.LEFTHOOK:
        token = lexicAnalysis()
        declarations(name)
        subprograms(name)
        nextquad[name] = labelNum #h prwth 
        genQuad(name,"begin_block", name, "_", "_")
        firstLabels[name] = labelNum
        if main != 1:
            addEntityAttr(name, "startQuad", firstLabels[name])       
        labelNum += 1
        sequence(name, None)
        if main == 1:#gia na doume pote teleiwnei to arxiko programma
            genQuad(name, "halt", "_", "_", "_")
        genQuad(name, "end_block", name, "_", "_")
        labelNum += 1
        print(token)
        if token == Lectical_Unit.RIGHTHOOK:            
            token = lexicAnalysis()           
        else:
            print("the symbol '}' is expected at the end of a block. line %d" % line_number)
            sys.exit(0)
    else:
        print("the symbol '{' is expected at the beggining of a block. line %d" % line_number)  
        sys.exit(0)    
        
        #frameLength = 0
        #addEntityArgToCurrentScope(name, "frameLenhth", frameLength)
    deleteCurrentScope()
    nestingLevel -= 1
    
    

def declarations(name):
    global token
    if token == Lectical_Unit.DECLARE:
        token = lexicAnalysis()
        varlist(name)
        if token == Lectical_Unit.ENDDECLARE:
            token = lexicAnalysis()
        else:
            print("the Keyword 'enddeclare' was expected in line %d" % line_number)
            sys.exit(0)

def varlist(name):
	global token
	if token == Lectical_Unit.IDENTIFIER:
		if identifierExists(wordid, nestingLevel):
			print("the variable %s has already be declared in function %s" % (wordid, name))
			sys.exit(0)
		addEntity(wordid, "int")
		token = lexicAnalysis()
		while token == Lectical_Unit.COMMA:
			token = lexicAnalysis()
			if token == Lectical_Unit.IDENTIFIER:
				if identifierExists(wordid, nestingLevel):
					print("the variable %s has already be declared in function %s" % (wordid, name))
					sys.exit(0)
				addEntity(wordid, "int")
				token = lexicAnalysis()
			else:
				print("an Identifier name was expected in line %d" % line_number)
				sys.exit(0)
        
        
def subprograms(name):
    global token
    while(token == Lectical_Unit.PROCEDURE or token == Lectical_Unit.FUNCTION):
        #token = lexicAnalysis()
        func(name)

def func(name):
    global token,procedureName, functionName, nestingLevel
    if token == Lectical_Unit.PROCEDURE:
        token = lexicAnalysis()
        if token == Lectical_Unit.IDENTIFIER:
            procedureName = wordid
            if identifierExists(procedureName, nestingLevel):
                print("the procedure %s has already been declared" % procedureName)
                sys.exit(0)
            counterProcRet[procedureName] = list()
            createNewCode(procedureName)
            addEntity(procedureName, "PROCEDURE")
            nestingLevel += 1
            addScope(procedureName, "PROCEDURE", nestingLevel)
            token = lexicAnalysis()
            funcbody(procedureName)
        else:
            print("an Identifier was expected in line %d" % line_number)
            sys.exit(0)
    elif token == Lectical_Unit.FUNCTION:
        token = lexicAnalysis()
        if token == Lectical_Unit.IDENTIFIER:
            functionName = wordid
            if identifierExists(functionName, nestingLevel):
                print("the function %s has already been declared" % functionName)
                sys.exit(0)
            counterFunRet[functionName] = list()
            createNewCode(functionName)
            addEntity(functionName, "FUNCTION")
            nestingLevel += 1
            addScope(functionName, "FUNCTION", nestingLevel)
            token = lexicAnalysis()
            funcbody(functionName)
        else:
            print("an Identifier was expected in line %d" % line_number)
            sys.exit(0)

def funcbody(name):
    formalpars(name)
    block(name,0)

def formalpars(name):
    global token
    if token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        formalparlist(name)
        if token == Lectical_Unit.RIGHTPARENTHESIS:
            token = lexicAnalysis()
        else:
            print("the symbol ')' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        print("the symbol '(' was expected in line %d" % line_number)
        sys.exit(0)

def formalparlist(name):
    global token
    formalparitem(name)
    while token == Lectical_Unit.COMMA:
        token = lexicAnalysis()
        formalparitem(name)

def formalparitem(name):
    global token
    if token == Lectical_Unit.IN:
        token = lexicAnalysis()
        if token == Lectical_Unit.IDENTIFIER:
            newDict = {"argumentName"   : wordid, "parMode"  : "in"}
            addEntityArgToPreviusScope(name, "listOfArguments", newDict)
            #addEntityArgToCurrentScope(name, "argumentName", wordid)
            addEntity(wordid, "int")
            addEntityAttrToCurrentScope(wordid, "parMode", "in")
            token = lexicAnalysis()
        else:
            print("an Identifier was expected in line %d" % line_number)
            sys.exit(0)
    elif token == Lectical_Unit.INOUT:
        token = lexicAnalysis()
        if token == Lectical_Unit.IDENTIFIER:
            newDict = {"argumentName"   : wordid, "parMode"  : "inout"}
            addEntityArgToPreviusScope(name, "listOfArguments", newDict)
            addEntity(wordid, "int")
            addEntityAttrToCurrentScope(wordid, "parMode", "inout")
            token = lexicAnalysis()
        else:
            print("an Identifier was expected in line %d" % line_number)
            sys.exit(0)
            
def sequence(name, exitList):
    global token
    statement(name, exitList)     
    while token == Lectical_Unit.SEMICOLON:
            token = lexicAnalysis()
            statement(name, exitList)
           
def brackets_seq(name, exitList):
    sequence(name, exitList)

def brack_or_stat(name, exitList):
    global token
    if token == Lectical_Unit.LEFTHOOK:
        token = lexicAnalysis()
        brackets_seq(name, exitList)
        if token == Lectical_Unit.RIGHTHOOK:
            token = lexicAnalysis()
        else:
            print("the symbol '}' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        statement(name, exitList)
        print(token)
        if token == Lectical_Unit.SEMICOLON:
            token = lexicAnalysis()

def statement(name, exitList):
    global token
    if token == Lectical_Unit.IDENTIFIER:
        token = lexicAnalysis()
        assignment_stat(name)
        if token != Lectical_Unit.SEMICOLON:
            print("; was expected in line %d" % line_number)
            sys.exit(0)
    elif token == Lectical_Unit.IF:
        token = lexicAnalysis()
        if_stat(name, exitList)
    elif token == Lectical_Unit.DO:
        token = lexicAnalysis()
        do_while_stat(name)
    elif token == Lectical_Unit.WHILE:
        token = lexicAnalysis()
        while_stat(name)
    elif token == Lectical_Unit.SELECT:
        token  = lexicAnalysis()
        select_stat(name)
    elif token == Lectical_Unit.EXIT:
        token = lexicAnalysis()
        exit_stat(name)
        if token != Lectical_Unit.SEMICOLON:
            print("; was expected in line %d" % line_number)
            sys.exit(0)
    elif token == Lectical_Unit.RETURN:
        if name in counterFunRet:
            counterFunRet[name].append("return")
        if name in counterProcRet:
            counterProcRet[name].append("return")
        token = lexicAnalysis()
        return_stat(name)
        if token != Lectical_Unit.SEMICOLON:
            print("; was expected in line %d" % line_number)
            sys.exit(0)
        if token != Lectical_Unit.SEMICOLON:
            print("; was expected in line %d" % line_number)
            sys.exit(0)
    elif token == Lectical_Unit.PRINT:
        token = lexicAnalysis()
        print_stat(name)
        if token != Lectical_Unit.SEMICOLON:
            print("; was expected in line %d" % line_number)
            sys.exit(0)
    elif token == Lectical_Unit.CALL:
        token = lexicAnalysis()
        call_stat(name)
        if token != Lectical_Unit.SEMICOLON:
            print("; was expected in line %d" % line_number)
            sys.exit(0)
        
def assignment_stat(name):
    global token, wordid, labelNum
    identifier = wordid
    if token == Lectical_Unit.DELIMETR:
        token = lexicAnalysis()
        Eplace = expression(name)
        genQuad(name, ":=", Eplace, "_", identifier)
        labelNum += 1
    else:
        print("the symbol ':=' was expected in line %d" % line_number)
        sys.exit(0)
    
def if_stat(name, exitList):
    global token, labelNum
    if token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        Btrue = emptyList()
        Bfalse = emptyList()
        ifExitList = emptyList()
        Btrue, Bfalse = condition(name, Btrue, Bfalse)
        if token == Lectical_Unit.RIGHTPARENTHESIS:
            backpatch(name, Btrue, str(nextQuad(name)))
            token = lexicAnalysis()
            brack_or_stat(name, exitList)
            label = nextQuad(name)
            genQuad(name, "jump", "_", "_", "_")
            labelNum += 1
            ifExitList.append(label)
            backpatch(name, Bfalse, str(nextQuad(name)))
            elsepart(name, exitList)
            backpatch(name, ifExitList, str(nextQuad(name)))
        else:
            print("the symbol ')' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        print("the symbol '(' was expected in line %d" % line_number)
        sys.exit(0)
        
def elsepart(name, exitList):
    global token
    if token == Lectical_Unit.ELSE:
        token = lexicAnalysis()
        brack_or_stat(name, exitList)

def while_stat(name):
    global token, labelNum
    startquad = str(nextQuad(name))
    if token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        Condtrue = emptyList()
        Condfalse = emptyList()
        exitList = emptyList()
        Condtrue, Condfalse = condition(name, Condtrue, Condfalse)
        if token == Lectical_Unit.RIGHTPARENTHESIS:
            token = lexicAnalysis()
            backpatch(name, Condtrue, str(nextQuad(name)))
            brack_or_stat(name, exitList)
            #labelNum = nextQuad(name)
            genQuad(name, "jump", "_", "_", startquad)
            labelNum += 1
            backpatch(name, Condfalse, str(nextQuad(name)))
            backpatch(name, exitList, str(nextQuad(name)))   
        else:
            print("the symbol ')' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        print("the symbol '(' was expected in line %d" % line_number)
        sys.exit(0)

def select_stat(name):
    global token, selectCounter
    ExitList = emptyList()
    if token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        if token == Lectical_Unit.IDENTIFIER:
            id1place = wordid
            token = lexicAnalysis()
            if token == Lectical_Unit.RIGHTPARENTHESIS:
                token = lexicAnalysis()
                while token == Lectical_Unit.NUMBER:
                    id2place = numberid
                    if int(numberid) != selectCounter:
                        print("wrong constant at select in line %d. was expected %d but it was %d" % (line_number, selectCounter, int(numberid)))
                    selectCounter += 1
                    token = lexicAnalysis()
                    if token == Lectical_Unit.COLON:
                        t = makeList(str(nextQuad))
                        genQuad(name, "<>", id1place, id2place, "_")
                        token = lexicAnalysis()
                        brack_or_stat(name, ExitList)  
                        e = makeList(str(nextQuad))
                        genQuad(name, "jump", "_", "_", "_")
                        ExitList = merge(ExitList, e)
                        backpatch(name, ExitList, str(nextQuad))             
                    else:
                        print("the symbol ':'  was expected in line %d" % line_number)
                        sys.exit(0)
                print(token)
                if token == Lectical_Unit.DEFAULT:
                    token = lexicAnalysis()
                    if token == Lectical_Unit.COLON:
                        token = lexicAnalysis()
                        brack_or_stat(name, ExitList)
                        backpatch(name, ExitList, str(nextQuad))
                    else:
                        print("the symbol ':'  was expected in line %d" % line_number)
                        sys.exit(0)
                else:
                    print("the Keyword 'default' was expected in line %d" % line_number)
                    sys.exit(0)
                    
            else:
                print("the symbol ')' was expected in line %d" % line_number)
                sys.exit(0)
        else:
            print("an Identifier was expected in line %d" % line_number)
            sys.exit(0)
    else:
        print("the symbol '(' was expected in line %d" % line_number)
        sys.exit(0)

def do_while_stat(name):
    global token, checkExit
    checkExit = True # mono h do while alalzei thn metavlhth checkExit gia an legxoum an to exit p tha vroume einai apthn do while
    exitList = emptyList()
    startquad = str(nextQuad(name))
    brack_or_stat(name, exitList)
    print(token)
    if token == Lectical_Unit.WHILE:
        token = lexicAnalysis()
        if token == Lectical_Unit.LEFTPARENTHESIS:
            token = lexicAnalysis()
            Condtrue = emptyList()
            Condfalse = emptyList()
            Condtrue, Condfalse = condition(name, Condtrue, Condfalse)
            if token == Lectical_Unit.RIGHTPARENTHESIS:
                token = lexicAnalysis()
                backpatch(name, Condtrue, startquad)
                backpatch(name, Condfalse, str(nextQuad(name)))
                backpatch(name, exitList, str(nextQuad(name)))
            else:
                print("the symbol ')' was expected in line %d" % line_number)
                sys.exit(0)
        else:
            print("the symbol '(' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        print("the Keyword 'while1' was expected in line %d" % line_number)
        sys.exit(0)
            
def exit_stat(name):
    global token, labelNum, checkExit
    if checkExit == False:
        print("a keyword 'exit found outside of a do-while loop in line %d" % line_number)
        sys.exit(0)
    if token == Lectical_Unit.EXIT:
        
        token = lexicAnalysis()
        Exit = makeList(nextQuad(name))
        genQuad(name, "jump", "_", "_", "_")
        labelNum += 1
        return Exit
    else:
        print("the Keyword 'exit' was expected in line %d" % line_number)
        sys.exit(0)
    
def return_stat(name):
    global token, labelNum
    print(token)
    if token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        Eplace = expression(name)
        genQuad(name, "ret", Eplace, "_", "_")
        labelNum += 1
        if token == Lectical_Unit.RIGHTPARENTHESIS:
            token = lexicAnalysis()
        else:
            print("the symbol ')' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        print("the symbol '(' was expected in line %d" % line_number)
        sys.exit(0)

def print_stat(name):
    global token, labelNum
    if token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        Eplace = expression(name)
        genQuad(name, "out", Eplace, "_", "_")
        labelNum = nextQuad(name)
        
        if token == Lectical_Unit.RIGHTPARENTHESIS:
            token = lexicAnalysis()
        else:
            print("the symbol ')' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        print("the symbol '(' was expected in line %d" % line_number)
        sys.exit(0)

def call_stat(name):
    global token
    if token == Lectical_Unit.IDENTIFIER:
        idname = wordid
        token = lexicAnalysis()
        actualpars(name, idname)
    else:
        print("an Identifier was expected for a call functio in line %d" % line_number)
        sys.exit(0)
       
def actualpars(callerFunction, funcName):
    global token, labelNum
    returnVar = ""
    if token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        returnVar = actualparlist(callerFunction, funcName)
        #labelNum = nextQuad(callerFunction)
        genQuad(callerFunction, "call", funcName, "_", "_" )
        labelNum += 1
        if token == Lectical_Unit.RIGHTPARENTHESIS:
            token = lexicAnalysis()
        else:
            print("the symbol ')' was expected in line %d" % line_number)
            sys.exit(0)
    return returnVar

def actualparlist(callerFunction, funcName):
    global token, labelNum
    actualparitem(callerFunction, funcName)
    while token == Lectical_Unit.COMMA:
        token = lexicAnalysis()
        actualparitem(callerFunction, funcName)
    returnVar = newTemp()
    addEntity(returnVar, "int")
    genQuad(callerFunction, "par", returnVar, "RET", "_")
    labelNum += 1
    return returnVar
                 
def actualparitem(callerFunction, funcName):
    global token, labelNum
    if token == Lectical_Unit.IN:
        token = lexicAnalysis()
        place = expression(callerFunction)
        genQuad(callerFunction, "par", place, "CV", "_")
        labelNum += 1
    elif token == Lectical_Unit.INOUT:
        token = lexicAnalysis()
        if token == Lectical_Unit.IDENTIFIER:
            genQuad(callerFunction, "par", wordid, "REF", "_")
            labelNum += 1
            token = lexicAnalysis()
        else:
            print("an Identifier was expected in line %d" % line_number)
            sys.exit(0)
            
def condition(name, BtrueList, BfalseList):
    global token
    boolterm_true = emptyList()
    boolterm_false = emptyList()
    boolterm_true, boolterm_false = boolterm(name, boolterm_true, boolterm_false)
    BtrueList.extend(boolterm_true)
    BfalseList.extend(boolterm_false)
    while token == Lectical_Unit.OR:
        boolterm1_true = emptyList()
        boolterm1_false = emptyList()
        backpatch(name, BfalseList, str(nextQuad(name)))
        token = lexicAnalysis()
        boolterm1_true, boolterm1_false = boolterm(name, boolterm1_true, boolterm1_false)
        BtrueList = merge(BtrueList, boolterm1_true)
        BfalseList.extend(boolterm1_false)
    return BtrueList, BfalseList
             
def boolterm(name, boolterm_trueList, boolterm_falseList):
    global token
    boolfactor_true = emptyList()
    boolfactor_false = emptyList()
    boolfactor_true, boolfactor_false = boolfactor(name, boolfactor_true, boolfactor_false)
    boolterm_trueList.extend(boolfactor_true)
    boolterm_falseList.extend(boolfactor_false)
    while token == Lectical_Unit.AND:
        boolfactor_true1 = emptyList()
        boolfactor_false1 = emptyList()
        backpatch(name, boolterm_trueList, str(nextQuad(name)))
        token = lexicAnalysis()
        boolfactor_true1, boolfactor_false1 = boolfactor(name, boolfactor_true1, boolfactor_false1)
        boolterm_trueList.extend(boolfactor_true1)
        boolterm_falseList = merge(boolterm_falseList, boolfactor_false1)
    return boolterm_trueList, boolterm_falseList
                 
def boolfactor(name, boolterm_true, boolterm_false):
    global token, labelNum
    if token == Lectical_Unit.NOT:
        token = lexicAnalysis()
        if token == Lectical_Unit.LEFTBRACKET:
            token = lexicAnalysis()
            Btrue = emptyList()
            Bfalse = emptyList()
            Btrue, Bfalse = condition(name, Btrue, Bfalse)
            boolterm_true.extend(Btrue)
            boolterm_false.extend(Bfalse)
            if token == Lectical_Unit.RIGHTBRACKET:
                token = lexicAnalysis()
            else:
                print("the symbol ']' was expected in line %d" % line_number)
                sys.exit(0)
        else:
            print("the symbol '[' was expected in line %d" % line_number)
        
    elif token == Lectical_Unit.LEFTBRACKET:
        token = lexicAnalysis()
        Btrue = emptyList()
        Bfalse = emptyList()
        Btrue, Bfalse = condition(name, Btrue, Bfalse)
        boolterm_true.extend(Btrue)
        boolterm_false.extend(Bfalse)
        if token == Lectical_Unit.RIGHTBRACKET:
            token = lexicAnalysis()
        else:
            print("the symbol ']' was expected in line %d" % line_number)
            sys.exit(0)
    else:
        
        E1place = expression(name)
        relop = relational_oper(name)
        E2place = expression(name)
        trueList = makeList(nextQuad(name))
        genQuad(name, relop, E1place, E2place, "_")
        labelNum += 1
        falseList = makeList(nextQuad(name))
        genQuad(name, "jump", "_", "_", "_")
        labelNum += 1
        boolterm_true = merge(boolterm_true, trueList)
        boolterm_false = merge(boolterm_false, falseList)
    return   boolterm_true, boolterm_false  

def expression(name):
    global token, labelNum
    sign = optional_sign(name)
    T1place = sign + term(name)
    while token == Lectical_Unit.PLUS or token == Lectical_Unit.MINUS:
        addOp = add_oper(name)
        T2place = term(name)
        tempVar = newTemp()
        addEntity(tempVar, "int")
        genQuad(name, addOp, T1place, T2place, tempVar)
        labelNum += 1
        T1place = tempVar
    
    return T1place    
    
def term(name):
    global token, labelNum
    F1place = factor(name)
    while token == Lectical_Unit.MULTIP or token == Lectical_Unit.DIV:
        mulOp = mul_oper(name)
        F2place = factor(name)
        tempVar = newTemp()
        addEntity(tempVar, "int")
        genQuad(name, mulOp, F1place, F2place, tempVar)
        labelNum += 1
        F1place = tempVar
        
    return F1place

def factor(name):
    global token
    if token == Lectical_Unit.NUMBER:
        number = numberid
        token = lexicAnalysis()
        return number
    elif token == Lectical_Unit.LEFTPARENTHESIS:
        token = lexicAnalysis()
        place = expression(name)
        if token == Lectical_Unit.RIGHTPARENTHESIS:
            token = lexicAnalysis()
            return place
        else:
            print("the symbol ')' was expected in line %d" % line_number)
            sys.exit(0)
    elif token == Lectical_Unit.IDENTIFIER: 
        idname = wordid
        token = lexicAnalysis()
        result = idtail(name, idname)
        if result != "":
            return result
        return idname
    else:
        print(" line %d error:something was expected here" % line_number)
        sys.exit(0)

def idtail(name, idname):
    if token == Lectical_Unit.LEFTPARENTHESIS:
        return actualpars(name, idname)
    return ""

def relational_oper(name):
    global token
    if token == Lectical_Unit.SMALLER:
        
        token = lexicAnalysis()
        return "<"
    elif token == Lectical_Unit.BIGGER:
        token = lexicAnalysis()
        return ">"
    elif token == Lectical_Unit.EQUAL:
        token = lexicAnalysis()
        return "="
    elif token == Lectical_Unit.SMALLEREQUAL:
        token = lexicAnalysis()
        return "<="
    elif token == Lectical_Unit.BIGGEREQUAL:
        token = lexicAnalysis()
        return ">="
    elif token == Lectical_Unit.NOTEQUAL:
        token = lexicAnalysis()
        return "<>"
    else:
        print("a comparison was expected in line %d" % line_number)
        sys.exit(0)
        
def add_oper(name):
    global token
    if token == Lectical_Unit.PLUS:
        token = lexicAnalysis()
        return "+"
    elif token == Lectical_Unit.MINUS:
        token = lexicAnalysis()
        return "-"
    else:
        print(" an add_operator (+/-) was expected in line %d" % line_number)
        sys.exit(0)
        

def mul_oper(name):
    global token
    if token == Lectical_Unit.MULTIP:
        token = lexicAnalysis()
        return "*"
    elif token == Lectical_Unit.DIV:
        token = lexicAnalysis()
        return "/"
    else:
        print(" an mul_operator (* or /) was expected in line %d" % line_number)
        sys.exit(0)
        

def optional_sign(name):
    global token
    if token == Lectical_Unit.PLUS or token == Lectical_Unit.MINUS:
        return add_oper(name)
    '''
    elif token == Lectical_Unit.MULTIP or token == Lectical_Unit.DIV:
        print("error: wrong numeric operator in line %d" % line_number)
        sys.exit(0)
    '''
    return ""
       
def main():

	
    program()
    print("parse completed succesfully")
    printFullCode()
    print("\n")
    printQuads()
    writeInf2(f1)
    printSymbolTable()
    printScopeStack()
    print(firstLabels)
    
   
    
if __name__ == "__main__":
        main()    
    
    
 



    
        
    
    
    
    
        
