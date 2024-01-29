import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tinydb import TinyDB, Query
import ttkbootstrap

class AccListFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # self.style = ttk.Style(self)
        # self.style.theme_use("clam")
        # self.style.configure("Treeview", background="#333333", fieldbackground="#333333", bordercolor="#333333", borderwidth=0)

        self.tree = ttk.Treeview(self, columns=('Delete', 'Id', 'Username', 'Password', 'Type', 'Status'), show='headings', style='success.Treeview')
        self.db = TinyDB('ListAppDB.json')
        self.create_table()

        self.tree.pack(expand=True, fill='both')

    def create_table(self):
        self.tree['columns'] = ('Id', 'Username', 'Password', 'Type', 'Status', 'Update', 'Delete')
        for col in ('Id', 'Username', 'Password', 'Type', 'Status'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        self.tree.heading('Update', text='Update')
        self.tree.heading('Delete', text='Delete')
        self.tree.column('Update', width=90, anchor='center')
        self.tree.column('Delete', width=90, anchor='center')

        for entry in self.db.all():
            values = [entry[col] for col in ('Id', 'Username', 'Password', 'Type', 'Status')]
            self.tree.insert('', 'end', values=(*values, 'Update', 'Delete'))

        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Button-3>", self.on_right_click)

    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        col = self.tree.identify_column(event.x)
        if region == "cell":
            item_id = self.tree.identify_row(event.y)
            if col == '#6':  # The 'Update' column
                self.update_record(item_id)
            elif col == '#7':  # The 'Delete' column
                self.delete_record(item_id)

    def update_record(self, item_id):
        item = self.tree.item(item_id)
        current_status = item['values'][4]  # Adjust index based on your columns
        new_status = simpledialog.askstring("Update Status", "Enter new status:",
                                            initialvalue=current_status)
        if new_status and new_status != current_status:
            record_id = item['values'][0]  # Adjust index based on your columns
            self.db.update({'Status': new_status}, Query().Id == record_id)
            self.tree.set(item_id, 'Status', new_status)

    def delete_record(self, item_id):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this record?"):
            record = self.tree.item(item_id)['values']
            record_id = record[0]  # Assuming the ID is the second value
            self.db.remove(Query().Id == record_id)
            self.tree.delete(item_id)

    def on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if iid and col in ('#2', '#3'):  # Assume columns 3 and 4 are 'Username' and 'Password'
            self.tree.selection_set(iid)
            item = self.tree.item(iid)
            values = item['values']
            username = values[1]  # Adjust index based on your columns
            password = values[2]  # Adjust index based on your columns
            menu = tk.Menu(None, tearoff=0, takefocus=0)
            menu.add_command(label="Copy Username", command=lambda: self.copy_to_clipboard(username))
            menu.add_command(label="Copy Password", command=lambda: self.copy_to_clipboard(password))
            menu.tk_popup(event.x_root, event.y_root)

    def copy_to_clipboard(self, value):
        self.clipboard_clear()
        self.clipboard_append(value)

    def refresh_data(self):
        # Clear the existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Re-populate the Treeview with data from the database
        self.create_table()