import tkinter as tk
import customtkinter as ctk
from gui.relaybox import RelayBox
from gui.pin import PinManager
from gui.navbar import Navbar
from gui.settings import *


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class Application:
    """A GUI for monitoring ..."""
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Relays Monitor")
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=GRAY)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Grid config
        self.window.columnconfigure(0, weight=3)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=3)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=5)
        self.window.rowconfigure(2, weight=5)

        # Draw grid
        self.navbar = Navbar(master=self.window, height=1)
        self.navbar.grid(row=0, column=2)

        self._draw_relays_grid()
        self.upper_relays = [getattr(self, f"relay_{i + 1}") for i in range(3)]

        # Listen for events
        self._configure_gui_events()
        self._configure_pin_events()
        self._configure_navbar_events()

        # Timer
        self._start_timer()

        # On close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.fullscreen = False

        self._maximize()
        # self.window.overrideredirect(1)

    def _maximize(self):
        """Maximize window"""
        self.window.attributes('-fullscreen', True)
        self.fullscreen = True
    
    def _minimize(self):
        """Minimize window"""
        self.window.attributes('-fullscreen', False)
        self.window.geometry(WINDOW_SIZE)
        self.fullscreen = False

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self._maximize()
        else:
            self._minimize()

    def _draw_relays_grid(self):
        """Draws a grid with RelayBox components"""
        index = 0
        pins = [(8, 7), (10, 11), (12, 13), (16, 15), (18, 19)] # (input_pin, output_pin)
        for row in range(2):
            for column in range(3):
                if index < 5:
                    relay = RelayBox(
                        master=self.window, name=f"relay_{index+1}", text=f"Relay {index + 1}", 
                        fg_color=GRAY, led_size=self.screen_width // 14
                    )
                    relay.grid(row=row+1, column=column)
                    pin_manager = PinManager(input_pin=pins[index][0], output_pin=pins[index][1])
                    setattr(self, f"relay_{index + 1}", relay)
                    setattr(self, f"pin_manager_{index + 1}", pin_manager)
                index += 1

    def _configure_gui_events(self):
        """Configures events and callbacks"""
        self.relay_1.led.bind("<ButtonPress-1>", lambda e: self.update_watch(1))
        self.relay_2.led.bind("<ButtonPress-1>", lambda e: self.update_watch(2))
        self.relay_3.led.bind("<ButtonPress-1>", lambda e: self.update_watch(3))
        self.relay_4.led.bind("<ButtonPress-1>", lambda e: self.update_watch(4))
        self.relay_5.led.bind("<ButtonPress-1>", lambda e: self.update_watch(5))

    def _configure_pin_events(self):
        """Configures Pin Events"""
        self.pin_manager_1.add_event_detect("rising", lambda e: self.physical_button_pressed(1))
        self.pin_manager_2.add_event_detect("rising", lambda e: self.physical_button_pressed(2))
        self.pin_manager_3.add_event_detect("rising", lambda e: self.physical_button_pressed(3))
        self.pin_manager_4.add_event_detect("rising", lambda e: self.physical_button_pressed(4))
        self.pin_manager_5.add_event_detect("rising", lambda e: self.physical_button_pressed(5))
    
    def _configure_navbar_events(self):
        self.navbar.close_btn.configure(command=self.on_close)
        self.navbar.fullscreen_btn.configure(command=self.toggle_fullscreen)

    def _start_timer(self):
        """call for the first time the recursive backup function."""
        self._callback_time_logger()

    def _callback_time_logger(self):
        """Recursive callback for making time backups"""
        self.make_time_backup()
        self.timerid = self.window.after(BACKUP_INTERVAL, self._callback_time_logger)

    def on_close(self):
        """this will be executed when the window is closed"""
        quit_response = tk.messagebox.askyesno('Exit','Are you sure you want to exit?')
        if quit_response:
            backup_response = tk.messagebox.askyesno('Backup','Would you like to make a backup before you go?')
            if backup_response:
                self.make_time_backup()
            self.window.after_cancel(self.timerid)
            self.window.destroy()

    def make_time_backup(self):
        """Save the current record time of the relay."""
        for i in range(5):
            relay = getattr(self, f"relay_{i + 1}")
            relay.save_time()

    def stop_upper_relays(self, id: int = 100):
        """Stops all relays except the passed id"""
        for i in range(len(self.upper_relays)):
            if id - 1 != i:
                relay = self.upper_relays[i]
                relay.led.set_checked(False)
                relay.watch.stop()
    
    def stop_all_relays(self):
        """stop all relays"""
        for i in range(5):
            relay = getattr(self, f"relay_{i + 1}")
            relay.led.set_checked(False)
            relay.watch.stop()

    def update_watch(self, id: int = 1):
        """Updates the watch state given the relay id"""
        relay = getattr(self, f"relay_{id}")

        if id <= 3:
            self.stop_upper_relays(id)

        if relay.led.toggle():
            # Only if relay 4 is on, turn on other relays
            if self.relay_4.led.is_checked():
                relay.watch.start()

            if id == 4:
                relay.watch.start()
        else:
            relay.watch.stop()

        if not self.relay_4.led.is_checked():
            self.stop_all_relays()

        self.make_time_backup()

    def physical_button_pressed(self, id: int = 1, *args, **kwargs):
        """Callback for a physical event."""
        print("callback reached!")
        relay = getattr(self, f"relay_{id}")
        pin_manager = getattr(self, f"pin_manager_{id}")

        if id <= 3:
            self.stop_upper_relays(id)

        input_state = pin_manager.get_input_state()
        relay.led.set_checked(input_state)

        if relay.led.is_checked():
            # Only if relay 4 is on, turn on other relays
            if self.relay_4.led.is_checked():
                relay.watch.start()
                
            if id == 4:
                relay.watch.start()
        else:
            relay.watch.stop()

        if not self.relay_4.led.is_checked():
            self.stop_all_relays()

        self.make_time_backup()

    def run(self):
        """Executes the application loop."""
        self.window.mainloop()