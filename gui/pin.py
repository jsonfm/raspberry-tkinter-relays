from gui.logs import logger

try:
    import RPi.GPIO as GPIO
except:
    GPIO = None

if GPIO is not None:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
else:
    logger.warning("RPi.GPIO module not found!")


class PinManager:
    """A custom Pin Manger."""
    def __init__(self, input_pin: int = None, output_pin: int = None):
        self.input_pin = input_pin
        self.output_pin = output_pin
        self._setup_pins()
        
    def _print_warning_message(self):
        logger.warning("RPi.GPIO module not found!")

    def _setup_pins(self):
        """Configures the input and the output pins."""
        if GPIO is None:
            self._print_warning_message()
            return
        GPIO.setup(self.input_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 
        GPIO.setup(self.output_pin, GPIO.OUT)

    def set_output(self, value: bool = False):
        """Updates the output pin value."""
        if GPIO is None:
            self._print_warning_message()
            return
        GPIO.output(self.output_pin, value)
    
    def add_event_detect(self, event: str= "rising", callback = None):
        """Adds a callback to a certain event."""
        if GPIO is None:
            self._print_warning_message()
            return

        if event == "rising":
            GPIO.add_event_detect(self.input_pin, GPIO.RISING, callback=callback)
    
    def get_input_state(self) -> bool:
        """Returns the current input state."""
        if GPIO is None:
            self._print_warning_message()
            return False 
        input_state = GPIO.input(self.input_pin)
        return input_state
