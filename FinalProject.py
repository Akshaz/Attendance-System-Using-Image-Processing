import sqlite3
import cv2
import os
import numpy as np
import datetime
import sys

"""
Start: 
def genMainWindow():
    Registration: registrationWindow()
    Take Attendance: selectSlotWindow()
    Display Attendance: displayAttendance()
"""

"""
Registration start: 
def registrationWindow():
    Submit: cameraWindow(NameEntry, IDEntry)
"""

"""
def takeAttendanceWindow(classStartTime, classEndTime):
    conn, cur = recognize()
    cur.execute("SELECT * FROM Attendance;")
    result = cur.fetchall()
    
    for i in result:
        hh = int(i[2].split(':')[0])
        mm = int(i[2].split(':')[1])
        sec = int(i[2].split(':')[2].split('.')[0])
        micro = int(i[2].split(':')[2].split('.')[1])
        if datetime.datetime.now().replace(hour = hh, minute = mm, second = sec, microsecond= micro)>=classStartTime and datetime.datetime.now().replace(hour = hh, minute = mm, second = sec, microsecond= micro)<=classEndTime:
            cur.execute("UPDATE Attendance SET Attend = 1 WHERE Val >=10 AND Id == \"{}\";".format(i[0]))
            conn.commit()
    
    conn.commit()
    conn.close()
    genMainWindow()
"""

"""
Select slot window:
def selectSlotWindow():
    def submitClicked():
        choice = variable.get()
        if choice == '1st':
            classStartTime = datetime.datetime.now().replace(hour = 8, minute = 30, second = 0, microsecond = 0)
            classEndTime = datetime.datetime.now().replace(hour = 10, minute = 00, second = 0, microsecond = 0)
        elif choice == '2nd':
            classStartTime = datetime.datetime.now().replace(hour = 10, minute = 5, second = 0, microsecond = 0)
            classEndTime = datetime.datetime.now().replace(hour = 11, minute = 35, second = 0, microsecond = 0)
        elif choice == '3rd':
            classStartTime = datetime.datetime.now().replace(hour = 11, minute = 40, second = 0, microsecond = 0)
            classEndTime = datetime.datetime.now().replace(hour = 1, minute = 10, second = 0, microsecond = 0)
        elif choice == '4th':
            classStartTime = datetime.datetime.now().replace(hour = 2, minute = 50, second = 0, microsecond = 0)
            classEndTime = datetime.datetime.now().replace(hour = 4, minute = 20, second = 0, microsecond = 0)
        takeAttendanceWindow(main, selectSlotWindowObjects, classStartTime, classEndTime)
"""

"""
def cameraWindow(NameEntry, IDEntry):
    
    name = NameEntry.get()
    NameEntry.destroy()
    id = int(IDEntry.get())
    IDEntry.destroy()
    
    for i in registrationWindowObjects:
        i.destroy()
    
    SmileLabel = tk.Label(main ,text = "Smile While Your Picture Is Taken!", font = ("Helvetica", 28), bg = 'yellow2')
    SmileLabel.pack(fill = tk.BOTH)
    
    WaitingLabel = imageCapture(name, id, main, SmileLabel)
    
    WaitingLabel.destroy()
    genMainWindow(main)

"""
"""
def cameraCapture(i, name, id):
    
    cap = cv2.VideoCapture(0)
    temp = i
    
    while(i < (temp+60)):
        ret, frame = cap.read()
        fileName = "{}+{}+{}.jpeg".format(name, id, i)
        cv2.imwrite(fileName ,frame)
        key = cv2.waitKey(1)
        
        if ord('q') == key:
            break
        i = i + 1
    
    cap.release()
    cv2.destroyAllWindows()
"""
"""
def imageCapture(id, name):
    os.chdir("Dataset")
    i = 0
    destinationFolder = name + "+" +str(id)
    
    if destinationFolder in os.listdir():
        os.chdir(destinationFolder)
        listOfFiles = os.listdir()

        if os.path.exists(".DS_Store"):
            os.remove('.DS_Store')
        
        for dir in listOfFiles:
            if i < int(dir.split("+")[2].split(".")[0]):
                i = int(dir.split("+")[2].split(".")[0])
        i=i+1
    
    else:
        os.makedirs(destinationFolder)
        os.chdir(destinationFolder)
    
    cameraCapture(i, name, id)
    os.chdir("../")    
    trainImage()
    return
"""
"""
def trainImage():
    
    faces = []
    ids = []
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    
    if os.path.exists(".DS_Store"):
        os.remove('.DS_Store')
    
    listOfFolders = os.listdir()
    
    for dir in listOfFolders:
        os.chdir(dir)
        
        if os.path.exists(".DS_Store"):
            os.remove('.DS_Store')
        
        id = os.getcwd()
        
        for images in os.listdir():
            img = cv2.imread(images)
            img = cv2.resize(img, (200, 200))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces.append(img)
            ids.append(int(id.split("+")[1]))
        os.chdir("../")
    
    os.chdir("../Trained Model")
    recognizer.train(faces, np.array(ids))
    recognizer.save("Trained.yml")
    os.chdir("../")
"""
"""
def recognize():
    
    conn, cur = generateList()
    cap = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("../Trained Model/Trained.yml")
    harcascadePath = "../haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath) 
    
    while(True):
        
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = faceCascade.detectMultiScale(gray, 1.2,5)
        
        for (x,y,w,h) in face:
            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w]) 
            cv2.putText(frame, str(Id)+" - "+str(conf),(x,y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
            cv2.imshow('Face Recognition Based Attendance System' ,frame)                                
            
            if(conf < 80):        
                if(cur.execute("SELECT * FROM Attendance WHERE ID == {};".format(Id))):
                    cur.execute("SELECT Val FROM Attendance WHERE ID == {};".format(Id))
                    result = cur.fetchall()
                    time = str(datetime.datetime.time(datetime.datetime.now()))
                    
                    if result[0][0] == 0:
                        cur.execute("UPDATE Attendance SET Val = {}, timeIn = \"{}\", timeOut = \"{}\" WHERE ID == {};".format(result[0][0]+1, time, time, Id))
                    else:
                        cur.execute("UPDATE Attendance SET Val = {}, timeOut = \"{}\" WHERE ID == {};".format(result[0][0]+1, time, Id))
                    conn.commit()

        key = cv2.waitKey(1)
        
        if ord('q') == key:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    os.chdir("../")
    
    return conn, cur
""" 
"""
def generateList():
    
    os.chdir("Dataset")
    if os.path.exists('.DS_Store'):
        os.remove('.DS_Store')
    listOfStudents = os.listdir()
    os.chdir("../Attendance")
    
    filename = str(datetime.datetime.date(datetime.datetime.now()))+'.db'
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    
    if os.path.exists(filename):
        
        cur.execute("CREATE TABLE Attendance(ID INTEGER, Val INTEGER, timeIn TEXT, timeOut TEXT, Attend INTEGER);")
        conn.commit()
        
        for IDS in listOfStudents:
            cur.execute("INSERT INTO Attendance VALUES ({}, {}, {}, {}, {});".format(int(IDS.split("+")[1]), 0, str(0), str(0), 0))
        conn.commit()
    
    conn.close()
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    return conn, cur
"""

"""
To check attendance: 
    os.chdir("Attendance")
    
    filename = str(datetime.datetime.date(datetime.datetime.now()))+'.db'
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Attendance;")
    result = cur.fetchall()
"""