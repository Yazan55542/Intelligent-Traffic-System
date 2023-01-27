import easyocr
import cv2 
import time
import matplotlib.pyplot as plt
import numpy as np
import imutils
from PIL import Image

url = "C:\\Users\\lenovo\\Desktop\\7.jpeg"
lie_data = cv2.CascadeClassifier('C:\\Users\\lenovo\\Desktop\\JUNIOR\\plat_number.xml')
im = Image.open(url)
img = cv2.imread(url)
def detect_number(im):
    temp = img
    number = lie_data.detectMultiScale(img,1.2)
    print("Number plate detected:" + str(len(number)))
    for numbers in number:
        print("k")
        (x,y,w,h) = numbers
        cv2.rectangle(temp, (x,y), (x+w,y+h), (0,255,0), 3)
        temp = im.crop((x,y,x+w,y+h)) 
    return temp

image = detect_number(im)
cv2.imwrite(r'C:\\Users\\lenovo\\55\\' + 'yazan.jpg', np.array(image))

time.sleep(5)
reader = easyocr.Reader(['ar'])
results = reader.readtext("C:\\Users\\lenovo\\55\\yazan.jpg") 

print(results)

text = ''
for result in results:
    text += result[1]+ ' '
    
print(text)

reader = easyocr.Reader(['en'])
results = reader.readtext("C:\\Users\\lenovo\\55\\yazan.jpg") 

print(results)

text = ''
for result in results:
    text += result[1]+ ' '
    
print(text)