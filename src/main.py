# main.py
# @brief :: BASIC interpreter entry point
import sys;
import tokeniser as t;
import parser as p;
import executor as execModule;
import expression_evaluator as ee;

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename.bas>");
        return;
    
    filename: str = sys.argv[1];
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines();
        
        # Store program lines with line numbers
        program: dict = {};
        lineNumbers: list = [];
        
        for rawLine in lines:
            line: str = rawLine.strip();
            if line == "":
                continue;
            
            # Tokenise with type information
            tokens: list = t.tokeniser(line);
            if len(tokens) > 0 and tokens[0][1] == "NUMBER":
                lineNum: int = int(tokens[0][0]);
                program[lineNum] = line;
                lineNumbers.append(lineNum);
        
        # Sort line numbers
        lineNumbers.sort();
        
        # Create line map for GOTO
        lineMap: dict = {};
        for lineNum in lineNumbers:
            lineMap[lineNum] = lineNum;
        
        # Execute program
        variables: dict = {};
        pc: int = 0;
        
        print("RUN");
        print("---");
        
        while pc < len(lineNumbers):
            currentLineNum: int = lineNumbers[pc];
            line: str = program[currentLineNum];
            tokens: list = t.tokeniser(line);
            
            command: dict = p.parser(tokens);
            result = execModule.executor(command, variables, lineMap, currentLineNum, lineNumbers);
            
            if result == -1:
                break;
            elif result is not None:
                targetIdx: int = -1;
                for i in range(len(lineNumbers)):
                    if lineNumbers[i] == result:
                        targetIdx = i;
                        break;
                
                if targetIdx != -1:
                    pc = targetIdx;
                else:
                    print(f"Error: Line {result} not found");
                    break;
            else:
                pc += 1;
        
        print("---");
        print("END");
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found");
    except Exception as err:
        print(f"Error: {err}");


if __name__ == "__main__":
    main();


