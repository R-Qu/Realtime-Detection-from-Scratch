from realtime_detect import getframe_detect
import threading
import multiprocessing
import sys
import os


def main(plc_port, streaming, x_1, y_1, w_1, h_1):

    detection =  getframe_detect(plc_port, streaming, x_1, y_1, w_1, h_1)
    t0 = threading.Thread(target = detection.frame_capture)
    t1 = threading.Thread(target = detection.task_1)

    t0.setDaemon(True)
    t0.start()
    t1.start()
    t0.join(timeout=30)

    print('thread0-frame_capture timeout, check camera link')
    p = sys.executable
    os.execl(p, p, *sys.argv)

if __name__=='__main__':

    plc_port_0 = "/dev/ttyUSB0"
    streaming_0 = "rtsp://username:passward@192.168.1.1:554//Streaming/Channels/1" 
    x_1_0, y_1_0, w_1_0, h_1_0 = 99,99,99,99

    detect_0 = main(plc_port_0, streaming_0, x_1_0, y_1_0, w_1_0, h_1_0)
    p0 = multiprocessing.Process(target=detect_0)
    # p1=multiprocessing.Process(target=detect_1)
    
    p0.start()
    # p1.start()


   
