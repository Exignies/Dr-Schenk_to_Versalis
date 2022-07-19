import winsound
import time
frequency = 2700  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency-200, duration)
time.sleep(0.5)
winsound.Beep(frequency, duration)