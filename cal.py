import tkinter as tk
import math

# Font styles
LARGE_FONT_STYLE = ("Arial", 28, "bold")
SMALL_FONT_STYLE = ("Arial", 12)
DIGITS_FONT_STYLE = ("Arial", 18, "bold")
DEFAULT_FONT_STYLE = ("Arial", 16)

# Colors
OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("250x430")  # smaller size
        self.window.resizable(0, 0)
        self.window.title('Calculator')

        self.total_expression = ""
        self.current_expression = ""

        self.digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 1), '.': (4, 0)  # Decimal button added
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.total_label, self.label = self.create_display_labels()

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_square_button()
        self.create_sqrt_button()

        self.configure_buttons_grid()

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=60, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=16, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,
                         bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=16, font=LARGE_FONT_STYLE, wraplength=250, justify="right")
        label.pack(expand=True, fill="both")

        return total_label, label

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
        self.update_clear_button()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        if self.current_expression and (self.current_expression[-1] in self.operations.keys()):
            self.current_expression = self.current_expression[:-1]
        self.current_expression += operator
        self.update_label()
        self.update_clear_button()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=3, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()
        self.update_clear_button()

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()
        self.update_clear_button()

    def create_clear_button(self):
        self.clear_button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR,
                                      font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        self.clear_button.grid(row=0, column=0, sticky=tk.NSEW)

    def update_clear_button(self):
        if self.current_expression:
            self.clear_button.config(text="⌫", command=self.backspace)
        else:
            self.clear_button.config(text="C", command=self.clear)

    def evaluate(self):
        self.total_expression = self.current_expression
        try:
            result = eval(self.current_expression)
            if isinstance(result, float):
                result = round(result, 2)  # limit to 2 decimal places
            self.current_expression = str(result)
        except ZeroDivisionError:
            self.current_expression = "Error"
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_total_label()
            self.update_label()
            self.update_clear_button()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=2, columnspan=2, sticky=tk.NSEW)

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x²", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="√", bg=OFF_WHITE, fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def square(self):
        try:
            number = float(self.current_expression)
            result = number ** 2
            if isinstance(result, float):
                result = round(result, 2)
            self.current_expression = str(result)
            self.update_label()
        except Exception:
            self.current_expression = "Error"
            self.update_label()
        self.update_clear_button()

    def sqrt(self):
        try:
            number = float(self.current_expression)
            if number < 0:
                raise ValueError
            result = math.sqrt(number)
            if isinstance(result, float):
                result = round(result, 2)
            self.current_expression = str(result)
            self.update_label()
        except Exception:
            self.current_expression = "Error"
            self.update_label()
        self.update_clear_button()

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()

    def configure_buttons_grid(self):
        for i in range(5):  # 5 rows
            self.buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):  # 4 columns
            self.buttons_frame.columnconfigure(j, weight=1)

    def update_label(self):
        self.label.config(text=self.current_expression)

    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
