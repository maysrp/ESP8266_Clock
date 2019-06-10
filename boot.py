import time
import ntptime
import network
import max7219
from machine import Pin,SPI
class clock:
    def __init__(self):
        self.ntp()
        self.dp()
        self.se=0
        self.time_zone=8 #your Time zone
        self.host='ntp.aliyun.com' #ntp server
    def net(self):
        wlan = network.WLAN(network.STA_IF) 
        wlan.active(True) 
        if not wlan.isconnected(): 
            wlan.connect('Your_wifi','Your_wifi_password')
    def dp(self):
        hspi = SPI(1, baudrate=10000000, polarity=0, phase=0)
        self.display = max7219.Matrix8x8(hspi,Pin(5),4)
    def ntp(self):
        self.net()
        ntptime.host=self.host
        try:
            ntptime.settime()
        except Exception as e:
            pass
    def text(self,texts):
        self.display.fill(0)
        self.display.text(texts[0:2],0,0,1)
        self.display.pixel(16,2,self.se)        
        self.display.pixel(16,4,self.se)        
        self.display.text(texts[2:4],17,0,1)
        self.se=0 if self.se==1 else 1
        self.display.show()
    def show_time(self):
        ti=time.localtime()
        h=ti[3]+self.time_zone if ti[3]+self.time_zone<24 else ti[3]+self.time_zone-24
        h=h if h>9 else '0'+str(h)
        m=ti[4]
        m=m if m>9 else '0'+str(m)
        s=ti[5]
        w=ti[6]+1
        self.h=ti[3]
        del ti
        time_string=str(h)+str(m)+'Day'+str(w)
        self.text(time_string)
    def show_time_s(self):
        ti=time.localtime()
        h=ti[3]+8
        h=h if h>9 else '0'+str(h)
        m=ti[4]
        m=m if m>9 else '0'+str(m)
        s=ti[5]
        s=s if s>9 else '0'+str(s)
        w=ti[6]+1
        self.m=ti[4]
        del ti
        time_string=str(h)+str(m)+'__'+str(s)
        self.text(time_string)
Clock=clock()

while 1:
    Clock.show_time_s()
    time.sleep(1)
    if Clock.m==10:
        Clock.ntp()