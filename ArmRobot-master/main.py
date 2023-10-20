from tkinter import ttk
from tkinter.ttk import Notebook

import options as options
import serial
import tkinter.messagebox
from tkinter import *


# GUI
win = Tk()
win.title('Panel sterowania')
win.geometry('900x800')
win.columnconfigure(1, weight=1)
win.rowconfigure(3, weight=1)

frame1 = Frame(win, pady=30, padx=30)
frame1.grid(column=0, row=0, columnspan=1)

frame2 = LabelFrame(win, pady=30, padx=30)
frame2.grid(column=1, row=1, columnspan=1, rowspan=3, sticky=N)

DEVICE = "COM1"
BAUD = 9600

#Metody
def configWindow():
    # Toplevel object which will
    # be treated as a new window
    winConfig = Toplevel(win)

    # sets the title of the
    # Toplevel widget
    winConfig.title("Konfiguracja połączenia")

    # sets the geometry of toplevel
    winConfig.geometry("800x500")

    # Tab control
    tabControl = ttk.Notebook(winConfig)

    # Tabs
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Common')
    tabControl.add(tab2, text='Serial Interface')
    tabControl.add(tab3, text='TCP/IP')

    tabControl.grid(row=0, column=0, sticky=NS, padx=30, pady=5)

    # Definicja frame
    frameC1 = LabelFrame(tab2, pady=30, padx=30, relief="groove", text="   Default Settings for   ")
    frameC1.grid(column=1, row=1, columnspan=1, sticky=W)

    frameC2 = LabelFrame(tab2, pady=30, padx=30, relief="groove", text="   Timeout   ")
    frameC2.grid(column=1, row=2, columnspan=1, sticky=W)

    frameC3 = LabelFrame(tab2, pady=30, padx=30, relief="groove", text="   Other Options   ")
    frameC3.grid(column=2, row=1, rowspan=2, sticky=NS)

    # Buttons Konfiguracja
    # Default Settings for
    RVBtn = Button(frameC1, text="RV-M1/RV-M2", width=25, height=2)
    RVBtn.grid(row=0, column=0, sticky=NS, padx=3, pady=3)

    AEBtn = Button(frameC1, text="A- and E- Types", width=25, height=2)
    AEBtn.grid(row=0, column=2, sticky=NS, padx=3, pady=3)

    # Timeout
    SendLabel = Label(frameC2, text="Send:")
    SendLabel.grid(row=0, column=0, sticky=W, padx=3, pady=3)

    ReceiveLabel = Label(frameC2, text="Receive:")
    ReceiveLabel.grid(row=1, column=0, sticky=W, padx=3, pady=3)

    SendE = Entry(frameC2)
    SendE.grid(row=0, column=1, sticky=W, padx=3, pady=3)

    ReceiveE = Entry(frameC2)
    ReceiveE.grid(row=1, column=1, sticky=W, padx=3, pady=3)

    Sec1Label = Label(frameC2, text="Seconds ( 1 - 30 )")
    Sec1Label.grid(row=0, column=2, sticky=W, padx=3, pady=3)

    Sec2Label = Label(frameC2, text="Seconds ( 1 - 120 )")
    Sec2Label.grid(row=1, column=2, sticky=W, padx=3, pady=3)

    # Other Options
    PortLabel = Label(frameC3, text="Port:")
    PortLabel.grid(row=0, column=0, sticky=W, padx=3, pady=3)

def robotConnect():
    global ser
    try:
        ser = serial.Serial(  # set parameters, in fact use your own :-)
            port="COM1",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        ser.isOpen()  # try to open port, if possible print message and proceed with 'while True:'
        print("Port is opened!")
        tkinter.messagebox.showinfo("Status", "Połączono")

    except IOError:  # if port is already opened, close it and open it again and print message
        ser.close()
        ser.open()
        print("Port was already open, was closed and opened again!")
        tkinter.messagebox.showinfo("Status", "Restart portu")

def robotSend():

    ser.write("GC\r".encode())

def robotReceive():
    print(ser.readline())

# Przycisk okna konfiguracji
btnConnect = Button(frame1, text="Konfiguracja", width=25, height=5, command=configWindow)
btnConnect.grid(row=0, column=0, sticky=NS, padx=3, pady=3)

# Przycisk połączenia
btnConnect = Button(frame1, text="Połącz", width=25, height=5, command=robotConnect)
btnConnect.grid(row=1, column=0, sticky=NS, padx=3, pady=3)

# Przycisk send
btnConnect = Button(frame2, text="Zamknij ramię", width=25, height=5, command=robotSend)
btnConnect.grid(row=0, column=0, sticky=NS, padx=3, pady=3)

# Przycisk Receive
btnConnect = Button(frame1, text="Receive", width=25, height=5, command=robotReceive)
btnConnect.grid(row=2, column=0, sticky=NS, padx=3, pady=3)


win.mainloop()