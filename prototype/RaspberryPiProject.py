# import RPi.GPIO as GPIO
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import numpy as np
import os
import time
import pickle

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)

# creates window, makes window fullscreen, gets screen width and height for scaling
root = tk.Tk()
root.attributes("-fullscreen", True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

def windowQuit():
    # saves time data for each class using pickle library
    for stop_watch in stopWatches:
        with open(stop_watch.relayWithNumber + ".pickle", "wb") as f:
            stop_watch.timeList = [stop_watch.hours, stop_watch.minutes, stop_watch.seconds]
            pickle.dump(stop_watch.timeList, f)
    # closes the window
    root.destroy()

class stopWatch:
    def __init__(self, instanceNumber, inputPin, outputPin):
        self.on = False
        self.instanceNumber = instanceNumber
        self.relayWithNumber = "Relay " + str(self.instanceNumber)
        self.relayNumberDisplay = tk.Label()
        # Loads time data from .pickle files using pickle library if data is stored else time is 0
        if os.path.exists(self.relayWithNumber + ".pickle"):
            with open(self.relayWithNumber + ".pickle", "rb") as f:
                self.timeList = pickle.load(f)
            self.hours = self.timeList[0]
            self.minutes = self.timeList[1]
            self.seconds = self.timeList[2]
        else:
            self.hours = 0
            self.minutes = 0
            self.seconds = 0
        self.timeList = [self.hours, self.minutes, self.seconds]
        self.formatTime()
        self.stopwatchLabel = tk.Label(text = self.timeString, font = ("Arial", 60))
        self.inputPin = inputPin
        self.outputPin = outputPin
        # GPIO.setup(self.inputPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Set pin self.inputPin to be an input pin and set initial value to be pulled low (off)
        # GPIO.add_event_detect(self.inputPin, GPIO.RISING,callback=self.physicalButtonPressed)
        # GPIO.setup(self.outputPin, GPIO.OUT)
    
    # This function creates the stopwatch function, displays the time, and then saves the new time
    def update(self):
        self.seconds += 1
        if self.seconds >= 60:
            self.minutes += 1
            self.seconds = 0
        if self.minutes >= 60:
            self.hours += 1
            self.minutes = 0
        
        self.formatTime()
        
        self.stopwatchLabel.config(text = self.timeString)
        
        with open(self.relayWithNumber + ".pickle", "wb") as f:
            self.timeList = [self.hours, self.minutes, self.seconds]
            pickle.dump(self.timeList, f)
        
        self.updateTime = self.stopwatchLabel.after(1000, self.update)

    # This function formats the time, and pads the 0's if needed
    def formatTime(self):
        if self.hours > 99:
            self.hourString = f'{self.hours}'
        elif self.hours > 9:
            self.hourString = f'0{self.hours}'
        else:
            self.hourString = f'00{self.hours}'
        self.minuteString = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
        self.secondString = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
        self.timeString = self.hourString + ":" + self.minuteString + ":" + self.secondString

    # This function determines whether you are turning the button on or off when you press it
    def buttonPressed(self):
        if self.on == True:
            self.stopStopwatch()
        else:
            self.startStopwatch()
    
    def physicalButtonPressed(self, channel):
        if self.on == True:
            self.stopStopwatch()
        else:
            self.startStopwatch()
    
    # This function starts the stopwatch
    def startStopwatch(self):
        # If the stopwatch is greater than 3, it just call the update function to start stopwatch and change the button display
        if self.instanceNumber <= 3:
            # If it is <= 3, it will check if stopwatch 4 is on, if it is, it will start the stopwatch and turn off the other
            # 2 stopwatches, and then change the button display
            if stopWatch4.on == True:
                self.update()
                self.on = True
                self.button.config(text = "ON", bg = "green", activebackground = "green")
                # GPIO.output(self.outputPin, True)
                for stop_watch in threeStopWatches:
                    if stop_watch.on == True and stop_watch.instanceNumber != self.instanceNumber:
                        stop_watch.stopStopwatch()
            else:
                pass
        else:
            self.update()
            self.on = True
            self.button.config(text = "ON", bg = "green", activebackground = "green")
            # GPIO.output(self.outputPin, True)
    
    def stopStopwatch(self):
        self.stopwatchLabel.after_cancel(self.updateTime)
        self.on = False
        self.button.config(text = "OFF", bg = "red", activebackground = "red")
        # GPIO.output(self.outputPin, False)
        if self.instanceNumber == 4:
            for stop_watch in threeStopWatches:
                if stop_watch.on == True:
                    stop_watch.stopStopwatch()

stopWatch1 = stopWatch(1, 8, 7)
stopWatch2 = stopWatch(2, 10, 11)
stopWatch3 = stopWatch(3, 12, 13)
stopWatch4 = stopWatch(4, 16, 15)
stopWatch5 = stopWatch(5, 18, 19)

stopWatches = [stopWatch1, stopWatch2, stopWatch3, stopWatch4, stopWatch5]
threeStopWatches = [stopWatch1, stopWatch2, stopWatch3]

# Displaying the stopwatches and their elements(Relay #, stopwatch, and button) as well as the quit button
def displayStopwatches():
    x = 0
    y = 0
    for stop_watch in stopWatches:
        if stop_watch.instanceNumber <= 3:
            stop_watch.relayNumberDisplay = tk.Label(text=stop_watch.relayWithNumber, font=("Arial", 60))
            stop_watch.relayNumberDisplay.grid(row = 0, column = x, padx = screen_width/14)
            stop_watch.stopwatchLabel.grid(row = 1, column = x)
            stop_watch.button = tk.Button(text = "OFF", command = stop_watch.buttonPressed, height = 2, width = 4, bg = "red", font = ("Arial", 60), activebackground = "red")
            stop_watch.button.grid(row = 2, column = x)
            x += 1
        elif stop_watch.instanceNumber >= 4:
            stop_watch.relayNumberDisplay = tk.Label(text=stop_watch.relayWithNumber, font=("Arial", 60))
            stop_watch.relayNumberDisplay.grid(row = 3, column = y, padx = screen_width/14)
            stop_watch.stopwatchLabel.grid(row = 4, column = y)
            stop_watch.button = tk.Button(text = "OFF", command = stop_watch.buttonPressed, height = 2, width = 4, bg = "red", font = ("Arial", 60), activebackground = "red")
            stop_watch.button.grid(row = 5, column = y)
            y += 1
    saveLabel = tk.Label(text = "SAVE", font = ("Arial", 60))
    saveLabel.grid(row = 3, column = 2)
    andQuitLabel = tk.Label(text = "AND QUIT", font = ("Arial", 60))
    andQuitLabel.grid(row = 4, column = 2)
    quitButton = tk.Button(text = "QUIT", command = windowQuit, font = ("Arial", 60), width = 4, height = 2, bg = "gray", activebackground = "red")
    quitButton.grid(row = 5, column = 2)

displayStopwatches()

root.mainloop()