import sqlite3
import cv2
import os
import numpy as np
import datetime
import qrcode
import tkinter as tk
import sys


def genMainWindow(main):
    mainWindowObjects = []
    Head = tk.Label(main, text = "Face Recognition Based Attendance System", height = 15, font=("Helvetica", 28), bg = 'hotpink')
    mainWindowObjects.append(Head)
    Registration = tk.Button(main, text = "Take Images",command = lambda : registrationWindow(main, mainWindowObjects), height = 5, width = 25)
    mainWindowObjects.append(Registration)
    Attendance = tk.Button(main, text= "Take Attendance", command = lambda : selectSlotWindow(main, mainWindowObjects), height = 5, width = 25)
    mainWindowObjects.append(Attendance)
    DisplayAttendance = tk.Button(main, text="Display Attendance", command = lambda : displayAttendance(main, mainWindowObjects), height = 5, width = 25)
    mainWindowObjects.append(DisplayAttendance)
    Quit = tk.Button(main, text="Quit", command = lambda : main.destroy(), height = 5, width = 25)
    mainWindowObjects.append(Quit)
    Head.pack(fill = tk.Y)
    Registration.pack(side = tk.LEFT, padx = 5)
    Attendance.pack(side = tk.LEFT, padx = 5)
    DisplayAttendance.pack(side = tk.LEFT, padx = 5)
    Quit.pack(side = tk.LEFT, padx = 5)


def registrationWindow(main ,mainWindowObjects):
    registrationWindowObjects = []

    for i in mainWindowObjects:
        i.destroy()

    Head = tk.Label(main, text = "Registration/Login", font = ("Helvetica", 26), bg = 'hot pink')
    registrationWindowObjects.append(Head)
    NameLabel = tk.Label(main, text = "Enter Name", font = ("Helvetica", 20), bg = 'steelblue')
    registrationWindowObjects.append(NameLabel)
    NameEntry = tk.Entry(main)
    registrationWindowObjects.append(NameEntry)
    IDLabel = tk.Label(main, text = "Enter ID", font = ("Helvetica", 20), bg = 'steelblue')
    registrationWindowObjects.append(IDLabel)
    IDEntry = tk.Entry(main)
    registrationWindowObjects.append(IDEntry)
    SubmitButton = tk.Button(main, text = "Submit", command = lambda : cameraWindow(main, NameEntry, IDEntry, registrationWindowObjects), height = 5, width = 25)
    registrationWindowObjects.append(SubmitButton)
    backButton = tk.Button(main, text = "Back", command = lambda : back(), height = 5, width = 25) 
    registrationWindowObjects.append(backButton)
    
    def back():
        for i in registrationWindowObjects:
            i.destroy()
        genMainWindow(main)
    
    Head.pack(pady = 25, fill = tk.X)
    NameLabel.pack(pady = 10, fill = tk.X, padx = 5)
    NameEntry.pack()
    IDLabel.pack(pady = 10, fill = tk.X, padx = 5)
    IDEntry.pack()
    SubmitButton.pack(padx = 120, side = tk.LEFT)
    backButton.pack(padx = 120, side = tk.RIGHT)
    

def takeAttendanceWindow(main, selectSlotWindowObjects, classStartTime, classEndTime):
    
    for i in selectSlotWindowObjects:
        i.destroy()

    conn, cur = recognize()
    timeNow, timeStop = generateQRCode()

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
    genMainWindow(main)


def selectSlotWindow(main, mainWindowObjects):
    
    selectSlotWindowObjects = []
    
    for i in mainWindowObjects:
        i.destroy()
    
    Head = tk.Label(main, text = "Slot Selection", font = ("Helvetica", 28), bg = 'hotpink')
    selectSlotWindowObjects.append(Head)
    variable = tk.StringVar()
    slotLabel = tk.Label(main, text = "Select Slot : ", width = '50', height = '5', bg = 'steelblue')
    selectSlotWindowObjects.append(slotLabel)
    choices = ['1st', '2nd', '3rd', '4th']
    slotDropDown = tk.OptionMenu(main, variable, *choices)
    slotDropDown.configure(width = '50', height = '5', background = 'skyblue')
    selectSlotWindowObjects.append(slotDropDown)
    variable.set(choices[0])
    backButton = tk.Button(main, text = 'Back', command = lambda:back(), bg = 'skyblue', height = 5, width = 25)
    selectSlotWindowObjects.append(backButton)
    submitButton = tk.Button(main, text = 'Submit', command = lambda : submitClicked(), bg = 'skyblue', height = 5, width = 25)
    selectSlotWindowObjects.append(submitButton)


    def back():
        for i in selectSlotWindowObjects:
            i.destroy()
        genMainWindow(main)


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
    
    Head.pack(pady = 10, fill = tk.X)
    slotLabel.pack(fill = tk.X, padx = 10, pady = 10)
    slotDropDown.pack(fill = tk.X, padx = 10, pady = 5)
    backButton.pack(pady = 5,side = tk.LEFT, padx=120, anchor = tk.W)
    submitButton.pack(pady = 5, side = tk.LEFT, padx=120, anchor = tk.W)


def cameraWindow(main, NameEntry, IDEntry,registrationWindowObjects):
    
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
    

def imageCapture(name, id, main, SmileLabel):
    
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
    
    SmileLabel.destroy()
    WaitingLabel = tk.Label(main, text = 'Images Taken! Please wait till images are processed', font = ("Helvetica", 28), bg = 'skyblue')
    WaitingLabel.pack(fill = tk.BOTH)
    
    trainImage()

    return WaitingLabel


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


def displayAttendance(main, mainWindowObjects):
    
    stringToDisplay = " "
    displayAttendanceObjects = []
    
    for i in mainWindowObjects:
        i.destroy() 
    
    os.chdir("Attendance")
    
    filename = str(datetime.datetime.date(datetime.datetime.now()))+'.db'
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Attendance;")
    result = cur.fetchall()
    
    Head = tk.Label(main, text = "Attendance Report", font =("Helvetica", 28), bg = 'hotpink')
    displayAttendanceObjects.append(Head)
    textLabel = tk.Label(main, text = "     Id     |     Present/Absent     ", font = ("Helvetica", 26), bg = 'steelblue')
    displayAttendanceObjects.append(textLabel)
    textBox = tk.Text(main, height = len(result), width = 100)
    displayAttendanceObjects.append(textBox)
    closeButton = tk.Button(main, text = "Close", command = lambda : close(), height = 3, width = 25)
    displayAttendanceObjects.append(closeButton)

    for i in range(0, len(result)):
        
        if result[i][4] == 0:
            stringToDisplay = stringToDisplay + "     " + str(result[i][0]) + "     |     Absent      \n"
        
        else:
            stringToDisplay = stringToDisplay + "     " + str(result[i][0]) + "     |     Present     \n"
    
    def close():
        
        for i in displayAttendanceObjects:
            i.destroy()
            conn.close()
        
        os.chdir("../")
        genMainWindow(main)

    textBox.delete(1.0, tk.END)
    textBox.insert(tk.END, stringToDisplay)
    Head.pack(pady = 10, fill = tk.X)
    textLabel.pack(pady = 10, padx = 5, fill = tk.X)
    textBox.pack(pady = 10, padx = 20)
    closeButton.pack(pady = 10, padx = 5)


def generateQRCode():
    
    timeNow = datetime.datetime.time(datetime.datetime.now())
    img = qrcode.make(timeNow)
    timeStop = timeNow.replace(minute = timeNow.minute+1)
    img.show()
    
    return timeNow, timeStop
    
    
main = tk.Tk(className = " Face Recognition Based Attendance System")
main.configure(background = 'skyblue')
main.geometry("950x700")
genMainWindow(main)
main.mainloop()

