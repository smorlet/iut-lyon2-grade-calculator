import tkinter as tk

root = tk.Tk()

tk.Label(root, text="A", bg="lightblue").grid(row=0, column=0, sticky="nsew")
tk.Label(root, text="B", bg="pink").grid(row=0, column=1, sticky="nsew")
tk.Label(root, text="C", bg="lightgreen").grid(row=2, column=0, columnspan=2, sticky="nsew")

# Configuration des lignes
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=10)
root.rowconfigure((0,1,2),weight=(1,1,10))
# Configuration des colonnes
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()
