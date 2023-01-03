import customtkinter as ctk
from gui.led import Led
from gui.stopwatch import StopWatch
from gui.settings import *
from gui.recorder import Recorder


class RelayBox(ctk.CTkFrame):
    """A relay box for monitoring."""
    def __init__(
        self, name: str = "relay", 
        text: str = "Relay",
        led_size: int = 45,
        label_font_family: str = "Verdana",
        label_font_size: int = 20,
        watch_font_size: int = 20,
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.label = ctk.CTkLabel(master=self, text=text, text_color="white", font=(label_font_family, label_font_size))
        self.watch = StopWatch(master=self, name=name, text="00:00:00", text_color="white", font=("Verdana", watch_font_size))
        self.led = Led(master=self, width=led_size, height=led_size, on_color=LED_ON_COLOR, off_color=LED_OFF_COLOR, bg=GRAY, bd=0, highlightthickness=0)
        
        self.label.grid(row=0, column=0)
        self.watch.grid(row=1, column=0)
        self.led.grid(row=2, column=0, pady=(10, 0))
        self.recorder = Recorder(filename=f"{name}.txt")
        self.restore_backup()

    def restore_backup(self):
        """restores the last record time found"""
        time_str = self.recorder.load_file()
        self.watch.update_time_value(time_str)
    
    def save_time(self):
        """Saves the current watch time."""
        time_str = self.watch.get_current_time_label()
        self.recorder.save(time_str)

    