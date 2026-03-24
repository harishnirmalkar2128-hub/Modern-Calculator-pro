import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ModernCalculator:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🧮 Modern Calculator Pro")
        self.window.geometry("400x680")
        self.window.resizable(False, False)
        self.window.configure(bg="#1b1b2e")
        self.window.attributes("-alpha", 0.95)

        # Calculator state
        self.expression = ""
        self.memory = 0
        self.last_result = None
        self.history = []

        self.setup_ui()
        self.setup_keyboard()

    def setup_ui(self):
        # Glass container
        glass_frame = ctk.CTkFrame(
            self.window,
            corner_radius=24,
            fg_color="#1f1f2e",
            border_width=1,
            border_color="#5b5b8a",
        )
        glass_frame.pack(padx=16, pady=16, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            glass_frame,
            text="Modern Calculator Pro",
            font=("Arial", 24, "bold"),
            text_color="#f8f8ff",
        )
        title.pack(pady=(12, 4))

        # Display
        self.display = ctk.CTkEntry(
            glass_frame,
            font=("Arial", 28),
            height=72,
            justify="right",
            state="readonly",
            fg_color="#232338",
            border_width=1,
            border_color="#6f6fb2",
            text_color="#f8f8ff",
        )
        self.display.pack(padx=18, pady=8, fill="x")

        # Memory and history indicators
        indicators_frame = ctk.CTkFrame(glass_frame, fg_color="#1f1f2e")
        indicators_frame.pack(fill="x", padx=18)

        self.memory_label = ctk.CTkLabel(
            indicators_frame,
            text="Memory: 0",
            font=("Arial", 10),
            text_color="#d9d9f1",
        )
        self.memory_label.pack(side="left")

        self.history_label = ctk.CTkLabel(
            indicators_frame,
            text="History: -",
            font=("Arial", 10),
            text_color="#d9d9f1",
        )
        self.history_label.pack(side="right")

        # Buttons frame
        buttons_frame = ctk.CTkFrame(glass_frame, fg_color="#1f1f2e")
        buttons_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Button layout
        buttons = [
            ["sin", "cos", "tan", "√"],
            ["log", "ln", "^", "()"],
            ["MC", "MR", "M+", "M-"],
            ["C", "CE", "±", "⌫"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["00", "0", ".", "="]
        ]

        for row in buttons:
            row_frame = ctk.CTkFrame(buttons_frame, fg_color="#1f1f2e")
            row_frame.pack(expand=True, fill="both", pady=2)

            for btn_text in row:
                fg_color, hover_color = self.get_button_colors(btn_text)
                btn = ctk.CTkButton(
                    row_frame,
                    text=btn_text,
                    fg_color=fg_color,
                    hover_color=hover_color,
                    font=("Arial", 16, "bold"),
                    corner_radius=16,
                    command=lambda t=btn_text: self.button_click(t),
                )
                btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)

    def get_button_colors(self, btn_text: str):
        # Professional modern calculator palette
        # Number buttons
        if btn_text.isdigit() or btn_text in ["00", "."]:
            return "#2b2e3c", "#3b3f55"

        # Primary action buttons
        if btn_text == "=":
            return "#4ac76f", "#3bb35c"
        if btn_text in ["C", "CE", "⌫"]:
            return "#ff5b5b", "#ff3b3b"

        # Operators
        if btn_text in ["/", "*", "-", "+", "^"]:
            return "#1e90ff", "#1c86ee"

        # Secondary operations / functions
        if btn_text in ["sin", "cos", "tan", "log", "ln", "√", "%", "()", "±"]:
            return "#7c5cff", "#6352e2"

        # Memory buttons
        if btn_text in ["MC", "MR", "M+", "M-"]:
            return "#6a7a8a", "#55616c"

        # Fallback
        return "#2b2e3c", "#3b3f55"

    def setup_keyboard(self):
        self.window.bind("<Key>", self.key_press)
        self.window.bind("<Return>", lambda e: self.button_click("="))
        self.window.bind("<BackSpace>", lambda e: self.button_click("⌫"))
        self.window.bind("<Escape>", lambda e: self.button_click("C"))

    def button_click(self, value):
        if value == "C":
            self.expression = ""
        elif value == "CE":
            self.clear_entry()
        elif value == "⌫":
            self.expression = self.expression[:-1]
        elif value == "()":
            self.add_parentheses()
        elif value == "±":
            self.toggle_sign()
        elif value == "=" or value == "Enter":
            self.evaluate_expression()
        elif value == "MC":
            self.memory = 0
        elif value == "MR":
            self.expression += str(self.memory)
        elif value == "M+":
            self.memory_operation(add=True)
        elif value == "M-":
            self.memory_operation(add=False)
        else:
            self.expression += value

        self.update_display()

    def clear_entry(self):
        # Remove the last entered number or function call
        self.expression = ""

    def add_parentheses(self):
        # Smart parentheses insertion
        if not self.expression or self.expression.endswith("("):
            self.expression += "("
        else:
            # If there is an unmatched '(', close it; otherwise, open a new one
            if self.expression.count("(") > self.expression.count(")"):
                self.expression += ")"
            else:
                self.expression += "("

    def toggle_sign(self):
        # Toggle sign for the last number entered
        match = re.search(r"([+\-*/^]|^)(\d+(?:\.\d*)?)$", self.expression)
        if not match:
            return
        prefix, number = match.group(1), match.group(2)
        if number.startswith("-"):
            self.expression = self.expression[: match.start(2)] + number[1:]
        else:
            self.expression = (
                self.expression[: match.start(2)] + "(-" + number + ")"
            )

    def memory_operation(self, add: bool):
        try:
            value = self.safe_eval(self.expression)
            if add:
                self.memory += value
            else:
                self.memory -= value
        except Exception:
            pass

    def evaluate_expression(self):
        try:
            result = self.safe_eval(self.expression)
            self.last_result = result
            self.history.append(f"{self.expression} = {result}")
            if len(self.history) > 5:
                self.history.pop(0)
            self.expression = str(result)
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.expression = ""

    def safe_eval(self, expression: str):
        # Normalize expression
        expression = expression.replace("^", "**")
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("√", "sqrt")

        # Support Ans token
        if self.last_result is not None:
            expression = expression.replace("ANS", str(self.last_result))

        # Convert percentage notation: 50% -> (50/100)
        expression = re.sub(r"(\d+(?:\.\d*)?)%", r"(\1/100)", expression)

        # Allowed functions and constants
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        allowed.update({"abs": abs, "round": round, "ln": math.log})

        return eval(expression, {"__builtins__": None}, allowed)

    def update_display(self):
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression or "0")
        self.display.configure(state="readonly")
        self.memory_label.configure(text=f"Memory: {self.memory}")

        history_text = " | ".join(self.history[-2:]) if self.history else "-"
        self.history_label.configure(text=f"History: {history_text}")

    def key_press(self, event):
        if event.char.isdigit() or event.char in "+-*/.%()^=":
            self.button_click(event.char)
        elif event.char.lower() in ["s", "c", "t", "l", "p"]:
            # allow typing common functions quickly
            mapping = {
                "s": "sin(",
                "c": "cos(",
                "t": "tan(",
                "l": "log(",
                "p": "±",
            }
            self.button_click(mapping[event.char.lower()])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = ModernCalculator()
    app.run()
