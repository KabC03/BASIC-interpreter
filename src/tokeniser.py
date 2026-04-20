# tokeniser.py
# @brief :: Convert line of BASIC code into tokens
#
# @param :: line :: String containing one line of BASIC code
#
# @return :: List of tokens with type information
def tokeniser(line: str) -> list:
    tokens: list = [];
    currentToken: str = "";
    inString: bool = False;
    quoteChar: str = "";
    i: int = 0;
    
    while i < len(line):
        char: str = line[i];
        
        # Handle string literals
        if char == '"' or char == "'":
            if not inString:
                # Start of string
                if currentToken != "":
                    tokenType: str = getTokenType(currentToken);
                    tokens.append((currentToken, tokenType));
                    currentToken = "";
                
                inString = True;
                quoteChar = char;
                currentToken = char;
            elif char == quoteChar:
                # End of string
                currentToken += char;
                tokens.append((currentToken, "STRING"));
                currentToken = "";
                inString = False;
                quoteChar = "";
            
            else:

                currentToken += char;
            
            i += 1;
            continue;
        
        # Inside string, take everything
        if inString:
            currentToken += char;
            i += 1;
            continue;
        
        # Whitespace separates tokens
        if char == ' ' or char == '\t':
            if currentToken != "":
                tokenType: str = getTokenType(currentToken);
                tokens.append((currentToken, tokenType));
                currentToken = "";
            
            i += 1;
            continue;
        
        # Single character operators and delimiters
        if char in ['=', '+', '-', '*', '/', '(', ')', ',', ':', ';']:
            if currentToken != "":
                tokenType: str = getTokenType(currentToken);
                tokens.append((currentToken, tokenType));
                currentToken = "";
            
            # Map single char tokens
            tokenMap: dict = {
                '=': "EQUALS",
                '+': "PLUS",
                '-': "MINUS",
                '*': "MULTIPLY",
                '/': "DIVIDE",
                '(': "LPAREN",
                ')': "RPAREN",
                ',': "COMMA",
                ':': "COLON",
                ';': "SEMICOLON",
            };
            tokens.append((char, tokenMap[char]));
            i += 1;
            continue;
        
        # Comparison operators
        if char in ['>', '<', '!']:
            if currentToken != "":
                tokenType: str = getTokenType(currentToken);
                tokens.append((currentToken, tokenType));
                currentToken = "";
            
            # Check for two character operators
            if i + 1 < len(line):
                twoChar: str = line[i:i+2];
                if twoChar in ['>=', '<=', '!=', '==']:
                    tokens.append((twoChar, "COMPARISON"));
                    i += 2;
                    continue;
            
            tokens.append((char, "COMPARISON"));
            i += 1;
            continue;
        
        # Build current token
        currentToken += char;
        i += 1;
    
    # Add any remaining token
    if currentToken != "":
        if inString:
            tokens.append((currentToken, "STRING"));
        else:
            tokenType: str = getTokenType(currentToken);
            tokens.append((currentToken, tokenType));
    
    return tokens;


# getTokenType
# @brief :: Determine the type of a token
#
# @param :: token :: String token to classify
#
# @return :: String representing token type
def getTokenType(token: str) -> str:
    # Keywords
    keywords: list = [
        "LET", "PRINT", "INPUT", "IF", "THEN", "ELSE", "GOTO", 
        "FOR", "TO", "NEXT", "END", "REM", "DIM", "GOSUB", "RETURN",
        "SET", "LABEL",
    ];
    
    upperToken: str = token.upper();
    
    if upperToken in keywords:
        return "KEYWORD";
    
    # Numbers
    if isNumber(token):
        return "NUMBER";
    
    # Identifiers
    if isIdentifier(token):
        return "IDENTIFIER";
    
    return "UNKNOWN";


# isNumber
# @brief :: Check if token is a valid number
#
# @param :: token :: String to check
#
# @return :: True if token can be parsed as number
def isNumber(token: str) -> bool:
    if len(token) == 0:
        return False;
    
    # Handle negative numbers
    startIdx: int = 0;
    if token[0] == '-':
        if len(token) == 1:
            return False;
        startIdx = 1;
    
    dotCount: int = 0;
    for i in range(startIdx, len(token)):
        char: str = token[i];
        if char == '.':
            dotCount += 1;
            if dotCount > 1:
                return False;
        elif not char.isdigit():

            return False;
    
    return True;


# isIdentifier
# @brief :: Check if token is a valid identifier
#
# @param :: token :: String to check
#
# @return :: True if token is valid variable/label name
def isIdentifier(token: str) -> bool:
    if len(token) == 0:
        return False;
    
    # First character must be letter or underscore
    firstChar: str = token[0];
    if not (firstChar.isalpha() or firstChar == '_'):
        return False;
    
    # Rest can be alphanumeric or underscore
    for i in range(1, len(token)):
        char: str = token[i];

        if not (char.isalnum() or char == '_'):
            return False;
    
    return True;


# tokeniseLine
# @brief :: Convenience function to tokenise and return just token values
#
# @param :: line :: String containing one line of BASIC code
#
# @return :: List of token values without type info
def tokeniseLine(line: str) -> list:
    typedTokens: list = tokeniser(line);
    simpleTokens: list = [];
    
    for tokenTuple in typedTokens:
        simpleTokens.append(tokenTuple[0]);
    
    return simpleTokens;




