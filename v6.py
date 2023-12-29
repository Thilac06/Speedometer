import tkinter as tk
from tkinter import ttk
import psutil
import math

class Speedometer(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(width=200, height=200, bg='#F0F0F0', highlightthickness=0)
        self.create_oval(10, 10, 190, 190, outline='#B0B0B0', width=10)

        self.needle = self.create_line(100, 100, 100, 20, width=3, fill='#FF4500')
        self.speed_label = self.create_text(100, 160, text='', font=('Helvetica', 12, 'bold'), fill='#333333')

    def update_needle(self, angle, speed):
        # Convert angle to radians and calculate the needle position
        radian_angle = math.radians(angle)
        x = 100 + 80 * math.sin(radian_angle)
        y = 100 - 80 * math.cos(radian_angle)

        # Update the needle position
        self.coords(self.needle, 100, 100, x, y)

        # Update speed label
        self.itemconfig(self.speed_label, text=f'{speed:.2f} MB/s')

class DataUsageViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Data Usage Viewer')

        # Set font size for numbers
        font = ('Helvetica', 14)  # Change the font as needed

        # Calculate the size of the speedometer based on the window size
        window_size = min(self.winfo_screenwidth(), self.winfo_screenheight())
        speedometer_size = int(window_size * 0.3)

        self.geometry(f'{speedometer_size + 200}x{speedometer_size}')

        self.label_usage = tk.Label(self, text='Data Usage:', font=font)
        self.label_usage.grid(row=0, column=1, pady=(10, 0), sticky='w')

        self.label_speed = tk.Label(self, text='Download Speed: 0.00 MB/s | Upload Speed: 0.00 MB/s', font=font)
        self.label_speed.grid(row=1, column=1, pady=5, sticky='w')

        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate', style='TProgressbar')
        self.progressbar.grid(row=2, column=1, pady=10, sticky='w')

        self.update_button = tk.Button(self, text='Update', command=self.update_data_usage, font=font)
        self.update_button.grid(row=3, column=1, pady=5, sticky='w')

        self.quit_button = tk.Button(self, text='Quit', command=self.destroy, font=font)
        self.quit_button.grid(row=4, column=1, pady=(0, 10), sticky='w')

        self.speedometer = Speedometer(self, width=speedometer_size, height=speedometer_size)
        self.speedometer.grid(row=0, column=0, rowspan=5, padx=(10, 0), pady=(10, 0), sticky='e')

        # Initial data update
        self.update_data_usage()

        # Apply a clean and professional theme
        self.configure(bg='#F0F0F0')
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=font)
        self.style.configure('TLabel', font=font)

        # Add fade-in animation
        self.attributes('-alpha', 0)
        self.after(500, self.fade_in)

    def fade_in(self):
        alpha = self.attributes('-alpha')
        if alpha < 1:
            alpha += 0.1
            self.attributes('-alpha', alpha)
            self.after(50, self.fade_in)

    def update_data_usage(self):
        # Get the current data usage
        data_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        # Display data usage in MB
        data_usage_mb = data_usage / (1024 * 1024)
        self.label_usage.config(text=f'Data Usage: {data_usage_mb:.2f} MB')

        # Update progress bar (assuming a maximum limit for demonstration purposes)
        max_data_limit = 1000  # Set your desired maximum data limit in MB
        progress_value = min(data_usage_mb / max_data_limit * 100, 100)
        self.progressbar['value'] = int(progress_value)

        # Calculate download and upload speeds
        download_speed = psutil.net_io_counters().bytes_recv / (1024 * 1024)
        upload_speed = psutil.net_io_counters().bytes_sent / (1024 * 1024)
        self.label_speed.config(text=f'Download Speed: {download_speed:.2f} MB/s | Upload Speed: {upload_speed:.2f} MB/s')

        # Update speedometer needle angle based on download speed
        needle_angle = min(download_speed / 10, 180)  # Scale the angle as needed
        self.speedometer.update_needle(needle_angle, download_speed)

        # Schedule the next update after 1000 milliseconds (1 second)
        self.after(1000, self.update_data_usage)

if __name__ == '__main__':
    app = DataUsageViewer()
    app.mainloop()
