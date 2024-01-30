import customtkinter as customtkinter
from HeaderFrame import MenuFrame
from AccListFrame import AccListFrame
from FooterFrame import FooterFrame

# Sets the appearance of the window
# Supported modes : Light, Dark, System
# "system" sets the appearance mode to
customtkinter.set_appearance_mode("System")

# Supported themes : green, dark-blue, blue
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Get the device screen dimensions
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        # Calculate the window size (65% of the screen size)
        window_width, window_height = int(screen_width * 0.65), int(screen_height * 0.65)
        # Calculate the position to center the window
        center_x, center_y = int(screen_width / 2 - window_width / 2), int(screen_height / 2 - window_height / 2)

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.title("List App v1.0.0")

        self.list_frame = AccListFrame(master=self)
        self.list_frame.grid(row=1, sticky="nsew")

        self.top_frame = MenuFrame(master=self, list_frame=self.list_frame, corner_radius=0)
        self.top_frame.grid(row=0, sticky="nsew")

        self.foot_frame = FooterFrame(master=self, corner_radius=0)
        self.foot_frame.grid(row=2, sticky="nsew")

        self.grid_rowconfigure(0, weight=15)        # 15% of the window
        self.grid_rowconfigure(1, weight=80)        # 80% of the window
        self.grid_rowconfigure(2, weight=5)         # 5% of the window

        self.grid_columnconfigure(0, weight=1)

app = App()
app.mainloop()
