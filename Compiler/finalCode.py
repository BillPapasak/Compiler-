''' uparxoun sto lexicAndSyntaxAnalysis.py alla den xrhsimopoiountai'''

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
	
	
			
                        
		
		
		
		
		

	
		
			
			
	
	
	

