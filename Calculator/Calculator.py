import tkinter

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["x\u00b2", "0", ".", "√"],
    ["⌫","", "="]
]

right_symbols = ["÷", "×", "-", "+", "√", "="]
top_symbols = ["AC", "+/-", "%"]
last_symbols = ["⌫"]
special_symbols = ["x\u00b2", "0"]

row_count = len(button_values)
column_count = len(button_values[0])

color_charcoal = "#393939"
color_dusty_rose = "#DEAA8E"
color_white = "#FBF5F5"
color_soft_sage_green = "#9DB2A2"
color_dark_sage_green = "#6A8E72"
color_lavender = "#988FB1"
color_warm_white = "#EDE6D6"

window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)

frame = tkinter.Frame(window, bg=color_warm_white)
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_white,
                      foreground=color_charcoal, anchor="e", width=column_count)

label.grid(row=0, column=0, columnspan=column_count, sticky="nsew")

for row in range(row_count):
    for column in range(len(button_values[row])):
        value = button_values[row][column]

        if value == "": continue
        if row == row_count - 1 and value == "⌫":
            button = tkinter.Button(frame, text=value, relief="flat", font=("Arial", 30),
                                    width=column_count-1, height=1,
                                    command=lambda value=value: button_clicked(value))
            button.grid(row=row+1, column=column, columnspan=2, padx=1, pady=1, sticky="nsew")
        elif row == row_count - 1 and value == "=":
            button = tkinter.Button(frame, text=value, relief="flat", font=("Arial", 30),
                                    width=column_count-1, height=1,
                                    command=lambda value=value: button_clicked(value))
            button.grid(row=row+1, column=column, columnspan=2, padx=1, pady=1, sticky="nsew")
        else:
            button = tkinter.Button(frame, text=value, relief="flat", font=("Arial", 30),
                                    width=column_count-1, height=1,
                                    command=lambda value=value: button_clicked(value))
            button.grid(row=row+1, column=column, padx=1, pady=1)
        
        if value in top_symbols:
            if value == "AC":
                button.config(foreground=color_white, background=color_dark_sage_green)
            else:
                button.config(foreground=color_charcoal, background=color_soft_sage_green)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_dusty_rose)
        elif value in special_symbols:
            button.config(foreground=color_charcoal, background=color_dusty_rose)
        else:
            button.config(foreground=color_charcoal, background=color_white)
            button.grid(row=row+1, column=column)
        
        if value in last_symbols:
            button.config(fg=color_white, bg=color_lavender)

frame.pack()

A = "0"
operator = None
B = None

def clear_all():
    global A, B, operator
    A = "0"
    operator = None
    B = None

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator

    if value in right_symbols:
        if value == "√":
            num = float(label["text"])
            if num < 0:
                label["text"] = "Error"
            else:
                result = float(label["text"]) ** 0.5
                label["text"] = remove_zero_decimal(result)
        elif value == "=":
            if A is not None and operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)

                if operator == "+":
                    label["text"] = remove_zero_decimal(numA + numB)
                elif operator == "-":
                    label["text"] = remove_zero_decimal(numA - numB)
                elif operator == "×":
                    label["text"] = remove_zero_decimal(numA * numB)
                elif operator == "÷":
                    if numB == 0:
                        label["text"] = "Error"
                    else:
                        label["text"] = remove_zero_decimal(numA / numB)
                
                clear_all()
        elif value in "+-×÷":
            if operator is None:
                A = label["text"]
                label["text"] = "0"
                B = "0"
            operator = value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"
        elif value == "+/-":
            result = float(label["text"]) * -1
            label["text"] = remove_zero_decimal(result)
        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_zero_decimal(result)

    elif value == "⌫":
        current = label["text"]
        if len(current) > 1:
            label["text"] = current[:-1]
        else:
            label["text"] = "0"

    else:
        if label["text"] == "Error":
            label["text"] = "0"
        if value == ".":
            if value not in label["text"]:
                label["text"] += value
        elif value == "x\u00b2":
            num = float(label["text"])
            result = num ** 2
            label["text"] = remove_zero_decimal(result)
        elif value in "0123456789":
            if label["text"] == "0":
                label["text"] = value
            else:
                label["text"] += value

def key_event(event):
    key = event.char

    if key in "0123456789":
        button_clicked(key)

    elif key == "+":
        button_clicked("+")

    elif key == "-":
        button_clicked("-")

    elif key == "*":
        button_clicked("×")

    elif key == "/":
        button_clicked("÷")

    elif key == ".":
        button_clicked(".")

    elif key == "\r":
        button_clicked("=")
    
    elif event.keysym == "BackSpace":
        button_clicked("⌫")

window.bind("<Key>", key_event)
window.mainloop()