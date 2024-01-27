import tkinter as tk
from tkinter import ttk
from tinydb import TinyDB

class AccListFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        # self.style.configure("Treeview", background="black",
        #         fieldbackground="black", foreground="white")

        self.tree = ttk.Treeview(self)
        self.db = TinyDB('ListAppDB.json')
        self.create_table()

        self.tree.pack(expand=True, fill='both',)

    def create_table(self):
        self.tree['columns'] = ('ID', 'Username', 'Password', 'Type', 'Status')

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        for entry in self.db.all():
            values = [entry[col] for col in self.tree['columns']]
            self.tree.insert('', 'end', values=values)

        self.tree.bind("<Button-3>", self.on_right_click)

    def on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            item = self.tree.item(iid)
            menu = tk.Menu(None, tearoff=0, takefocus=0)

            # Add menu option to copy username and password
            menu.add_command(label="Copy",
                             command=lambda: self.copy_to_clipboard(item['values'][1:3]))  # Copy 2nd and 3rd items (Username and Password)
            menu.tk_popup(event.x_root, event.y_root)

    def copy_to_clipboard(self, values):
        self.clipboard_clear()
        self.clipboard_append('\t\t\t'.join(map(str, values)))
