import win32print
from PIL import Image, ImageWin
import win32ui
import win32con
import platform

def check_platform(name):
    os_name = platform.system()
    if name == os_name:
        return True
    else:
        return False

def print_image(image_data):
    if check_platform("Windows"):
        windows_print_image(image_data)
    elif check_platform("Linux"):
        linux_print_img(image_data)
    else:
        print("Unknown OS")

def windows_print_image(image_data):
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    
    printer_info = win32print.GetPrinter(hprinter, 2)
    printer_info['pDevMode'].Duplex = 1  # Set duplex mode if desired (0 for simplex, 1 for duplex)

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)
    
    hdc.StartDoc('My Document')
    hdc.StartPage()

    # Get the printer's DPI
    dpi = ImageWin.Dib(image_data).size

    # Calculate image position and size
    img_width, img_height = image_data.size
    page_width, page_height = hdc.GetDeviceCaps(110), hdc.GetDeviceCaps(111)  # 110 and 111 are width and height codes
    
    # Calculate position and size for centering the image on the page
    x = (page_width - img_width) // 2
    y = (page_height - img_height) // 2
    width, height = img_width, img_height

    # Draw the image
    hdc.StretchBlt((x, y, x + width, y + height), image_data, (0, 0, img_width, img_height), win32con.SRCCOPY)
    
    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()
    
    win32print.ClosePrinter(hprinter)

def linux_print_img(image_data):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = list(printers.keys())[0]  # Assumes the first printer is the default

    file_path = "/tmp/print_test.png"  # Temporary file path
    with open(file_path, 'wb') as file:
        file.write(image_data)

    conn.printFile(printer_name, file_path, "Print Job", {})
    print("Printing completed.")
