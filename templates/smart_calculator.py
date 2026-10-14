import cmath
import math
import statistics
import sympy as sp
from sympy import Eq, Matrix, solve, symbols
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

# Enable implicit multiplication (e.g., '4x', '8(x+2)')
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
)


def print_help():
    """Displays user guide for Smart Calculator features."""
    print("""
===================================================================
                   SMART CALCULATOR HELP & GUIDE                   
===================================================================
1. BASIC CALCULATIONS & IMPLICIT MULTIPLICATION:
   • Standard Math:     12 + 8 * (10 - 2) / 4   -> Answer: 28
   • Implicit Typing:   4x = 4  or  8(x + 2) = 32 -> Works automatically!
   • Powers / Exponents: 5²  or  2³  or  2 ^ 4  -> Answer: 25 | 8 | 16

2. TRIGONOMETRY (DEGREES):
   • Functions:         sin(30), cos(60), tan(45)
   • Inverse Trig:      asin(0.5), acos(0.5), atan(1)

3. ALGEBRA SOLVER (SymPy):
   • Single Equations:  x² = 4                  -> Answer: [-2, 2]
   • Equation Systems:  2x + y = 5, x - y = 1   -> Answer: {x: 2, y: 1}

4. CALCULUS (SymPy Engine):
   • Derivative:        diff(x^3 + sin(x), x)   -> Answer: 3*x^2 + cos(x)
   • Indefinite Integ:  integrate(x^2, x)       -> Answer: x^3/3
   • Definite Integ:    integrate(x^3 + sin(x), (x, 0, 1)) -> Answer: 5/4 - cos(1)
   • Limit:             limit(sin(x)/x, x, 0)   -> Answer: 1
   • Series Expansion:  series(exp(x), x, 0, 4) -> Answer: 1 + x + x^2/2 + x^3/6 + O(x^4)

5. MATRIX ALGEBRA:
   • Determinant:       det([,])   -> Answer: -2
   • Inverse Matrix:    inv([,])   -> Answer: Matrix([[-5/2, 3/2],])

6. STATISTICS:
   • Mean / Average:    mean(2, 4, 6, 8)        -> Answer: 5.0
   • Median:            median(1, 3, 5, 7, 9)   -> Answer: 5.0
   • Standard Dev:      stdev(2, 4, 4, 4, 5, 5, 7, 9) -> Answer: 2.138...

   Type 'quit' or 'exit' to exit the calculator.
===================================================================
""")


def clean_math_expression(text):
    """Normalizes power symbols into Python exponent format."""
    return (
        text.replace("⁰", "**0")
        .replace("¹", "**1")
        .replace("²", "**2")
        .replace("³", "**3")
        .replace("⁴", "**4")
        .replace("⁵", "**5")
        .replace("⁶", "**6")
        .replace("⁷", "**7")
        .replace("⁸", "**8")
        .replace("⁹", "**9")
        .replace("^", "**")
        .replace("×", "*")
        .replace("÷", "/")
    )


def parse_smart_expr(expr_str):
    """Parses expressions allowing implicit multiplication."""
    cleaned = clean_math_expression(expr_str)
    return parse_expr(cleaned, transformations=TRANSFORMATIONS)


def solve_calculus(text):
    """Calculates symbolic derivatives, integrals, limits, and series expansions using SymPy."""
    try:
        res = parse_smart_expr(text)
        return f"Calculus Result: {res}"
    except Exception as err:
        return f"Calculus Error: {err}"


def solve_matrix(text):
    """Calculates matrix determinants and inverses."""
    try:
        cleaned = clean_math_expression(text)
        first_p = cleaned.find("(")
        last_p = cleaned.rfind(")")

        if first_p == -1 or last_p == -1:
            return "Matrix Error: Missing parentheses."

        func_name = cleaned[:first_p].strip().lower()
        matrix_str = cleaned[first_p + 1 : last_p].strip()

        matrix_data = eval(matrix_str)
        m = Matrix(matrix_data)

        if func_name == "det":
            return f"Matrix Determinant: {m.det()}"
        elif func_name == "inv":
            return f"Inverse Matrix: {m.inv()}"

        return "Matrix Error: Function not recognized."

    except Exception as err:
        return f"Matrix Error: {err}"


def solve_statistics(text):
    """Calculates statistical metrics: mean, median, mode, and standard deviation."""
    try:
        cleaned = clean_math_expression(text)
        first_p = cleaned.find("(")
        last_p = cleaned.rfind(")")

        if first_p == -1 or last_p == -1:
            return "Statistics Error: Missing parentheses."

        func_name = cleaned[:first_p].strip().lower()
        nums_str = cleaned[first_p + 1 : last_p].strip()
        nums = [float(x.strip()) for x in nums_str.split(",") if x.strip()]

        if func_name == "mean":
            return f"Mean: {statistics.mean(nums)}"
        elif func_name == "median":
            return f"Median: {statistics.median(nums)}"
        elif func_name == "mode":
            return f"Mode: {statistics.mode(nums)}"
        elif func_name == "stdev":
            return f"Standard Deviation: {statistics.stdev(nums)}"

        return "Statistics Error: Function not recognized."

    except Exception as err:
        return f"Statistics Error: {err}"


def solve_algebra_sympy(eq_input):
    """Solves algebraic equations and multi-variable equation systems symbolically."""
    try:
        clean_input = eq_input.lower().replace("solve ", "").strip()

        # Multi-variable system of equations
        if "," in clean_input or ";" in clean_input:
            eq_strings = [
                e.strip()
                for e in clean_input.replace(";", ",").split(",")
                if e.strip()
            ]
            eq_objects = []
            var_set = set()

            for eq_str in eq_strings:
                if "=" not in eq_str:
                    return f"Algebra Error: Equation '{eq_str}' missing '='"
                left, right = eq_str.split("=")
                p_left = parse_smart_expr(left)
                p_right = parse_smart_expr(right)
                eq_objects.append(Eq(p_left, p_right))
                var_set.update(p_left.free_symbols | p_right.free_symbols)

            var_list = sorted(list(var_set), key=lambda s: s.name)
            solution = solve(eq_objects, var_list)
            return f"System Solution: {solution}"

        # Single variable equation
        elif "=" in clean_input:
            left, right = clean_input.split("=")
            p_left = parse_smart_expr(left)
            p_right = parse_smart_expr(right)
            eq_obj = Eq(p_left, p_right)

            var_list = sorted(list(eq_obj.free_symbols), key=lambda s: s.name)
            if not var_list:
                return "Algebra Error: No variable found to solve for."

            solution = solve(eq_obj, var_list)
            return f"Algebra Solution for {var_list}: {solution}"

        else:
            return "Algebra Error: Equation must contain '='"

    except Exception as err:
        return f"SymPy Algebra Error: {err}"


def calculate(user_input):
    """Main routing function for processing calculations."""
    user_input_clean = user_input.strip()
    lowered = user_input_clean.lower()

    if not user_input_clean:
        return "Please type a math problem or 'help'!"

    if lowered == "help":
        print_help()
        return "Help guide displayed above!"

    # -------------------------------------------------------------
    # CONVERSATIONAL FILTER: Catch greetings and non-math questions
    # -------------------------------------------------------------
    greetings = [
        "hi",
        "hello",
        "hey",
        "hola",
        "greetings",
        "good morning",
        "good afternoon",
        "good evening",
        "yo",
    ]
    chat_phrases = [
        "who are you",
        "what are you",
        "how are you",
        "what can you do",
        "can you talk",
    ]

    if lowered in greetings or any(phrase in lowered for phrase in chat_phrases):
        return (
            "Hello! 👋 I am Smart Calculator.\n"
            "I'm designed specifically for mathematical calculations, so I can't chat!\n\n"
            "I can help you solve:\n"
            "  • Basic Math & Trig   (e.g., '12 + 8 * 4' or 'sin(30)')\n"
            "  • Algebra & Systems    (e.g., '4x = 16' or '2x + y = 5, x - y = 1')\n"
            "  • Calculus             (e.g., 'diff(x^3, x)' or 'integrate(x^2, x)')\n"
            "  • Matrices & Stats     (e.g., 'det([,])' or 'mean(2, 4, 6, 8)')\n\n"
            "Please type a math problem or equation, or type 'help' for examples!"
        )

    # Calculus Routing
    if any(
        lowered.startswith(kw)
        for kw in [
            "diff(",
            "derivative(",
            "integrate(",
            "integral(",
            "limit(",
            "series(",
        ]
    ):
        return solve_calculus(user_input_clean)

    # Matrix Math Routing
    if any(lowered.startswith(kw) for kw in ["det(", "inv("]):
        return solve_matrix(user_input_clean)

    # Statistics Routing
    if any(
        lowered.startswith(kw) for kw in ["mean(", "median(", "mode(", "stdev("]
    ):
        return solve_statistics(user_input_clean)

    # Algebra Routing
    if lowered.startswith("solve ") or "=" in user_input_clean:
        return solve_algebra_sympy(user_input_clean)

    # Standard Arithmetic & Trigonometry Evaluation
    try:
        parsed = parse_smart_expr(user_input_clean)
        result = parsed.evalf()
        return f"Result: {result}"

    except Exception as e:
        return (
            "I am a Smart Calculator designed for math calculations!\n"
            f"Error parsing '{user_input_clean}'. Make sure to enter a valid mathematical expression, or type 'help' for examples."
        )


