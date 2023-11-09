import qrcode
from io import BytesIO

unit_types = ['Floor Door','Floor Drawer']

def generate_qr_code(data, directory = None, box_size = 10, border = 3):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # Adjust version as needed (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,  # Adjust box size as needed
        border=border,     # Adjust border size as needed
    )

    # Add the data to the QR code instance
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    if directory:
        # Save the image to a file
        img.save(directory)
    else:
        return img