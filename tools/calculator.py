import math

DESCRIPTION = """calculator: Evaluates math expressions safely.
Input: {"expression": "2 + 2"} or {"expression": "sqrt(144)"} or {"expression": "log(100, 10)"}"""

def calculator(params: dict) -> str:
    expression = params.get("expression", "").strip()
    if not expression:
        return "Error: No expression provided."
    try:
        safe_globals = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        safe_globals["__builtins__"] = {}
        result = eval(expression, safe_globals, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Calculator Error: {e}"