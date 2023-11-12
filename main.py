import logging
import threading
import time
import queue
import serial
import PrinterManager
import QrCode
from database import Database
from datetime import datetime


def scanned_unit_type(scanned_data):
    DB.insert_data(table_name='units',data=(None,scanned_data,None,None,datetime.now()))
    insert_id = DB.select_data(table_name='units',columns='id',order=('id','DESC')) # Gets the last inseted value
    qr_code = QrCode.generate_qr_code(insert_id)
    PrinterManager.print_image(qr_code)

# Function to simulate a scan event
def simulate_scan():
    scanned_data = "scanned_unit_type,floor door"
    function_name,data = scanned_data.split(',')
    function_callable = globals()[function_name]
    
    function_callable(data)

def monitor_port(Port:serial.Serial,data_queue:queue.Queue):
    try:
        while True:
            # Read data from the COM port
            data = Port.readline().decode('utf-8').strip()  # Adjust encoding as needed
            if data:
                data_queue.put(data)  # Put the data into the queue
            
    except KeyboardInterrupt:
        # Close the COM port when interrupted by user
        ser.close()

#GLOBALS
DATA_WHITE_LIST = ['Floor Door','Floor Drawer']
DB = Database("database.db")
QR_PORT = ser = serial.Serial("COM8", baudrate=9600, timeout=1)  # Replace 'COM1' with the appropriate port name

# THREAD GENERATION
# Create a thread-safe queue for communication between threads
QR_Thread_Queue = queue.Queue()
read_thread = threading.Thread(target=monitor_port,args=(QR_PORT,QR_Thread_Queue), daemon=True)
read_thread.start()

# My Main Thread
while True:
    # Check if there is data in the queue
    if not QR_Thread_Queue.empty():
        qr_data = str(QR_Thread_Queue.get())
        qty,qr_code = qr_data.split(",")
        print(qr_data)
