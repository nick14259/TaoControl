import requests
import random
import time

from urllib.parse import urljoin

HOST = 'http://192.168.1.102:8090'
PIN_ENDPOINT = 'devices/'
TEMP_ENDPOINT = 'devices/temp'
PINS = urljoin(HOST, PIN_ENDPOINT)
TEMP = urljoin(HOST, TEMP_ENDPOINT)

TRELAY = 'Temp. Relay'

def get_temp():
	d = requests.get(TEMP).json()
	f = d['temp_f']
	return f

def set_relay(state: str):
	for pin in requests.get(PINS).json():
		if pin['name'] == TRELAY:
			if pin['state'] != state:
				requests.patch(urljoin(PINS, str(pin['id'])), json={"state": state})

while True:
	time.sleep(6)
	d = get_temp()
	if d > 80:
		set_relay("off")
	if d < 79:
		set_relay("on")

