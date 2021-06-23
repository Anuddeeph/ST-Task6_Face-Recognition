import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import ImageGrab
import smtplib
import pywhatkit
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass

path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def Sendemail():
    fromaddr = input("Enter your email address:")
    print("Hope you are using Gmail")
    password = getpass.getpass()
    toaddr = input("To email address: ") 
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Hey this is email for Task-6"
    body = "Hope you are fine we are just testing"
    msg.attach(MIMEText(body, 'plain'))
    filename = "./Images/face.jpg"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.send_message(msg)
    server.quit()

def Whtsappmsg():
    Number = input("Enter the number you want to send msg +91XXXXXXXXXX: ")
    MSG=input("What msg you want to send:")
    print("Enter the time when you want to send the msg in the following format 24 hours method")
    hour=int(input("Enter the hour: "))
    min=int(input("Enter the minute: "))
    print (hour, min)
    pywhatkit.sendwhatmsg(Number,MSG,hour,min)


def instanceA():
    print("Using ami-0a9d27a9f4f5c0efc")
    print("listing your subnets")
    os.system("aws ec2 describe-subnets | findstr SubnetId")
    subnet = input("Enter the subnet id:   ")
    print("listing your security groups")
    os.system("aws ec2 describe-security-groups | findstr GroupId")
    sg = input("Enter the security group:  ")
    number = input("Enter the number of instances you want to launch: ")
    keyname = "aws ec2 describe-key-pairs | findstr KeyName"
    os.system(keyname)
    keypair = input("Enter the key pair name you want to use for launching the instance: ")
    launch = "aws ec2 run-instances --image-id ami-0a9d27a9f4f5c0efc" + " " + "--count " + number + " " + "--instance-type t2.micro --key-name " + keypair + " " + "--security-group-ids " + sg + " --subnet-id " + subnet + " " + "| findstr  InstanceId"
    os.system(launch)


def ebs():
    size = input("Enter the size without the keyword gb: ")
    region = input("which region : ")
    ebsc = "aws ec2 create-volume --volume-type gp2 --size " + size + " --availability-zone " + region
    os.system(ebsc)

def attach():
    os.system("aws ec2 describe-volumes | findstr VolumeId ")
    vlmid = input("Enter the volume id you want to attach: ")
    os.system("aws ec2 describe-instances | findstr InstanceId ")
    instance = input("Enter the instance id: ")
    attaching = "aws ec2 attach-volume --volume-id " + vlmid + " --instance-id " + instance + " --device /dev/sdf"
    os.system(attaching)

def Linux():
    while True: 
        print('Below is the Menu just for you choose an appropriate option \n')
        print('AWS menu by th3gentleman..Mubin Girach')
        
        print('----------------------------------------')
        
        print('''
            To launch EC2 instance- Press E \n'
            To create EBS volume- Press V \n'
            To attach EBS volume to your instance- Press A \n'
            To exit from this program -Press X \n'
            ''')
        print('---------------------------------------------------------')
        menu = input("Enter your input: ")

        if menu == "E":
            instanceA()
        elif menu == "V":
            ebs()
        elif menu == "A":
            attach()
        elif menu == "X":
            break
                
    
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
    
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

    if matches[matchIndex]:
        name = classNames[matchIndex].upper()
        #print(name)
        y1,x2,y2,x1 = faceLoc
        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        

        if name == "DEVASHISH":
           Whtsappmsg()
        
        elif name == "MUBIN":
            cv2.imwrite("./Images/face.jpg", img)
            Sendemail()

        elif name == "ANUDEEP":
            Linux()
    
        break
    
    
    



 
            

            

        
           

       
        

