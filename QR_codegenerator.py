# qrcode_generator.py

import qrcode

def generate_qrcode(num1,num2):
    # ترکیب اعداد به صورت یک رشته
    data = f"{num1},{num2}"

    # ایجاد QR Code
    qr = qrcode.make(data)

    # ذخیره QR Code به عنوان تصویر
    qr.save(f"QR/{num1}.png")
    print("QR Code در فایل 'qrcode.png' ذخیره شد.")

