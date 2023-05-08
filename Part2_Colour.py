#import statements
from machine import Pin, PWM
from utime import sleep
import rp2
import array,time
from rp2 import PIO, StateMachine, asm_pio
buzzer = PWM(Pin(18))
button = Pin(20, Pin.IN, Pin.PULL_UP)
button2 = Pin(21, Pin.IN, Pin.PULL_UP)
button3 = Pin(22, Pin.IN, Pin.PULL_UP)

#setting up the maker pico neopixel
NUM_LEDS = 1
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]

# creates a StateMachine with the ws2812 program, outputting on pin GP28 (Maker Pi Pico).
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(28))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

#premade with all the different notes for you to have a go with
tones = {
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}

#pre-defined songs
song_1 = ["E5", "E5", "P", "E5", "P", "C5", "E5", "P", "G5", "P", "P", "P", "G4", "P", "P", "P"]
song_2 = ["D5","E5","G5","E5","B5","B5","P","B5","B5","P","A5","A5","P","D5","E5","G5","E5","A5","A5","P","A5","A5","A5","G5","P","P","P"]

#tempo of the songs to make pitch correct
tempo = 320

# Calculate the duration of each note (in seconds)
note_duration = 60 / tempo

#what happens on each tone
def playtone(frequency):
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)
    changeLED(frequency)

#silencing the buzzer
def bequiet():
    buzzer.duty_u16(0)

def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            bequiet()
        else:
            playtone(tones[mysong[i]])
           
        time.sleep(note_duration)
    bequiet()

#getting all the buttons values, 1 is pressed 0 is released
def get_button():
    return not button.value()

def get_button2():
    return not button2.value()

def get_button3():
    return not button3.value()

#different function for each button
def button_press_function():
    ar[0] = 0
    sm.put(ar)
    playsong(song2)
    
def button2_press_function():
    ar[0] = 0
    sm.put(ar)
    playsong(song)
    
    
def button3_press_function():
    #iterating through all the rgb colours in a gradient
    while True:
        
        #TODO create function to smoothly implement a gradient to go through the colour wheel
            
            #in order to use other functions
            if get_button3() == 1:
                button_released_function()
                break
            elif get_button2() == 1:
                button_released_function()
                button2_press_function()
                break
            elif get_button() == 1:
                button_released_function()
                button_press_function()
                break

#changing the colours depending on the notes
def changeLED(frequency):
    
    #TODO: if statements for which note is pressed to change colour
    #Colours needed to define from given songs: 659, 587, 784, 880, 523, 392, 988 
        
        
        else:
            ar[0] = 0					# clear
            sm.put(ar)
    
    
#to stop 
def button_released_function():
    bequiet()
    ar[0] = 0
    sm.put(ar)


#main function
while True:
  
  if get_button() == 1:
    button_press_function()
  elif get_button2() == 1:
    button2_press_function()
  elif get_button3() == 1:
    button3_press_function()
  else:
    button_released_function()
    