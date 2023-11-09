import threading
from datetime import datetime

unit_types = []

# Define an event
scanner_event = threading.Event()

# Event handler function
def on_scan_complete(data):
    print(f"Scanned data: {data}")

# Function to simulate a scan event
def simulate_scan():
    scanned_data = "floor 2 door"
    on_scan_complete(scanned_data)
    scanner_event.set()

# Start a thread to simulate a scan
scan_thread = threading.Thread(target=simulate_scan)
scan_thread.start()

# Wait for the event to be set (scan to complete)
scanner_event.wait()

print("Scan complete.")



then = datetime(2012, 3, 5, 23, 8, 15)        # Random date in the past
now  = datetime.now()                         # Now
duration = now - then                         # For build-in functions
duration_in_s = duration.total_seconds()      # Total number of seconds between dates

print(duration_in_s)