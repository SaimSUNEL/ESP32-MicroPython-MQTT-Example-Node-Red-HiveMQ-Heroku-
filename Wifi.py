import network
import time
import gc
import ntptime
import machine
import urequests as requests
import ujson
wlan = None

OS_ERROR_COUNT = 0
def connectWifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    attempt_count = 0
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        wlan.connect("xxxx", "xxxxxx")
        while not wlan.isconnected():
            attempt_count += 1
            if attempt_count == 15:
                break
            print("Connecting... "+str(attempt_count))
            for i in range(1000):
                time.sleep_ms(1)
    gc.collect()
    if attempt_count == 15:
        return False
    else:
        print("******Connected to Wifi******")
        return True
def disconnectWifi():
    global wlan
    if wlan != None:
        if wlan.isconnected():
            wlan.disconnect()
        if wlan.active():
            wlan.active(False)
        wlan = None
        gc.collect()
def isConnectedWifi():
    if wlan == None:
        return False
    return wlan.isconnected()

def makeRequest(url, method="GET", header=None, data=None):
    global OS_ERROR_COUNT
    if isConnectedWifi() == False:
        return None
    try:

        if method == "GET":
            res = requests.get(url)
        elif method == "POST":
            post_data = ujson.dumps(data)
            res = requests.post(url, headers=header, data=post_data)
    
    except OSError as err:
        print("--- makeRequest : Os Error-*-")
        print(type(err))
        print(dir(err))
        print(err.args)
        if err.args[0] == -2:
            print("eksi iki")
            OS_ERROR_COUNT += 1
            print("OS error count : ", OS_ERROR_COUNT)
            if OS_ERROR_COUNT == 3:
                machine.reset()
        gc.collect();
        return None
    
    except Exception as err:
        print("makeRequest Err : ", err)
        gc.collect()
        return None
    gc.collect()
    OS_ERROR_COUNT = 0
    return res.json()