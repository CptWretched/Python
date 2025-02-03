#!/usr/bin/python
import sys
import os
import subprocess
import socket

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13b_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

#Find the OS Version
try:
    logging.info("Getting OS Version...")  
    output = subprocess.check_output(['grep', '-o', r'"[^"]*"', '/etc/os-release']).decode()
    os_version = output.strip().split('\n')[0].replace('"PRETTY_NAME=', '').strip('"')
except subprocess.CalledProcessError as e:  
    logging.info(f"Subprocess error: {e}")
    exit(1)

#Find the CPU Temp
try:
    logging.info("Getting CPU Temperature...")
    cpu_temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode().split('=')[1].strip().replace('C','')
except subprocess.CalledProcessError as e:
    logging.info(f"Subprocess error: {e}")
    exit(1)

#Find the IP Address
try:
    logging.info("Getting IP Address...")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
except subprocess.CalledProcessError as e:
    logging.info(f"Subprocess error: {e}")
    exit(1)

#Find the Host Name
try:
    logging.info("Getting Hostname...")
    host_name = subprocess.check_output(['hostname']).decode().strip()
except subprocess.CalledProcessError as e:
    logging.info(f"Subprocess error: {e}")
    exit(1)

#Find the NTP Server
try:
    logging.info("Getting NTP Server...")  
    output = subprocess.check_output(['grep', 'server', '/etc/ntp.conf']).decode('utf-8')
except subprocess.CalledProcessError as e:  
    print(f"Subprocess error: {e}")  
    exit(1)
ntpd_servers = output.splitlines()[0].split(' ')[1]

#Print the Info
try:
    logging.info("Test Run")
    
    epd = epd2in13b_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)

# Drawing on the image
    logging.info("Drawing")    
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    
# Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...") 
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
    HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 250*122
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
   
#Text
    drawry.text((10, 0), u'OS:', font = font20, fill = 0) 
    drawry.text((10, 20), u'IP Address:', font = font20, fill = 0) 
    drawry.text((10, 40), 'CPU Temp:', font = font20, fill = 0)
    drawry.text((10, 60), 'Host Name:', font = font20, fill = 0)
    drawry.text((10, 80), 'NTP:', font = font20, fill = 0)
#Outputs
    drawblack.text((45, 0), os_version, font = font18, fill = 0)
    drawblack.text((110, 20), ip_address, font = font20, fill = 0)
    drawblack.text((110, 40), cpu_temp, font = font20, fill = 0)
    drawblack.text((120, 60), host_name, font = font20, fill = 0)
    drawblack.text((55, 80), ntpd_servers, font = font20, fill = 0)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(5)

#    logging.info("Clear...")
#    epd.init()
#    epd.clear()
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13b_V4.epdconfig.module_exit(cleanup=True)
    exit()

