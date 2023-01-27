import threading
import cv2
import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import msvcrt
import serial.tools.list_ports
import os
#import matplotlib.pyplot as plt

ip='rtsp://admin:admin12345@192.168.1.105:554' #define the IP Camera for Local GPS
path = r"C:\Users\lenovo\Desktop\b\new"
speed_limit = 0
bad_cars_counter = []
bad_cars_counter.append(1)
info = []
cars = []
bad_cars = []
daily_cars = []
daily_speed = []
monthly_cars = []
monthly_speed = []



serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = "COM" + str(4)
serialInst.open()

class Statistics:
      def __init__(self, date, speed, count):
          self.date = date
          self.speed = speed
          self.count = count
    
    
class CarData:
    
    
    def __init__(self, id, long, speed, date):
        self.id = id
        self.long = long
        self.speed = speed
        self.date = date
        self.pic = 0
        self.plate = 0
    
    def get_date(self):
        return self.date
    
    
    def set_pic(self, p):
        self.pic = p
        
    def get_pic(self):
        return self.pic

    def set_num_plate(self):
        if(self.pic == 0):
            print("There's no pic of This Car")
        else:
            print("will use moudle here")#-------------here will use the AI Module
            
    def get_num_plate(self):
        return self.plate

#def recor_video_street():
    


def record_for_week(s):
    
    start_time = s # Date of Staring The Program
    while(True):
        day_of_week = 1
        #----------------------For Record Video Of Street-----------------------------------------------------------------
        video = cv2.VideoCapture(1)
        if(video.isOpened() == False):
            print("Error reading video file")
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        size = (frame_width, frame_height)
        if(video.isOpened() == False):
            print("Error reading video file")
       # print(current_day)
        filee = path + "\\" +str(day_of_week) + ".avi"
        #os.remove(filee)
        result = cv2.VideoWriter(r'New\\'+str(day_of_week)+'.avi', cv2.VideoWriter_fourcc(*'MJPG'), 13, size)
        print("Now We Are In   "+str(day_of_week)+"   Of Week")
    #----------------------------------------------------------------------------------------------------------
        while(day_of_week != 8):
            ret, frame = video.read()
            if ret == True :
                result.write(frame)
            
            
            if((datetime.now()-start_time).seconds==50):
                start_time = datetime.now()
                result.release()
                day_of_week +=1
                if(day_of_week == 8):
                    break
                filee = path + "\\" +str(day_of_week) + ".avi"
                #os.remove(filee)
                result = cv2.VideoWriter(r'New\\'+str(day_of_week)+'.avi', cv2.VideoWriter_fourcc(*'MJPG'), 13, size)
                print("Now We Are In   "+str(day_of_week)+"   Of Week in recording")
                            
            
    #--------------------------------------------------------------------------------------------------------------        
            
    #-----------------------------------------------------------------------------------------        
            
                
            
        
def getting_data_from_arduino(s):
    #print("11111111")
    start_time = s # Date of Staring The Program
    while True:
       # print("2222222222")
        cars_in_day=0
        day_of_week = 1
        
        
        while day_of_week != 8:
            #print("333333333")
            data = serialInst.readline()
            data_ = data.decode('utf8')
            info.append(data_[0:1])
            info.append(data_[2])
            #info.append(time.ctime(time.time()))
            info.append(datetime.now())
            if (len(info)%3 ==0 ):
               # print("4444444444444444")
                car = CarData(bad_cars_counter[0],info[len(info)-3],info[len(info)-2],info[len(info)-1])
                #info.clear()
                if(int(car.speed) > speed_limit):
                   # print("5555555555555")
                    bad_cars.append(car)
                    bad_cars_counter[0] = bad_cars_counter[0] + 1
                    #print(car.id)
                    #print(bad_cars[0].date)
                   # print(type(bad_cars[0].date))
                    
            if(( datetime.now() - start_time ).seconds>=50):
                
                print("666666666666")
                start_time = datetime.now()
                for i in range(int(len(info)/3)):
                    cars_in_day += int(info[i*3])
                cars_in_day = cars_in_day/len(info)/3
                stat = Statistics(day_of_week, cars_in_day, len(info)/3)
                daily_cars.append(stat)
                info.clear()
                day_of_week +=1   
                print("Now We Are In   "+str(day_of_week)+"   Of Week in getting data from arduino")
        for i in range(len(daily_cars)):   
            #print("77777777777777") 
            print(f'There are {daily_cars[i].count} Cars in {daily_cars[i].date} of Week __With speed average {daily_cars[i].speed}')
        daily_cars.clear()
        
        
def getting_frame_from_video(s):
    reciver_counter = 0
    print(s)
    ssstart_time = s + timedelta(seconds=50)
    print(ssstart_time)
    #time.sleep(50)  
    do = 1
    
    while True:
        if datetime.now() >= ssstart_time:
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            day_of_week = 1
            while day_of_week != 8:
                if do == 1:
                    m = 0
                    
                    for i in range(reciver_counter, len(bad_cars)):
                        m += 1
                    # n = len(bad_cars)
                        #print(day_of_week)
                        d= bad_cars[i].date
                        #print(d)
                    # print(type(d))
                        #print(d.timestamp())
                        
                        video = cv2.VideoCapture(f'{path}\{day_of_week}.avi')
                        fps = video.get(cv2.CAP_PROP_FPS)
                        # file modification timestamp of a file
                        m_time = os.path.getmtime(f'{path}\{day_of_week}.avi')
                        # convert timestamp into DateTime object
                        #dt_m = datetime.fromtimestamp(m_time)
                        #print(m_time)
                        minutes = 0 
                        #print(minutes)
                        vv = int( m_time ) - int(d.timestamp())  
                        #print(vv)
                        seconds =  50 - int(vv)  
                        #print(seconds)
                        
                        #print('frames per second =',fps)
                        #m_time = os.path.getmtime(f'{path}\{day_of_week - 1}.avi')#########################بترجعلي تاريخ تعديل ملف الفيديو
                        frame_id = int(fps* seconds)
                        #print('frame id =',frame_id) 
                        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
                        ret, frame = video.read()
                        t_msec = 1000*(minutes*60 + seconds)
                        video.set(cv2.CAP_PROP_POS_MSEC, t_msec)
                        ret, frame = video.read()
                        bad_cars[i].set_pic(frame)
                        
                        cv2.imwrite(r'badcars\\'+str(bad_cars[i].id)+'.png', frame)
                        if(bad_cars[i].id == 5):
                            img_ = cv2.cvtColor(bad_cars[i].pic,cv2.COLOR_BGR2RGB)
                            
                            
                            cv2.imshow('frame', img_); cv2.waitKey(0)
                    print("ccccccccccccccccccccccccccccccccccccccccccccccccc")
                    do = 0
                    print((datetime.now() - ssstart_time ).seconds)
                if ( datetime.now() - ssstart_time ).seconds >= 50 :
                    print("Now We Are In   "+str(day_of_week)+"   Of Week in getting frames")
                    ssstart_time = datetime.now()
                    day_of_week +=1   
                    reciver_counter = reciver_counter + m
                    print(reciver_counter)
                    do = 1
        
        
        
        
        
if __name__ == '__main__':
    s = datetime.now()
    t1 = threading.Thread(target=record_for_week, args=(s,))
    t2 = threading.Thread(target=getting_data_from_arduino, args=(s,))
    t3 = threading.Thread(target=getting_frame_from_video, args=(s,))
    
    
    
    t2.start()
    t1.start()
    
    t3.start()
    
    
