#import database
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from time import sleep

import requests
import base64
import json
import tkinter as tk
from tkinter import filedialog



def reqapi(fileName = 'saved_img.jpg'):
    IMAGE_PATH = fileName
    SECRET_KEY = 'sk_93d9b2e48cc1fcadc819984d'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)
    rjson = r.json()
    #print(json.dumps(r.json(), indent=2))
    result = rjson["results"]
    if len(result) == 0:
        print("No Plate detected")
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        #print(file_path)
        reqapi(file_path)
        
        return
    dataEntry(rjson["results"][0]["plate"])
    print("Plate: ", rjson["results"][0]["plate"])
    print("Region: ", rjson["results"][0]["region"])
    vehicle = rjson["results"][0]["vehicle"]
    print("Make: ", vehicle["make"][0]["name"])
    print("Make: ", vehicle["color"][0]["name"])
    print("Model: ", vehicle["make_model"][0]["name"])
    print("Year: ", vehicle["year"][0]["name"])
    print("*****************************************************")

def main():
    while True:
        
        key = cv2. waitKey(1)
        webcam = cv2.VideoCapture(0)
        sleep(2)
        while True:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'): 
                cv2.imwrite(filename='saved_img.jpg', img=frame)
                webcam.release()
                reqapi()
                break
            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break
        
########################################
import sqlite3
from datetime import datetime

conn = sqlite3.connect('parkingRite.db') 
c = conn.cursor()


def dataEntry(pid):
    now= datetime.now()
    date= now.strftime("%m/%d/%Y")
    time= now.strftime("%H:%M:%S")
    first_entries= "insert into parkingInfo (plate,time_in,time_out,served,price) \
    values(?,?,?,?,?)"
    
     

    if(checkPlateINdb(pid)==0):
        print("Welcome to Parking Right")
        c.execute(first_entries,(pid,time,"","No",0.0))
        conn.commit()
    else:
        print("Thank you for your business!\nPlease pay here!")
        enter_time = checkPlateINdb(pid)
        current_time = now.strftime("%H:%M:%S")
        print("Enter time:    ",enter_time)
        print("Exit time:     ", current_time)
        time_in = datetime.strptime(enter_time, '%H:%M:%S')
        time_out =datetime.strptime( current_time, '%H:%M:%S')
        time_delta = (time_out - time_in)
        print("Duration time: ", time_delta)
        duration = time_delta.total_seconds()
        price = "{0:.2f}".format(getPrice(duration))
        print("Price: $" + price)
        timeout_query="update parkingInfo set time_out='" +time+ "' , price = "
        timeout_query+= price + ",served = 'Yes' where plate= '" + pid + "' and served = 'No'"
        
        c.execute(timeout_query)
        conn.commit()
        
        
def getPrice(duration):
    if duration < 300:
        return 0.0;
    elif duration < 3600:
        return 10.0
    elif duration < 36000:
        return (duration / 3600) * 10.0
    else:
        return 100.0
    

def checkPlateINdb(mypid):

   myquery ="Select * from parkingInfo where plate='" + mypid + "'"
   myquery += " and served = 'No'"
   c.execute(myquery)
   result=c.fetchone()
   if result == None:
        return 0;
   else:
       print(result)
       return result[1];
        
        
    
        




if __name__ == "__main__":
    main()

