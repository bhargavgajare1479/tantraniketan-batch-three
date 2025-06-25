import tkinter as tk
from tkinter import ttk, scrolledtext

core_concepts = {
    "Variables": "Variables store data values. Example:\n\nx = 5\ny = 'Hello'",
    "Data Types": "Common data types: int, float, str, bool, list, tuple, dict, set.\n\nExample:\nnum = 10\nname = 'Alice'\nnums = [1, 2, 3]",
    "Operators": "Operators perform operations on variables and values.\n\nExample:\nresult = 2 + 3 * 4",
    "Control Flow": "if, elif, else, for, while are used for control flow.\n\nExample:\nif x > 0:\n    print('Positive')",
    "Functions": "Functions are reusable blocks of code.\n\nExample:\ndef greet(name):\n    print('Hello', name)",
    "Classes & Objects": "Classes define objects. Objects are instances of classes.\n\nExample:\nclass Dog:\n    def __init__(self, name):\n        self.name = name",
    "Modules & Packages": "Modules are files with Python code. Packages are collections of modules.\n\nExample:\nimport math\nprint(math.sqrt(16))",
    "Exception Handling": "Handle errors using try-except.\n\nExample:\ntry:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')",
    "File I/O": "Read and write files.\n\nExample:\nwith open('file.txt', 'r') as f:\n    data = f.read()",
    "List Comprehensions": "Concise way to create lists.\n\nExample:\nsquares = [x*x for x in range(5)]",
}

def show_concept(event):
    concept = concept_listbox.get(concept_listbox.curselection())
    explanation = core_concepts[concept]
    text_area.config(state='normal')
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, explanation)
    text_area.config(state='disabled')

root = tk.Tk()
root.title("Python Core Concepts")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

ttk.Label(mainframe, text="Select a Python Core Concept:").grid(row=0, column=0, sticky=tk.W)

concept_listbox = tk.Listbox(mainframe, height=10)
for concept in core_concepts:
    concept_listbox.insert(tk.END, concept)
concept_listbox.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
concept_listbox.bind('<<ListboxSelect>>', show_concept)

text_area = scrolledtext.ScrolledText(mainframe, width=60, height=15, wrap=tk.WORD, state='disabled')
text_area.grid(row=1, column=1, padx=10, sticky=(tk.N, tk.S, tk.W, tk.E))

root.mainloop()