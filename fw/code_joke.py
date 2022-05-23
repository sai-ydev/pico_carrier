import sys
from time import sleep
import board
import busio
import sparkfun_qwiickeypad
import notecard

productUID = ""

i2c = busio.I2C(board.GP17, board.GP16)
# Create keypad object
keypad = sparkfun_qwiickeypad.Sparkfun_QwiicKeypad(i2c)
# Create relay object
card = notecard.OpenI2C(i2c, 0, 0, debug=True)

print("Blues Cellular Module Test")

# Check if connected
if keypad.connected:
    print("Keypad connected. Firmware: ", keypad.version)
else:
    print("Keypad does not appear to be connected. Please check wiring.")
    sys.exit()

print("Enter a phone number: ")

# button value -1 is error/busy, 0 is no key pressed
button = -1
payload = ""

req = {"req": "hub.set"}
req["product"] = productUID
req["mode"] = "periodic"
req["inbound"] = 120
req["outbound"] = 60
rsp = card.Transaction(req)

# while no key is pressed
while True:
    # request a button
    keypad.update_fifo()

    button = keypad.button
    # Display the button value
    if button and chr(button) != "#":
        payload += chr(button)
    elif chr(button) == "#" and len(payload) == 10:
        req = {"req": "note.add"}
        req["file"] = "numbers.qo"
        req["sync"] = True
        req["body"] = {"phone": payload}
        req = card.Transaction(req)
        payload = ""

    # wait a bit before trying again
    sleep(0.100)
