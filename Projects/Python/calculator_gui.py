from tkinter import *
from tkinter.ttk import *
equat = ""
last_input = ""

def input_manager(character_input):
    global equat
    equat = entry.get()
    if len(equat) > 0:
        equat = equat + " " + character_input
    else:
        equat = character_input
    entry.insert(0, equat)
    
calc = Tk()
calc.geometry("400x200")
entry = Entry(width=19)
btn_1 = Button(text="1", width=19, command = input_manager("1"))
btn_2 = Button(text="2", width=19, command = input_manager("2"))
btn_3 = Button(text="3", width=19, command = input_manager("3"))
btn_4 = Button(text="4", width=19, command = input_manager("4"))
btn_5 = Button(text="5", width=19, command = input_manager("5"))
btn_6 = Button(text="6", width=19, command = input_manager("6"))
btn_7 = Button(text="7", width=19, command = input_manager("7"))
btn_8 = Button(text="8", width=19, command = input_manager("8"))
btn_9 = Button(text="9", width=19, command = input_manager("9"))
btn_0 = Button(text="0", width=19, command = input_manager("0"))
btn_plus = Button(text="+", width=19, command = input_manager("+"))
btn_minus = Button(text="-", width=19, command = input_manager("-"))
btn_mult = Button(text="*", width=19, command = input_manager("*"))
btn_div = Button(text="/", width=19, command = input_manager("/"))
btn_expo = Button(text="^", width=19, command = input_manager("^"))
btn_enter = Button(text = "Enter", width=19)
entry.grid(row=0, column=0, sticky="ew")
btn_enter.grid(row=0, column=1, sticky="ew",padx=4, pady=3)
btn_1.grid(row=1, column=0, sticky="ew", padx=4, pady=3)
btn_2.grid(row=1, column=1, sticky="ew", padx=4, pady=3)
btn_3.grid(row=1, column=2, sticky="ew", padx=4, pady=3)
btn_4.grid(row=2, column=0, sticky="ew", padx=4, pady=3)
btn_5.grid(row=2, column=1, sticky="ew", padx=4, pady=3)
btn_6.grid(row=2, column=2, sticky="ew", padx=4, pady=3)
btn_7.grid(row=3, column=0, sticky="ew", padx=4, pady=3)
btn_8.grid(row=3, column=1, sticky="ew", padx=4, pady=3)
btn_9.grid(row=3, column=2, sticky="ew", padx=4, pady=3)
btn_plus.grid(row=4, column=0, sticky="ew", padx=4, pady=3)
btn_0.grid(row=4, column=1, sticky="ew", padx=4, pady=3)
btn_minus.grid(row=4, column=2, sticky="ew", padx=4, pady=3)
btn_mult.grid(row=5, column=0, sticky="ew", padx=4, pady=3)
btn_div.grid(row=5, column=1, sticky="ew", padx=4, pady=3)
btn_expo.grid(row=5, column=2, sticky="ew", padx=4, pady=3)

calc.mainloop()