# parser.py
# @brief :: Parse typed tokens into command structure for BASIC interpreter
#
# @param :: tokens :: List of (token, type) tuples from tokeniser
#
# @return :: Dictionary with command type and processed arguments
def parser(tokens: list) -> dict:
    if len(tokens) == 0:
        return {"type": "empty"};
    
    # Skip line number if present
    startIdx: int = 0;
    if len(tokens) > 0 and tokens[startIdx][1] == "NUMBER":
        startIdx += 1;
    
    # Skip empty commands
    if startIdx >= len(tokens):
        return {"type": "empty"};
    
    cmd: str = tokens[startIdx][0].upper();
    
    # REM comment
    if cmd == "REM":
        return {"type": "rem"};
    
    # LET or SET assignment
    if cmd == "LET" or cmd == "SET":
        # LET IDENTIFIER EQUALS expression
        if startIdx + 3 < len(tokens) and tokens[startIdx + 1][1] == "IDENTIFIER" and tokens[startIdx + 2][1] == "EQUALS":
            varName: str = tokens[startIdx + 1][0];
            
            # Build expression from remaining tokens
            exprTokens: list = tokens[startIdx + 3:];
            expr: str = "";
            
            for tokenTuple in exprTokens:
                expr += tokenTuple[0];
            
            return {
                "type": "let",
                "var": varName,
                "expr": expr
            };
    
    # PRINT statement
    if cmd == "PRINT":
        printItems: list = [];
        printIdx: int = startIdx + 1;
        
        if printIdx >= len(tokens):
            return {"type": "print", "items": printItems};
        
        while printIdx < len(tokens):
            tokenTuple: tuple = tokens[printIdx];
            token: str = tokenTuple[0];
            tokenType: str = tokenTuple[1];
            
            # Handle strings
            if tokenType == "STRING":
                printItems.append({"kind": "string", "value": token[1:-1]});
                printIdx += 1;
            
            # Handle semicolons
            elif tokenType == "SEMICOLON":
                printIdx += 1;
                continue;
            
            # Handle expressions
            else:
                expr: str = "";
                
                while printIdx < len(tokens) and tokens[printIdx][1] != "SEMICOLON":
                    expr += tokens[printIdx][0];
                    printIdx += 1;
                
                if expr != "":
                    printItems.append({"kind": "expr", "value": expr});
        
        return {
            "type": "print",
            "items": printItems
        };
    
    # INPUT statement
    if cmd == "INPUT":
        if startIdx + 1 < len(tokens) and tokens[startIdx + 1][1] == "IDENTIFIER":
            return {
                "type": "input",
                "var": tokens[startIdx + 1][0]
            };
    
    # GOTO statement
    if cmd == "GOTO":
        if startIdx + 1 < len(tokens) and tokens[startIdx + 1][1] == "NUMBER":
            return {
                "type": "goto",
                "line": int(tokens[startIdx + 1][0])
            };
    
    # IF THEN statement
    if cmd == "IF":
        thenIdx: int = -1;
        
        for i in range(startIdx + 1, len(tokens)):
            if tokens[i][0].upper() == "THEN" and tokens[i][1] == "KEYWORD":
                thenIdx = i;
                break;
        
        if thenIdx != -1:
            # Build condition with proper spacing
            condition: str = "";
            for i in range(startIdx + 1, thenIdx):
                token: str = tokens[i][0];
                tokenType: str = tokens[i][1];
                
                if tokenType in ["EQUALS", "COMPARISON"]:
                    # Handle >= <= != == <>
                    if token == "<>":
                        condition += " != ";
                    elif token in [">=", "<=", "!=", "=="]:
                        condition += " " + token + " ";
                    elif token == "=":
                        condition += " == ";
                    elif token == ">":
                        condition += " > ";
                    elif token == "<":
                        condition += " < ";
                    else:
                        condition += " " + token + " ";
                else:
                    condition += token;
            
            # Parse THEN part
            thenTokens: list = tokens[thenIdx + 1:];
            thenCommand: dict = parseThen(thenTokens);
            
            return {
                "type": "if",
                "condition": condition,
                "then": thenCommand
            };
    
    # FOR loop
    if cmd == "FOR":
        # FOR IDENTIFIER EQUALS expression TO expression
        if startIdx + 5 < len(tokens) and tokens[startIdx + 1][1] == "IDENTIFIER" and tokens[startIdx + 2][1] == "EQUALS":
            varName: str = tokens[startIdx + 1][0];
            
            # Get start expression
            startExpr: str = "";
            idx: int = startIdx + 3;
            
            while idx < len(tokens) and tokens[idx][0].upper() != "TO":
                startExpr += tokens[idx][0];
                idx += 1;
            
            # Get end expression
            endExpr: str = "";
            idx += 1;  # Skip TO
            
            while idx < len(tokens):
                endExpr += tokens[idx][0];
                idx += 1;
            
            return {
                "type": "for",
                "var": varName,
                "start": startExpr,
                "end": endExpr
            };
    
    # NEXT statement
    if cmd == "NEXT":
        if startIdx + 1 < len(tokens) and tokens[startIdx + 1][1] == "IDENTIFIER":
            return {
                "type": "next",
                "var": tokens[startIdx + 1][0]
            };
    
    # END statement
    if cmd == "END":
        return {"type": "end"};
    
    return {"type": "unknown"};


# parseThen
# @brief :: Parse the THEN portion of an IF statement
#
# @param :: tokens :: List of (token, type) tuples after THEN
#
# @return :: Parsed command dictionary
def parseThen(tokens: list) -> dict:
    if len(tokens) == 0:
        return {"type": "empty"};
    
    cmd: str = tokens[0][0].upper();
    
    if cmd == "GOTO":
        if len(tokens) > 1 and tokens[1][1] == "NUMBER":
            return {
                "type": "goto",
                "line": int(tokens[1][0])
            };
    
    elif cmd == "PRINT":
        printItems: list = [];
        printIdx: int = 1;
        
        while printIdx < len(tokens):
            tokenTuple: tuple = tokens[printIdx];
            token: str = tokenTuple[0];
            tokenType: str = tokenTuple[1];
            
            if tokenType == "STRING":
                printItems.append({"kind": "string", "value": token[1:-1]});
                printIdx += 1;
            elif tokenType == "SEMICOLON":
                printIdx += 1;
                continue;
            else:
                expr: str = "";
                
                while printIdx < len(tokens) and tokens[printIdx][1] != "SEMICOLON":
                    expr += tokens[printIdx][0];
                    printIdx += 1;
                
                if expr != "":
                    printItems.append({"kind": "expr", "value": expr});
        
        return {
            "type": "print",
            "items": printItems
        };
    
    elif cmd == "LET" or cmd == "SET":
        if len(tokens) > 3 and tokens[1][1] == "IDENTIFIER" and tokens[2][1] == "EQUALS":
            expr: str = "";
            
            for i in range(3, len(tokens)):
                expr += tokens[i][0];
            
            return {
                "type": "let",
                "var": tokens[1][0],
                "expr": expr
            };
    
    return {"type": "empty"};

