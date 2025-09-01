#This is a basic test where the ESP32 and DHT11 sensor will be measuring and sending data to a Google Firebase DB
#The code is based on MicroPython

from machine import Pin, I2C
import ssd1306big
import utime, dht
import network
import urequests
import gc
import ntptime

# --- WIFI CONFIG ---
SSID = 'YOUR WIFI NETWORK'
PASSWORD = 'YOUR PASSWORD'

led = Pin(2, Pin.OUT)
def conect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting ...")
    while not wlan.isconnected():                           #The LED is on until it connects to the wifi (visual reference)
        led.on()
        utime.sleep(0.5)
    led.off()					                                      #The LED is off when it establishes wifi connection
    print("You're connected! IP:", wlan.ifconfig()[0])
    
# --- TIME SYNCHRONIZATION  ---
def sync_time():
    try:
        ntptime.settime()                                   #The ESP32 establishes a connection to a NTP server to adquire the time 
        print("Synchronized time with NTP")
    except Exception as e:
        print("There is an error in the synchronization: ", e)
        
# --- FIREBASE CONFIG ---
FIREBASE_URL = "YOUR DATABASE URL.json"                     #Your URL should end with a JSON file which will be the one to get the data

# --- SENSOR CONFIG ---
s = dht.DHT11(Pin(16))

def call_dht():
    try:
        s.measure()
        temp = s.temperature()
        humd = s.humidity()
        print('T:', temp, '  H:', humd)
        return temp, humd
    except Exception as e:
        print("There is an error in the measurement: ",e)
        return None, None

# --- OLED ---                                               #The measurement will be displayed in an OLED display      
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
ssd1306big.oled = ssd1306big.SSD1306(128, 64, i2c)   

oled_on = True
button = Pin(32, Pin.IN, Pin.PULL_UP)                        #The button is used to turn on and turn off the display

def toggle_oled(pin):
    global oled_on
    oled_on = not oled_on

button.irq(trigger=Pin.IRQ_FALLING, handler=toggle_oled)


# --- SEND MESSAGE TO FIREBASE ---
def send_firebase(temp,humd,date_time):
    try:
        gc.collect()                                         #The memory is freed to perform the other tasks
        data = {
            "temperature":temp,
            "humidity":humd,
            "timestamp":date_time
            }
        res = urequests.post(FIREBASE_URL, json=data)
        print("The message is sent to the DB:", res.text)
        res.close()
    except Exception as e:
        print("There is an error sending the message: ", e)

# --- LOCAL .TXT FILE ---
def file_local(temp, humd, date_time):
    try:
        with open("measurementrecord.txt", "a") as f:
            f.write("Temp: {}C, Humd: {}%, DateTime: {}\n".format(temp, humd, date_time))
    except Exception as e:
        print("There is an error saving the file: ", e)
        
# --- TIMESTAMP FORMAT ---                                  #This format is based on: dd/mm/yyyy hh:mm:ss
def timestamp_legible():
    t = utime.localtime(utime.time()- 6*3600)               #Adjustment to UTC-6 (Change according to your time zone)
    return "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(t[2], t[1], t[0], t[3], t[4], t[5])    

# --- MAIN ---
print("Free memory:", gc.mem_free())
conect_wifi()
sync_time()


while True:
    temp, humd = call_dht()
    if temp is not None and humd is not None:
        date_time = timestamp_legible()
        if oled_on:
            #Measurement in the display
            ssd1306big.oled.fill(0)
            ssd1306big.display("Tmp:"+str(temp), ssd1306big.displayArray)
            ssd1306big.display("Hmd:"+str(humd), ssd1306big.displayArray[16:])  #Second row in the display
        
        #Send message to DB
        send_firebase(temp,humd,date_time)
        file_local(temp,humd,date_time)
        
    else:
        print("The message is not sent due to a measurement error")
        
    utime.sleep(5)                                          #Measuring and sending data every 5 seconds
