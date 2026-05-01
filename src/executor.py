# executor.py
# @brief :: Execute parsed BASIC commands
#
# @param :: command :: Parsed command dictionary from parser
# @param :: variables :: Dictionary of variable name -> value
# @param :: lineMap :: Dictionary of line number -> index in program
# @param :: currentLine :: Current line number being executed
# @param :: programLines :: List of line numbers in order
#
# @return :: Next line number to execute, or None for sequential
def executor(command: dict, variables: dict, lineMap: dict, currentLine: int, programLines: list):
    import expression_evaluator as ee;
    
    cmdType: str = command["type"];
    
    if cmdType == "empty" or cmdType == "rem" or cmdType == "unknown":
        return None;
    
    # Variable assignment
    if cmdType == "let":
        varName: str = command["var"];
        expr: str = command["expr"];
        
        value: float = ee.expression_evaluator(expr, variables);
        variables[varName] = value;
        return None;
    
    # Print statement
    if cmdType == "print":
        items: list = command["items"];
        
        for i in range(len(items)):
            item: dict = items[i];
            
            if item["kind"] == "string":
                print(item["value"], end="");
            elif item["kind"] == "expr":
                value: float = ee.expression_evaluator(item["value"], variables);
                
                if value == int(value):
                    print(int(value), end="");
                else:
                    print(value, end="");
        
        print();
        return None;
    
    # Input statement
    if cmdType == "input":
        varName: str = command["var"];
        
        try:
            userInput: str = input("? ");
            value: float = float(userInput);
            variables[varName] = value;
        except ValueError:
            print("Invalid number");
            variables[varName] = 0.0;
        
        return None;
    
    # GOTO statement
    if cmdType == "goto":
        targetLine: int = command["line"];
        
        if targetLine in lineMap:
            return targetLine;
        else:
            print(f"Line {targetLine} not found");
        
        return None;
    
    # IF THEN statement
    if cmdType == "if":
        condition: str = command["condition"];
        result: float = ee.expression_evaluator(condition, variables);
        
        if result != 0.0:
            thenCommand: dict = command["then"];
            return executor(thenCommand, variables, lineMap, currentLine, programLines);
        
        return None;
    
    # FOR loop
    if cmdType == "for":
        varName: str = command["var"];
        startExpr: str = command["start"];
        endExpr: str = command["end"];
        
        startVal: float = ee.expression_evaluator(startExpr, variables);
        endVal: float = ee.expression_evaluator(endExpr, variables);
        
        variables[varName] = startVal;
        variables[f"__FOR_END_{varName}"] = endVal;
        variables[f"__FOR_LINE_{varName}"] = currentLine;
        
        return None;
    
    # NEXT statement
    if cmdType == "next":
        varName: str = command["var"];
        loopVar: str = f"__FOR_END_{varName}";
        lineVar: str = f"__FOR_LINE_{varName}";
        
        if varName in variables and loopVar in variables:
            variables[varName] = variables[varName] + 1;
            
            if variables[varName] <= variables[loopVar]:
                forLine: int = int(variables[lineVar]);
                
                forIdx: int = -1;
                for i in range(len(programLines)):
                    if programLines[i] == forLine:
                        forIdx = i;
                        break;
                
                if forIdx != -1 and forIdx + 1 < len(programLines):
                    return programLines[forIdx + 1];
            else:
                del variables[loopVar];
                del variables[lineVar];
        
        return None;
    
    # END statement
    if cmdType == "end":
        return -1;
    
    return None;


