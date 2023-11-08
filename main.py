import threading

# Define an event
scanner_event = threading.Event()

# Event handler function
def on_scan_complete(data):
    print(f"Scanned data: {data}")

# Function to simulate a scan event
def simulate_scan():
    scanned_data = "Sample QR Code Data"
    on_scan_complete(scanned_data)
    scanner_event.set()

# Start a thread to simulate a scan
scan_thread = threading.Thread(target=simulate_scan)
scan_thread.start()

# Wait for the event to be set (scan to complete)
scanner_event.wait()

print("Scan complete.")
