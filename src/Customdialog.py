import tkinter as tk

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.parent = parent
        self.x = self.parent.winfo_x()
        self.y = self.parent.winfo_y()
        
        label = tk.Label(self, text=prompt)
        label.pack(padx=10, pady=10)
        self.geometry(f"400x400+{self.x}+{self.y}")
        self.resizable(0,0)
        
        self.entry_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.entry_var)
        entry.pack(padx=10, pady=10)
        
        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.pack(padx=10, pady=10)

    def submit(self):
        self.result = self.entry_var.get()
        self.destroy()




