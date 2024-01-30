import customtkinter
from PIL import Image
import webbrowser

class FooterFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.my_font = customtkinter.CTkFont(family="Helvetica", size=14)
        # Configure rows and columns
        self.rowconfigure(0, weight=1)
        num_cols = 3  # Three main sections in the footer
        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        # Left-aligned elements (version and copyright)
        self.version_label = customtkinter.CTkLabel(self, text="List App v1.0.0", font=self.my_font)
        self.version_label.grid(row=0, column=0, padx=10, sticky="w")

        self.license_label = customtkinter.CTkLabel(self, text="Licensed under the MIT License.", font=self.my_font)
        self.license_label.grid(row=0, column=1, padx=10)

        # Social Icons Frame
        social_icons_frame = customtkinter.CTkFrame(self)
        social_icons_frame.grid(row=0, column=2, padx=0, sticky="e")

        # Instagram Icon
        self.create_social_icon("", "https://www.instagram.com/prince_a_akeem", "images/instagram_icon.png", social_icons_frame)

        # GitHub Icon
        self.create_social_icon("", "https://github.com/prince-akeem", "images/github_icon.png", social_icons_frame)

    def create_social_icon(self, name, url, icon_path, parent):
        def open_link():
            webbrowser.open(url)

        parent_bg_color = parent.cget("bg_color")

        icon_image = customtkinter.CTkImage(light_image=Image.open(icon_path),
                                            dark_image=Image.open(icon_path),
                                            size=(30, 30))
        icon_button = customtkinter.CTkButton(parent, image=icon_image, text=name, command=open_link,
                                              fg_color=parent_bg_color, bg_color=parent_bg_color,
                                              width=50, hover_color=parent_bg_color, font=self.my_font)
        icon_button.image = icon_image
        icon_button.pack(side="left")
