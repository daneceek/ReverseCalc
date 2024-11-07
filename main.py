

from os.path import basename, splitext
import tkinter as tk
from tkinter import font
from operation import operation1, operation2
import operator
import math


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class MyListbox(tk.Listbox):
    def pop(self):
        if self.size() > 0:
            x = self.get("end")
            self.delete("end")
            return x
        else:
            raise IndexError("The stack is empty")


class Application(tk.Tk):
    name = "RevCal"
    font_settings = ("Verdana", 16)

    def __init__(self):
        super().__init__(className=self.name)
        self.option_add("*Font", self.font_settings)

        self.title(self.name)
        self.bind("<Escape>", self.destroy)

        
        self.lbl = tk.Label(self, text="Reverzní kalkulátor")
        self.listbox = MyListbox(master=self)
        self.btn = tk.Button(self, text="Opustit", command=self.destroy)
        self.entry = MyEntry(master=self)
        self.entry.bind("<Return>", self.enterHandler)
        self.entry.bind("<KP_Enter>", self.enterHandler)
        
       
        self.status_bar = tk.Label(self, text="", fg="red")
        
        
        self.history = []
        self.history_index = -1
        self.entry.bind("<Up>", self.showPreviousHistory)
        self.entry.bind("<Down>", self.showNextHistory)

        
        self.lbl.pack()
        self.listbox.pack()
        self.entry.pack()
        self.btn.pack()
        self.status_bar.pack(fill="x")
        self.entry.focus()

    def enterHandler(self, event):
        input_text = self.entry.value.strip()
        self.history.append(input_text)
        self.history_index = len(self.history)
        
        for token in input_text.split():
            try:
                self.listbox.insert("end", float(token))
                self.updateStatus("")  
            except ValueError:
                self.tokenProcess(token)
                
        self.entry.value = ""
        self.listbox.see("end")

    def tokenProcess(self, token):
        try:
            if token in operation2:
                if self.listbox.size() < 2:
                    raise ValueError("Nedostatek čísel")
                b = float(self.listbox.pop())
                a = float(self.listbox.pop())
                if token == '/' and b == 0:
                    self.listbox.insert("end", a)
                    raise ZeroDivisionError("Dělení nulou")
            
                result = operation2[token](a, b)
                self.listbox.insert("end", result)
                self.updateStatus("")  

            elif token in operation1:
                if self.listbox.size() < 1:
                    raise ValueError("Nedostatek čísel")
                a = float(self.listbox.pop())
                result = operation1[token](a)
                self.listbox.insert("end", result)
                self.updateStatus("") 

            

            elif token == "del" and self.listbox.size() >= 1:
                self.listbox.delete("end")
            else:
                raise ValueError(f"Neznámý token: {token}")
        
        except (ValueError, ZeroDivisionError) as e:
            self.updateStatus(str(e))

    def updateStatus(self, message):
        self.status_bar.config(text=message)

    def showPreviousHistory(self, event):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.entry.value = self.history[self.history_index]

    def showNextHistory(self, event):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.entry.value = self.history[self.history_index]
        elif self.history_index == len(self.history) - 1:
            self.history_index += 1
            self.entry.value = ""  

    def destroy(self, event=None):
        super().destroy()



app = Application()
app.mainloop()
