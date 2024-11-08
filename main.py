import tkinter as tk
from tkinter import StringVar, ttk
import math
from collections import deque


class PostfixCalculator:
    def __init__(self):
        self._buffer = deque()
        self._operations = {}
        self._exception_message = "Invalid Syntax"
        self.init_dict()

    def init_dict(self):
        self._operations = {
            "+": lambda: self.ensure_operands(2) or self._buffer.pop() + self._buffer.pop(),
            "-": lambda: self.ensure_operands(2) or -self._buffer.pop() + self._buffer.pop(),
            "*": lambda: self.ensure_operands(2) or self._buffer.pop() * self._buffer.pop(),
            "/": lambda: self.ensure_operands(2) or self.divide(),
            "%": lambda: self.ensure_operands(2) or self._buffer.pop() % self._buffer.pop(),
            "sin": lambda: self.ensure_operands(1) or math.sin(self._buffer.pop()),
            "cos": lambda: self.ensure_operands(1) or math.cos(self._buffer.pop()),
            "tg": lambda: self.ensure_operands(1) or math.tan(self._buffer.pop()),
            "pow": lambda: self.ensure_operands(1) or math.pow(self._buffer.pop(), 2),
            "sqrt": lambda: self.ensure_operands(1) or self.sqrt(),
            "log": lambda: self.ensure_operands(1) or self.log10(),
            "ln": lambda: self.ensure_operands(1) or self.ln(),
            "abs": lambda: self.ensure_operands(1) or abs(self._buffer.pop())
        }

    def ensure_operands(self, count):
        if len(self._buffer) < count:
            self.throw_exception(f"Insufficient operands (needed {count})")

    def divide(self):
        num2 = self._buffer.pop()
        num1 = self._buffer.pop()
        if num2 == 0:
            self.throw_exception("Cannot divide by zero")
        return num1 / num2

    def sqrt(self):
        num = self._buffer.pop()
        if num < 0:
            self.throw_exception("Sqrt() cannot be < 0")
        return math.sqrt(num)

    def log10(self):
        num = self._buffer.pop()
        if num <= 0:
            self.throw_exception("Log() cannot be ≤ 0")
        return math.log10(num)

    def ln(self):
        num = self._buffer.pop()
        if num <= 0:
            self.throw_exception("Ln() cannot be ≤ 0")
        return math.log(num)

    def process_input(self, input_value):
        if input_value in self._operations:
            # If input is an operator, perform the operation with last two numbers
            try:
                result = self._operations[input_value]()
                self._buffer.append(result)
                return result
            except Exception as e:
                return str(e)
        else:
            # If it's a number, add it to the stack
            self._buffer.append(float(input_value))
            return input_value

    def throw_exception(self, msg):
        self._exception_message = msg
        raise Exception(msg)

    def get_stack(self):
        return list(self._buffer)


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reverse Calculator")
        self.root.geometry("400x300")

        self.result_var = StringVar()
        self.input_var = StringVar()
        self.status_var = StringVar()

        self.history = []
        self.history_index = None
        self.calculator = PostfixCalculator()

        self.label = ttk.Label(self.root, text="Enter a number or operator, then press Enter:", font=("Helvetica", 16),
                               anchor="center", justify="center")
        self.label.pack(pady=10)

        self.input_entry = ttk.Entry(self.root, textvariable=self.input_var, font=("Helvetica", 14), justify='center')
        self.input_entry.pack(pady=10)

        self.result_label = ttk.Label(self.root, textvariable=self.result_var, font=("Helvetica", 16), anchor="center")
        self.result_label.pack(pady=10)

        self.input_entry.bind("<Return>", self.calculate_result)
        self.input_entry.bind("<Up>", self.show_previous_command)
        self.input_entry.bind("<Down>", self.show_next_command)

        status = ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken")
        status.pack(side="bottom", fill="x")

    def calculate_result(self, _):
        user_input = self.input_var.get()
        if user_input:
            try:
                result = self.calculator.process_input(user_input)
                self.update_display()
                self.status_var.set("Input processed successfully.")

                # Append input to history
                self.history.append(user_input)
                self.history_index = None
            except Exception as e:
                self.result_var.set("Error")
                self.status_var.set(f"Error: {str(e)}")

        self.input_var.set("")

    def update_display(self):
        # Display the current stack as a string
        stack_display = "Stack: " + " ".join(map(str, self.calculator.get_stack()))
        self.result_var.set(stack_display)

    def show_previous_command(self, _):
        if self.history and (self.history_index is None or self.history_index > 0):
            if self.history_index is None:
                self.history_index = len(self.history) - 1
            else:
                self.history_index -= 1

            self.input_var.set(self.history[self.history_index])
            self.input_entry.icursor(tk.END)

    def show_next_command(self, _):
        if self.history and self.history_index is not None:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.input_var.set(self.history[self.history_index])
            else:
                self.input_var.set("")
                self.history_index = None

            self.input_entry.icursor(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
