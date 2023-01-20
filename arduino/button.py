import pyfirmata
import time
import sys
sys.path.append("C:/Users/erenf/Desktop/Projects/Assistant-Home-System")
from face_recognition.faces import recognize


board = pyfirmata.Arduino("COM4")

it = pyfirmata.util.Iterator(board)
it.start()

board.digital[10].mode = pyfirmata.INPUT
board.digital[12].mode = pyfirmata.OUTPUT
board.digital[13].mode = pyfirmata.OUTPUT

while True:
    sw = board.digital[10].read()
    if sw is True:
        print("Button pressed")
        person = recognize()
        if person is not None:
            print(f"{person} geldi.")
            board.digital[13].write(1)
            time.sleep(1)
            board.digital[13].write(0)
        else:
            print("Kişi tanınmıyor.")
            board.digital[12].write(1)
            time.sleep(1)
            board.digital[12].write(0)
        time.sleep(0.5)
