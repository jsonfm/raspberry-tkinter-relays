import customtkinter as ctk


class StopWatch(ctk.CTkLabel):
    """A custom Pausable Time counter"""
    def __init__(
        self, 
        name: str = "stop watch", 
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self._running = False
        self.timerid = None
    
    
    def update_time_count(self):
        """Increases the time count."""
        self.seconds += 1

        if self.seconds >= 60:
            self.seconds = 0
            self.minutes += 1

        if self.minutes >= 60:
            self.minutes = 0
            self.hours += 1
        
        if self.hours >= 24:
            self.hours = 0
    
    def get_current_time_label(self):
        """Returns the current time label"""
        return f"{str(self.hours).zfill(2)}:{str(self.minutes).zfill(2)}:{str(self.seconds).zfill(2)}"
    
    def set_time_units_from_string(self, time_str: str):
        """Updates the time unit from a time string."""
        values = time_str.split(":")
        self.hours = int(values[0])
        self.minutes = int(values[1])
        self.seconds = int(values[2])

    def set_time_label(self):
        """Sets the current time on the label."""
        time_str = self.get_current_time_label()
        self.configure(text=time_str)

    def update_time_value(self, time_str: str):
        """Updates the time values given a time string."""
        self.time_str = time_str
        self.configure(text=time_str)
        self.set_time_units_from_string(time_str)

    def update_time_label(self):
        """Updates the current time label."""
        self.update_time_count()
        self.set_time_label()

    def update_time_callback(self):
        """Updates the time callback."""
        self.update_time_label()
        self.timerid = self.after(1000, self.update_time_callback)

    def stop(self):
        """Stops the time count."""
        if self._running:
            self.after_cancel(self.timerid)
            self._running = False
    
    def start(self):
        """Starts the time count."""
        if not self._running:
            self._running = True
            self.update_time_callback()
    
    def reset(self):
        """Resets the time count."""
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.stop()
