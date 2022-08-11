from machine import Pin , PWM
import machine 
import time
morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....','I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.','Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-','Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-','5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}
slowhell = {'S': '00000100101010110101101010100100000', 'C': '00000111111000110001100011000100000','A': '00000111100010100101001011111000000','N': '00000111110001000100010001111100000', 'G': '00000111111000110101101011110000000', '7': '00000000011000101001001010001100000'}

callsign = 'SA7CNG' #callsign
qrss = 10 #define qrss speed in seconds
fskcw = 16000 #define offset, 16000 = 4Hz
slowheight = 15000 #10000pwm = 20Hz
slowlength = 0.5 #500ms per dot
txpin = 0 #define pin that starts tx
fskpin = 1 #define pin that PWM fsk

pwm = PWM (Pin(fskpin)) # start PWM on pin 10
pwm.freq (1000) # set PWM frequency at 100Hz
pwm.duty_u16 (0) # duty 0% (65535/2)

start = Pin(txpin, Pin.OUT) #define TX-start pin
start.value(0) #stop transmitter
time.sleep(qrss) #stabilization time

for i in range(len(callsign)): #print callsign with slowhell
    buffer = slowhell[callsign[i]]
    duty = 0
    for x in range(34):
        if '1' in buffer[x]:
            start.value(1) #start transmitter
            pwm.duty_u16 (duty) #PWM 25% for 5Hz FSK
            time.sleep(slowlength)
            pwm.duty_u16 (0)
            start.value(0) #stopp transmitter
            duty = duty + slowheight
            if duty > slowheight * 4:
                duty = 0
        else:
            time.sleep(slowlength)
            duty = duty + slowheight
            if duty > slowheight * 4:
                duty = 0

time.sleep(qrss) #wait before sending fskcw
start.value(1) #start transmitter to send low line before first
pwm.duty_u16 (0) #set line low
time.sleep(qrss) #wait for one QRSS time unit before transmitting

for i in range(len(callsign)):
    buffer = morse[callsign[i]]
    start.value(1) #start transmitter
    for x in range(len(buffer)):
        if "." in buffer[x]:
            pwm. duty_u16 (fskcw) #PWM 25% for 5Hz FSK
            time.sleep(qrss)
            pwm. duty_u16 (0)
            time.sleep(qrss)
        else:
            pwm. duty_u16 (fskcw) #PWM 25% for 5Hz FSK
            time.sleep(qrss*3)
            pwm. duty_u16 (0)
            time.sleep(qrss)
    time.sleep(qrss*2) #delay between letters

start.value(0) #stopp tx
time.sleep(qrss*6) #stabilization time
machine.reset()
