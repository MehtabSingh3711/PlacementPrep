import math
class Calculator:
    def __init__(self):
        self.history_stack = []

    def add(self, a, b):
        result = a + b
        self._add_to_history(f"{a} + {b} = {result}")
        return result

    def sub(self, a, b):
        result = a - b
        self._add_to_history(f"{a} - {b} = {result}")
        return result

    def mul(self, a, b):
        result = a * b
        self._add_to_history(f"{a} * {b} = {result}")
        return result

    def div(self, a, b):
        if b == 0:
            return "Error: Division by zero"
        result = a / b
        self._add_to_history(f"{a} / {b} = {result}")
        return result

    def power(self, a, b):
        result = math.pow(a, b)
        self._add_to_history(f"{a} ^ {b} = {result}")
        return result

    def sqrt(self, a):
        if a < 0:
            return "Error: Negative input for square root"
        result = math.sqrt(a)
        self._add_to_history(f"sqrt({a}) = {result}")
        return result

    def log(self, a):
        if a <= 0:
            return "Error: Non-positive input for logarithm"
        result = math.log(a)
        self._add_to_history(f"log({a}) = {result}")
        return result

    def _add_to_history(self, entry):
        self.history_stack.append(entry)

    def show_history(self):
        if not self.history_stack:
            print("History is empty.")
            return
        
        print("\n--- History (Most Recent First) ---")
        for i in range(len(self.history_stack) - 1, -1, -1):
            print(self.history_stack[i])
        print("-----------------------------------")

def main():
    calc = Calculator()
    print("Welcome to Calculator CLI!")
    print("Enter 'exit' at any prompt to quit.")
    print("Enter 'history' at 'Input 1' to see past calculations.")
    print("Supported Commands: +, -, *, /, ^ (power), sqrt, log")

    while True:
        try:
            val1_str = input("Input 1: ").strip()
            
            if val1_str.lower() == "exit":
                print("Exiting Calculator.")
                break
            if val1_str.lower() == "history":
                calc.show_history()
                continue
            
            if not val1_str:
                continue

            try:
                num1 = float(val1_str)
            except ValueError:
                print("Error: Invalid number.")
                continue

            op = input("Command: ").strip().lower()
            if op == "exit":
                print("Exiting Calculator.")
                break

            if op == "sqrt":
                print(calc.sqrt(num1))
                continue
            elif op == "log":
                print(calc.log(num1))
                continue
            
            if op not in ["+", "-", "*", "/", "^", "add", "sub", "mul", "div", "pow"]:
                print("Unknown command.")
                continue

            val2_str = input("Input 2: ").strip()
            if val2_str.lower() == "exit":
                print("Exiting Calculator.")
                break
            
            try:
                num2 = float(val2_str)
            except ValueError:
                print("Error: Invalid number.")
                continue

            if op in ["+", "add"]:
                print(calc.add(num1, num2))
            elif op in ["-", "sub"]:
                print(calc.sub(num1, num2))
            elif op in ["*", "mul"]:
                print(calc.mul(num1, num2))
            elif op in ["/", "div"]:
                print(calc.div(num1, num2))
            elif op in ["^", "pow"]:
                print(calc.power(num1, num2))

        except KeyboardInterrupt:
            print("\nExiting Calculator.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
