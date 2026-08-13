from tkinter import *
import datetime
import time
# Removed: import winsound # winsound is Windows-specific
from threading import *

# Added imports for cross-platform sound playback and generation
import math
import os
import struct
import wave
import pygame

root = Tk()
root.geometry("400x200")
root.title("Python Alarm Clock")

# Define the sound file path
TONE_FILE = os.path.join(os.getcwd(), "sound.wav")

# Flag used to stop both the sound and the checking loop
stop_flag = Event()

# --- Tkinter Variables and Widgets for Time Input ---
hour = StringVar(root)
minute = StringVar(root)
second = StringVar(root)

# Set default values to current time
current_time_dt = datetime.datetime.now()
hour.set(f"{current_time_dt.hour:02d}")
minute.set(f"{current_time_dt.minute:02d}")
second.set(f"{current_time_dt.second:02d}")

# Create OptionMenu widgets for hour, minute, second
hours_list = [f"{i:02d}" for i in range(24)]
minutes_list = [f"{i:02d}" for i in range(60)]
seconds_list = [f"{i:02d}" for i in range(60)]

Label(root, text="Set Alarm Time:").pack()

time_frame = Frame(root)
time_frame.pack()

hour_menu = OptionMenu(time_frame, hour, *hours_list)
minute_menu = OptionMenu(time_frame, minute, *minutes_list)
second_menu = OptionMenu(time_frame, second, *seconds_list)

hour_menu.pack(side=LEFT)
minute_menu.pack(side=LEFT)
second_menu.pack(side=LEFT)
# --- End Tkinter Widgets ---

def generate_tone(filename=TONE_FILE, freq=880.0, duration=1.0, volume=0.5, framerate=44100):
    """Generate a simple sine-wave beep and save it as a WAV file (only if missing)."""
    if os.path.exists(filename):
        return

    n_samples = int(framerate * duration)
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(framerate)
        for i in range(n_samples):
            t = i / framerate
            sample = volume * math.sin(2 * math.pi * freq * t)
            packed = struct.pack("<h", int(sample * 32767))
            wav_file.writeframesraw(packed)

def Threading():
    stop_flag.clear()          # reset in case it was set from a previous run
    t1 = Thread(target=alarm)
    t1.start()

def alarm():
    generate_tone() # Ensure the tone file exists

    # First, wait for the alarm time
    while not stop_flag.is_set():
        set_alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        if current_time == set_alarm_time:
            print("Time to Wake up")
            break # Exit the waiting loop, proceed to ringing

        time.sleep(1)

    # If stop_flag was set during waiting, exit
    if stop_flag.is_set():
        print("Alarm cancelled before ringing.")
        return

    # Now, alarm time is reached, start ringing
    pygame.mixer.init()
    pygame.mixer.music.load(TONE_FILE)
    pygame.mixer.music.play(loops=-1) # -1 = loop forever

    # Keep the thread alive while the music plays, until stop_flag is set
    while not stop_flag.is_set():
        time.sleep(0.2) # Small sleep to not busy-wait too much

    # Stop the music when stop_flag is set
    pygame.mixer.music.stop()
    print("Alarm stopped. Good morning! ☀️")

def stop_alarm():
    # Removed: winsound.PlaySound(None, winsound.SND_PURGE)
    stop_flag.set() # Signal the alarm thread to stop

Button(root, text="Set Alarm", font=("Helvetica 15"), command=Threading).pack(pady=10)
Button(root, text="Stop Alarm", font=("Helvetica 15"), command=stop_alarm, bg="red", fg="white").pack()

root.mainloop()
