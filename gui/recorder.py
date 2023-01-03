import os
from gui.logs import logger


class Recorder:
    """A custom time for save time records."""
    def __init__(self, folder="records", filename="relay.txt"):
        self.folder = folder
        self.filename = filename
        self.fullfilepath = os.path.join(folder, filename)
        self.time_str = "00:00:00"
    
    def load_file(self):
        """Loads initial time values."""
        if os.path.exists(self.fullfilepath):
            with open(self.fullfilepath, "r") as f:
                self.time_str = f.readline()
        else:
            logger.debug(f"file reading: file path {self.fullfilepath} does not exist!")
        return self.time_str
    
    def save(self, new_time_str: str):
        """Saves new time str values."""   
        if not os.path.exists(self.folder):
            logger.debug(f"file writing: file path {self.fullfilepath} does not exist! Creating it.")
            os.makedirs(self.folder)

        with open(self.fullfilepath, 'w') as f:
            f.write(new_time_str)
        return new_time_str
    
