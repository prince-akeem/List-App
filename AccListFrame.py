import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tinydb import Query
from DataBase import get_database

class UpdateDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, initial_values):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        self.result = None
        self.initial_values = initial_values
        self.create_widgets()
        self.center_window(parent)
        self.grab_set()
        self.bind("<Return>", self.on_update)
        self.wait_window(self)

    def create_widgets(self):
        labels = ['Username', 'Password', 'Type', 'Status']
        self.entries = {}
        for i, label in enumerate(labels):
            ctk.CTkLabel(self, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = ctk.CTkEntry(self, width=400)
            entry.insert(0, self.initial_values[i])
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

        update_button = ctk.CTkButton(self, text="Update", command=self.on_update)
        update_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def on_update(self, event=None):
        self.result = [self.entries[field].get() for field in ['Username', 'Password', 'Type', 'Status']]
        self.destroy()

    def center_window(self, parent):
        self.update_idletasks()  # Update "requested size" from geometry manager
        ww = self.winfo_width()
        wh = self.winfo_height()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        x = px + (pw - ww) // 2
        y = py + (ph - wh) // 2
        self.geometry(f'+{x}+{y}')  # Center the window

class AccListFrame(tk.Frame):
    def __init__(self, master, **kwargs):

        self.bg_color = master.cget('bg')
        self.text_color = "#f0f0f0"  # Light text color
        if ctk.get_appearance_mode() == 'Light':
            self.text_color = "gray10"

        super().__init__(master, bg=self.bg_color, borderwidth=0, relief="flat", **kwargs)


        self.my_font = tk.font.Font(family="Helvetica", size=12)
        self.header_font = tk.font.Font(family="Helvetica", size=16, weight="bold")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Apply CustomTkinter colors to the Treeview
        self.style.configure("Treeview", background=self.bg_color, fieldbackground=self.bg_color, border_color="", foreground=self.text_color, font=self.my_font, rowheight=26, borderwidth=0, relief="flat")
        self.style.configure("Treeview.Heading", background=self.bg_color, foreground=self.text_color, font=self.header_font, borderwidth=0, relief="flat")
        # self.style.configure("Treeview", background="#333333", fieldbackground="#333333", bordercolor="#333333", borderwidth=0)

        self.tree = ttk.Treeview(self, columns=('Delete', 'Id', 'Username', 'Password', 'Type', 'Status'), show='headings',)
        self.db = get_database()
        self.create_table()

        self.tree.pack(expand=True, fill='both')

    def create_table(self):
        self.tree['columns'] = ('#', 'Username', 'Password', 'Type', 'Status', 'Update', 'Delete')
        for col in ('#', 'Username', 'Password', 'Type', 'Status'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        self.tree.heading('Update', text='Update')
        self.tree.heading('Delete', text='Delete')
        self.tree.column('Update', width=90, anchor='center')
        self.tree.column('Delete', width=90, anchor='center')

        sorted_entries = sorted(self.db.all(), key=lambda x: x['Id'])

        for entry in sorted_entries:
            values = [entry[col] for col in ('Id', 'Username', 'Password', 'Type', 'Status')]
            self.tree.insert('', 'end', values=(*values, '[Update]', '[Delete]'))

        self.adjust_column_width()
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Button-3>", self.on_right_click)
        self.tree.bind("<Return>", self.on_enter_press)
        self.tree.bind("<Delete>", self.on_delete_press)

    def adjust_column_width(self):
        for col in self.tree['columns']:
            max_width = 0
            self.tree.column(col, width=tk.font.Font().measure(col.title()))
            for row in self.tree.get_children():
                item = self.tree.item(row)['values']
                col_index = self.tree['columns'].index(col)
                cell_width = tk.font.Font().measure(str(item[col_index]))
                max_width = max(max_width, cell_width)
            self.tree.column(col, width=max_width)

    def on_enter_press(self, event):
        selected_item = self.tree.selection()
        if selected_item:  # Check if there is a selected item
            self.update_record(selected_item[0])

    def on_delete_press(self, event):
        selected_item = self.tree.selection()
        if selected_item:  # Check if there is a selected item
            self.delete_record(selected_item[0])

    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        col = self.tree.identify_column(event.x)
        if region == "cell":
            item_id = self.tree.identify_row(event.y)
            if col == '#6':  # The 'Update' column
                self.update_record(item_id)
            elif col == '#7':  # The 'Delete' column
                self.delete_record(item_id)

    # def update_record(self, item_id):
    #     item = self.tree.item(item_id)
    #     current_status = item['values'][4]  # Adjust index based on your columns
    #     new_status = simpledialog.askstring("Update Status", "Enter new status:",
    #                                         initialvalue=current_status)
    #     if new_status and new_status != current_status:
    #         record_id = item['values'][0]  # Adjust index based on your columns
    #         self.db.update({'Status': new_status}, Query().Id == record_id)
    #         self.tree.set(item_id, 'Status', new_status)
    def update_record(self, item_id):
        item = self.tree.item(item_id)
        current_values = item['values'][1:5]  # Adjust indices based on your columns (Username, Password, Type, Status)

        dialog = UpdateDialog(self, "Update Record", current_values)
        new_values = dialog.result

        if new_values and new_values != current_values:
            record_id = item['values'][0]  # Adjust index based on your columns
            update_data = dict(zip(['Username', 'Password', 'Type', 'Status'], new_values))
            self.db.update(update_data, Query().Id == record_id)

            # Update Treeview
            for i, field in enumerate(['Username', 'Password', 'Type', 'Status']):
                self.tree.set(item_id, field, new_values[i])

    def delete_record(self, item_id):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this record?"):

            # Find the closest record to the deleted record
            next_item = self.tree.next(item_id)
            prev_item = self.tree.prev(item_id)

            record = self.tree.item(item_id)['values']
            record_id = record[0]
            self.db.remove(Query().Id == record_id)
            self.tree.delete(item_id)

            # Select the closest record to the deleted record
            if next_item:
                self.tree.focus(next_item)
                self.tree.selection_set(next_item)
            elif prev_item:
                self.tree.focus(prev_item)
                self.tree.selection_set(prev_item)

    def on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if iid and col in ('#2', '#3'):  # columns 2 and 3 are 'Username' and 'Password'
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
