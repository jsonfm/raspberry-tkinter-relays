import os
import pathlib
from PIL import Image
import customtkinter as ctk
from gui.settings import *


class Navbar(ctk.CTkFrame):
    """Custom Navbar."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filepath = pathlib.Path(__file__).resolve().parent
        close_png = os.path.join(filepath, "assets", "close.png")
        fullscreen_png = os.path.join(filepath, "assets", "fullscreen.png")

        self.close_icon = ctk.CTkImage(light_image=Image.open(close_png), size=(30, 30))
        self.close_btn = ctk.CTkButton(master=self, image=self.close_icon, text="", fg_color=GRAY, hover_color=GRAY, width=10)
        self.fullscreen_icon = ctk.CTkImage(light_image=Image.open(fullscreen_png), size=(30, 30))
        self.fullscreen_btn = ctk.CTkButton(master=self, image=self.fullscreen_icon, text="", fg_color=GRAY, hover_color=GRAY, width=10)

        self.close_btn.grid(row=0, column=2)
        self.fullscreen_btn.grid(row=0, column=1)