import cv2
import numpy as np

import queue
import threading
import os
import sys
import gc
import time, datetime
import psutil

import modbus_tk.defines as md
from modbus_tk import modbus_rtu
import serial


class getframe_detect():
    
    def __init__(self, plcport, video_path, x, y, w, h):

        self.video_path = video_path 
        self.x, self.y, self.w, self.h = x, y, w, h #ROI 1

        self.frame_count = 0
        self.frame_interval = 20
        self.frame_queue_1 = queue.Queue(1) #threading 1 queue
        
        self.log_val_trigger = False 
        self.lock = threading.RLock() #recursive lock
        self.p = sys.executable #restart script

        #set auto-reboot
        self.boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        self.reboot_time = str(self.boot_time + datetime.timedelta(hours=8)).split('.')[0]

        try:
            self.master = modbus_rtu.RtuMaster(serial.Serial(port=plcport, baudrate=9600, bytesize=8, parity='E',stopbits=1,xonxoff=0))
            self.master.set_timeout(1.0)
            self.master.set_verbose(True)
            self.readinfo = self.master.execute(2, md.READ_HOLDING_REGISTERS, starting_address=32, quantity_of_x=1)
            self.readinfo_tbd = self.master.execute(2, md.READ_HOLDING_REGISTERS, starting_address=33, quantity_of_x=1)

        except Exception as e:
            print('plc connect error:', e)
            time.sleep(5)
            os.execl(self.p, self.p, *sys.argv)

    def frame_capture(self):
        
        try:
            cap = cv2.VideoCapture(self.video_path)
        except Exception as e:
            print('camera link error:', e)
            os.execl(self.p, self.p, *sys.argv)

        print(self.car_no,'start reveive')
        print('reboot at:', self.reboot_time)

        if cap.isOpened():
            while cap.isOpened():
                current_time = datetime.datetime.now()
                current_time = str(current_time).split('.')[0]

                if current_time == self.reboot_time:
                    print('reboot')
                    os.system('shotdown -r')

                try:
                    ret, frame = cap.read()

                except Exception as e:
                    print("read frame error:",e)
                    os.execl(self.p, self.p, *sys.argv)

                cropped_frame = frame[self.y : self.y + self.h, self.x : self.x + self.w] #ROI
                gray_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_RGB2GRAY) #gray-scaled

                #frame process rate
                if self.frame_count % self.frame_interval == 0:
                    self.lock.acquire()
                    self.frame_queue_1.put(gray_frame)
                    self.lock.release()                    

                    print('-----')
                    print('frame no.',int(self.frame_count/20))

                self.frame_count += 1

                #restart the programm to handle camera lag
                if self.frame_count == 200:  
                    break  
            
            cap.release()
            gc.collect() #release pc memory

            try:
                os.execl(self.p, self.p, *sys.argv)
            except Exception as e:
                print('fatal restart error:',e)
                pass
        
        else:
            cap.open()

    def task_1(self):
    
        if self.frame_queue_1.empty() != True:
            with self.lock:
                frame = self.frame_queue_1.get()
            
            frame = cv2.medianBlur(frame, 5)

            # display
            # cv2.imshow("frame", gray_frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            # detection code 
                    
    # def task_2(self):

    #     if self.frame_queue_2.empty() != True:
    #         frame = self.frame_queue_2.get()


      