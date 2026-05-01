# expression_evaluator.py
# @brief :: Evaluate an expression given a variable dictionary and expression
#
# @param :: expr :: String expression with variables
# @param :: variables :: Dictionary of variable name -> value
#
# @return :: Returned float value of expression
def expression_evaluator(expr: str, variables: dict) -> float:
    result: float = 0.0;
    try:
        # Replace variables with their values
        evalExpr: str = expr;
        
        # Sort variables by length (longest first) to avoid partial replacements
        sortedVars: list = sorted(variables.keys(), key=len, reverse=True);
        
        for var in sortedVars:
            evalExpr = evalExpr.replace(var, str(variables[var]));
        
        result = eval(evalExpr);
        
    except NameError as e:
        print(f"Undefined variable: {e}");
    except Exception as e:
        print(f"Expression error: {e}");
    
    return result;


