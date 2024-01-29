import customtkinter
import tkinter as tk
from tinydb import TinyDB
import threading

class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, list_frame, **kwargs):
        super().__init__(master, **kwargs)
        self.list_frame = list_frame

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        num_cols = 6  # Number of columns in your table
        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        # Header row
        self.label = customtkinter.CTkLabel(self,
                    text="Account List App that is not a Password Manager")
        self.label.grid(row=0, columnspan=num_cols, padx=20)

        # New Account Row
        self.label = customtkinter.CTkLabel(self, text="Enter Account details -> ")
        self.label.grid(column=0, row=1, pady=1)
        self.entry_username = customtkinter.CTkEntry(self, width=120, placeholder_text="Username")
        self.entry_username.grid(column=1, row=1, pady=1)
        self.entry_password = customtkinter.CTkEntry(self, width=120, placeholder_text="Password")
        self.entry_password.grid(column=2, row=1, pady=1)
        self.entry_type = customtkinter.CTkEntry(self, width=120, placeholder_text="Type")
        self.entry_type.grid(column=3, row=1, pady=1)
        self.entry_status = customtkinter.CTkEntry(self, width=120, placeholder_text="Status")
        self.entry_status.grid(column=4, row=1, pady=1)

        # Add Account button
        self.addAcc_button = customtkinter.CTkButton(self, text="Add Account", command=self.submit)
        self.addAcc_button.grid(column=5, row=1)

    def show_message(self, message, message_color="red", display_time=3.0):
        """ Show a timed message (error or success) """
        message_label = customtkinter.CTkLabel(self, text=message, text_color=message_color)
        message_label.grid(column=0, row=2, columnspan=6, sticky="ew", pady=(0, 10))

        # Hide the message after a certain time (e.g., 3 seconds)
        threading.Timer(display_time, lambda: message_label.destroy()).start()

    def submit(self):
        # Get data from entry fields
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        acc_type = self.entry_type.get().strip()

        # Check if any required field is empty
        if not username:
            self.show_message("Username cannot be empty")
            return
        if not password:
            self.show_message("Password cannot be empty")
            return
        if not acc_type:
            self.show_message("Type cannot be empty")
            return

        # Proceed with database insertion if all checks pass
        db = TinyDB('ListAppDB.json')
        new_id = len(db.all()) + 1

        db.insert({'Id': new_id,
            'Username':self.entry_username.get(),
            'Password':self.entry_password.get(),
            'Type':self.entry_type.get(),
            'Status':self.entry_status.get()})

        # Show success message and reset fields
        self.show_message("Account added successfully!", message_color="green", display_time=3)
        self.reset_entry_fields()
        self.list_frame.refresh_data()

    def reset_entry_fields(self):
        """ Reset all entry fields """
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_status.delete(0, tk.END)



