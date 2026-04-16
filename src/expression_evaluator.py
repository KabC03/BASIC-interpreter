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
        for var in variables:
            evalExpr = evalExpr.replace(var, str(variables[var]));
        
        result = eval(evalExpr);
        
    except NameError as e:
        print(f"Undefined variable: {e}");
    except Exception as e:
        print(f"Expression error: {e}");
    
    return result;



