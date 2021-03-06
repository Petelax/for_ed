import http.client, urllib
import os
import glob
import time
import busio
import board
import adafruit_amg88xx
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

human = False

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    for row in amg.pixels:
        for pixel in row:
            if pixel >= 29:
                human = True
            if human == True and read_temp() >= 0:
                conn = http.client.HTTPSConnection("api.pushover.net:443")
                conn.request("POST", "/1/messages.json",
                            urllib.parse.urlencode({
                                "token": "aajaiutjvx1fwdqy15g2nqcp6av8dt",
                                "user": "usqmx1mv4pams23f4nq8igh5a7okzf",
                                "message": "There is a living being ",
                            }), {"Content-type": "application/x-www-form-urlencoded"})
                conn.getresponse()
