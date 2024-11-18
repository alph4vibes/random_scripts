import tkinter as tk
from tkinter import messagebox
import time
import threading
from datetime import datetime

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cooking Timer")
        self.root.geometry("400x300")
        self.root.config(bg="#2c3e50")

        # Font settings
        self.font = ('Verdana', 14)
        self.timer_font = ('Verdana', 36)

        # Initialize Timer values
        self.timer_running = False
        self.timer_end_time = None
        self.timer_duration = 0

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Cooking Timer", font=('Verdana', 20), fg="white", bg="#2c3e50")
        self.title_label.pack(pady=10)

        # Timer display
        self.timer_display = tk.Label(self.root, text="00:00", font=self.timer_font, fg="white", bg="#2c3e50")
        self.timer_display.pack(pady=10)

        # Timer control mode
        self.mode_label = tk.Label(self.root, text="Mode: Duration", font=self.font, fg="white", bg="#2c3e50")
        self.mode_label.pack(pady=5)

        # Time inputs for Duration mode
        self.duration_frame = tk.Frame(self.root, bg="#2c3e50")
        self.duration_frame.pack(pady=5)
        self.minutes_entry = tk.Entry(self.duration_frame, font=self.font, width=5)
        self.minutes_entry.grid(row=0, column=0, padx=5)
        self.minutes_entry.insert(0, "0")
        self.seconds_entry = tk.Entry(self.duration_frame, font=self.font, width=5)
        self.seconds_entry.grid(row=0, column=1, padx=5)
        self.seconds_entry.insert(0, "0")

        # Time inputs for End Time mode
        self.end_time_frame = tk.Frame(self.root, bg="#2c3e50")
        self.end_time_label = tk.Label(self.end_time_frame, text="End Time (HH:MM):", font=self.font, fg="white", bg="#2c3e50")
        self.end_time_label.grid(row=0, column=0)
        self.end_time_entry = tk.Entry(self.end_time_frame, font=self.font, width=10)
        self.end_time_entry.grid(row=0, column=1, padx=5)
        self.end_time_frame.pack_forget()

        # Timer buttons
        self.start_button = tk.Button(self.root, text="Start Timer", font=self.font, command=self.start_timer, bg="#27ae60", fg="white")
        self.start_button.pack(pady=10, side=tk.LEFT, padx=30)

        self.stop_button = tk.Button(self.root, text="Stop Timer", font=self.font, command=self.stop_timer, bg="#e74c3c", fg="white")
        self.stop_button.pack(pady=10, side=tk.RIGHT, padx=30)

        # Switch mode button
        self.switch_button = tk.Button(self.root, text="Switch to End Time", font=self.font, command=self.switch_mode, bg="#3498db", fg="white")
        self.switch_button.pack(pady=10)

    def start_timer(self):
        if self.timer_running:
            return
        
        if self.mode_label.cget("text") == "Mode: Duration":
            try:
                minutes = int(self.minutes_entry.get())
                seconds = int(self.seconds_entry.get())
                self.timer_duration = minutes * 60 + seconds
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for the duration.")
                return
        else:
            end_time_str = self.end_time_entry.get()
            try:
                end_time = datetime.strptime(end_time_str, "%H:%M")
                current_time = datetime.now()
                self.timer_end_time = current_time.replace(hour=end_time.hour, minute=end_time.minute,
                                                            second=0, microsecond=0)
                if self.timer_end_time < current_time:
                    self.timer_end_time += timedelta(days=1)
                self.timer_duration = int((self.timer_end_time - current_time).total_seconds())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid end time in HH:MM format.")
                return

        self.timer_running = True
        self.update_timer()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_timer(self):
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def switch_mode(self):
        if self.mode_label.cget("text") == "Mode: Duration":
            self.mode_label.config(text="Mode: End Time")
            self.duration_frame.pack_forget()
            self.end_time_frame.pack(pady=5)
            self.switch_button.config(text="Switch to Duration")
        else:
            self.mode_label.config(text="Mode: Duration")
            self.end_time_frame.pack_forget()
            self.duration_frame.pack(pady=5)
            self.switch_button.config(text="Switch to End Time")

    def update_timer(self):
        if self.timer_running:
            if self.timer_duration > 0:
                minutes, seconds = divmod(self.timer_duration, 60)
                self.timer_display.config(text=f"{minutes:02}:{seconds:02}")
                self.timer_duration -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.timer_display.config(text="00:00")
                messagebox.showinfo("Time's up!", "The timer has ended.")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

