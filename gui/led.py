import customtkinter as ctk


class Led(ctk.CTkCanvas):
    """A custom Led Button based on Tk Canvas"""
    def __init__(
        self, 
        checked: bool = False, 
        on_color: str = "green",
        off_color: str = "red",
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.on_color = on_color
        self.off_color = off_color
        self.checked = checked
        self.oval = self.create_oval(0, 0, kwargs.get("width", 20) - 2, kwargs.get("height", 20) - 2)
        self.set_checked(checked)
    
    def set_checked(self, checked: bool):
        """Updates the checked status."""
        self.checked = checked
        if self.checked:
            self.itemconfig(self.oval, fill=self.on_color)
        else:
            self.itemconfig(self.oval, fill=self.off_color)
    
    def is_checked(self) -> bool:
        """Returns the current checked status."""
        return self.checked
    
    def toggle(self) -> bool:
        """Toggles the current checked status"""
        self.checked = not self.checked
        self.set_checked(self.checked)
        return self.checked

    