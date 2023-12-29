import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QProgressBar, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt5.QtGui import QColor

import psutil

class DataUsageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Start a timer to update data usage periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data_usage)
        self.timer.start(1000)  # Update every 1 second

    def init_ui(self):
        self.setWindowTitle('Data Usage Viewer')
        self.setGeometry(100, 100, 400, 200)

        self.label_usage = QLabel('Data Usage:', self)
        self.label_speed = QLabel('Download Speed: 0.00 MB/s | Upload Speed: 0.00 MB/s', self)

        self.progressbar = QProgressBar(self)
        self.progressbar.setOrientation(Qt.Horizontal)  # Horizontal orientation
        self.progressbar.setMaximum(100)

        self.update_button = QPushButton('Update', self)
        self.update_button.clicked.connect(self.update_data_usage)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.label_usage)
        layout.addWidget(self.label_speed)
        layout.addWidget(self.progressbar)
        layout.addWidget(self.update_button)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

        # Initial data update
        self.update_data_usage()

        # Apply dark theme stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e; /* Dark background color */
                color: #ffffff; /* Text color */
            }
            QProgressBar {
                background-color: #2e2e2e; /* Darker background color for progress bar */
                border: 1px solid #4CAF50;
                border-radius: 5px;
                height: 15px;
                color: #4CAF50; /* Progress bar color */
            }
            QPushButton {
                background-color: #4CAF50; /* Button color */
                color: #ffffff; /* Button text color */
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Add fade-in animation
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)  # 0.5 seconds
        self.fade_in_animation.start()

    def update_data_usage(self):
        # Get the current data usage
        data_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        # Display data usage in MB
        data_usage_mb = data_usage / (1024 * 1024)
        self.label_usage.setText(f'Data Usage: {data_usage_mb:.2f} MB')

        # Update progress bar (assuming a maximum limit for demonstration purposes)
        max_data_limit = 1000  # Set your desired maximum data limit in MB
        progress_value = min(data_usage_mb / max_data_limit * 100, 100)
        self.progressbar.setValue(int(progress_value))

        # Calculate download and upload speeds
        download_speed = psutil.net_io_counters().bytes_recv / (1024 * 1024)
        upload_speed = psutil.net_io_counters().bytes_sent / (1024 * 1024)
        self.label_speed.setText(f'Download Speed: {download_speed:.2f} MB/s | Upload Speed: {upload_speed:.2f} MB/s')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataUsageViewer()
    window.show()
    sys.exit(app.exec_())
