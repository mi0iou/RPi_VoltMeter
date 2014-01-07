# RPi Volt Meter v1.0

# Copyright (C) 2014 Tom Herbison MI0IOU
# Email tom@asliceofraspberrypi.co.uk
# Web <http://www.asliceofraspberrypi.co.uk>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# import GUI module
from tkinter import *

#import quick2wire i2c module
import quick2wire.i2c as i2c

# import GPIO module
import RPi.GPIO as GPIO

# setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#define address for ADC chip
adc_address = 0x68

# setup i2c bus
bus = i2c.I2CMaster()

# Function to set address for ADC
def changechannel(address, adcConfig):
	bus.transaction(i2c.writing_bytes(address, adcConfig))
	return

# Function to get reading from ADC		
def getadcreading(address):
	h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
	while (s & 128):
		h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
	# shift bits to product result
	t = ((h & 0b00000001) << 16) | (m << 8) | l
	# check if positive or negative number and invert if needed
	if (h > 128):
		t = ~(0x020000 - t)
	return (t / 64000)

# Class definition for RPiVoltMeter application
class RPiVoltMeter:

        # Build Graphical User Interface
        def __init__(self, master):
                frame = Frame(master, bd=10)
                frame.pack(fill=BOTH,expand=1)
                #display voltage
                self.voltage = DoubleVar()
                voltdisplay = Label(frame, bg='white', textvariable=self.voltage, width=18)
                voltdisplay.grid(row=0, column=0)
                voltlabel = Label(frame, text='Volts')
                voltlabel.grid(row=0, column=1)
                # choose channel
                channelframe = LabelFrame(frame, text='Channel', labelanchor='n')
                self.channel = IntVar()
                g1 = Radiobutton(channelframe, text='1', variable=self.channel, value=0)
                g1.grid(column=0, row=0)
                g1.select()
                g2 = Radiobutton(channelframe, text='2', variable=self.channel, value=1)
                g2.grid(column=1, row=0)
                g3 = Radiobutton(channelframe, text='3', variable=self.channel, value=2)
                g3.grid(column=2, row=0)
                g4 = Radiobutton(channelframe, text='4', variable=self.channel, value=3)
                g4.grid(column=3, row=0)
                channelframe.grid(row=1, column=0)
                # Measure button to measure voltage
                measurebutton = Button(frame, text='Measure', padx=5, pady=9, command=self.measurevoltage)
                measurebutton.grid(row=1, column=1)

        # start frequency sweep
        def measurevoltage(self):  
                channel = int(self.channel.get())
                chip = adc_address
                address = (156 + (32 * channel))
                changechannel(chip, address)
                self.voltage.set(getadcreading(chip))
                
# Assign TK to root
root = Tk()

# Set main window title
root.wm_title('RPi Volt Meter')

# Create instance of class WobbyPi
app = RPiVoltMeter(root)

# Start main loop and wait for input from GUI
root.mainloop()


