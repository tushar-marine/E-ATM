import cv2
import face_recognition
import sqlite3
from tkinter import *
from tkinter import ttk
import time
from tkinter import messagebox
from twilio.rest import Client
import random
from PIL import ImageTk, Image

# Unknown Face Warning
def warningOTP():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Invalid OTP", "You have inserted wrong OTP!!!\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# Unknown Face Warning
def warningUnkownFace():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("No Face", "Could not detect any face\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# Account Number Warning
def warningAccountNumber():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Invalid Account Number", "Invalid Account Number\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# Pin Warning
def warningPin():
    processing.pack_forget()
    processingText.pack_forget()

    response = messagebox.askquestion("Incorrect Pin", "Incorrect Pin\nTry Again?")
    if response == "yes":
        start()
    else:
        root.quit()

# OTP Verification
def verifyOTP():
    failedText.pack_forget()
    OTPText.pack_forget()
    OTPNumInput.pack_forget()
    OTPsubmitButton.pack_forget()

    processingText = Label(root, text="Verifying OTP Code")
    processing = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    # Showing in the Screen
    processingText.pack(pady=20)
    processing.pack()
    processing.start(10)

    # Matching OTP
    if otp == int(OTPNumInput.get()):
        processingText.pack_forget()
        processing.pack_forget()
        processing.after(1000, update)
    else:
        # Set error message to invalid OTP
        processing.after(1000, warningOTP)

# Asking for OTP
def callOTP():
    processing.pack_forget()
    processingText.pack_forget()

    global failedText
    global OTPText
    global OTPNumInput
    global OTPsubmitButton
    global otp


    # Generate and Send OTP
    account_sid = 'AC49ebed6f7a0afea5e102a515c51d35f6'
    auth_token = '810036a00726c0ad4fdbd25f03a0d234'
    client = Client(account_sid, auth_token)
    otp = random.randint(100000, 999999)
    #mobile = '+8801736783656'
    sms = client.messages.create(
        body='Please enter this OTP to continue. Your OTP is - ' + str(otp),
        from_='+12019037061',
        to= str(contactNumber)
    )
    sms.sid


    failedText = Label(root, text="Face Recognition Failed", fg="red")
    OTPText = Label(root, text="Enter Your OTP Code")
    OTPNumInput = Entry(root, width=50, borderwidth=2)
    OTPsubmitButton = Button(root, text="Log In", width=20, height=2, bg="#2d5cf7", fg="white", command=verifyOTP)
    failedText.pack(pady=30)
    OTPText.pack(pady=10)
    OTPNumInput.pack()
    OTPsubmitButton.pack(pady=10)

#Face Authentication
def faceAuthentication():

    # Get video footage
    global faceFramesEncoded
    faceFramesEncoded = []
    totalDist = []
    face1 = []
    video = cv2.VideoCapture(0)

    # set footage length to 5 seconds
    endTime = time.time() + 15
    while time.time() < endTime:
        status, frame = video.read()
        # Converting resized original image into RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encode image frame
        frameEncode = face_recognition.face_encodings(frame)
        # Get face location(top, right, bottom, left)
        faceLoc = face_recognition.face_locations(frame)

        for ef, fl in zip( frameEncode, faceLoc):
            if len(face1) == 0:
                face1.append(ef)
            dist = face_recognition.face_distance(face1, ef)

            # if any human face found, get the distance from base image
            if len(dist) > 0:
                totalDist.append(dist[0])
                faceFramesEncoded.append(ef)

                top, right, bottom, left = fl
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4)
            # Show the video
            cv2.imshow('Live Video', frame)
            cv2.waitKey(1)

    video.release()
    cv2.destroyAllWindows()

    if len(totalDist)<1:
        return False
    distance = sum(totalDist) / len(totalDist)
    if distance < 0.16:
        return False
    else:
        return True

#Face Recognition
def matchFace():

    img = cv2.imread('baseImage.jpg')
    # Change color to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Encode base image
    imgEncode = face_recognition.face_encodings(img)[0]

    # Compare with video footage
    totalDist = []
    for ef in faceFramesEncoded:
        dist = face_recognition.face_distance([imgEncode], ef)
        # if any human face found, get the distance from base image
        if len(dist) > 0:
            totalDist.append(dist[0])

    if len(totalDist)<1:
        return False
    distance = sum(totalDist) / len(totalDist)

    if distance > 0.6:
        return False
    else:
        return True

# Function to read data from DB
def readDB():
    connect = sqlite3.connect("bank_database.db")
    c = connect.cursor()
    number = accountNumInput.get()
    sql = "SELECT * FROM accounts WHERE account_number = '{0}'"
    c.execute(sql.format(number))

    data = c.fetchone()
    if data is None:
        data = []
    else:
        with open('baseImage.jpg', 'wb') as f:
            f.write(data[2])
    connect.close()
    return data

# Function for authorized screen
def update():
    # Removing Elements from Screen after 3sec
    processing.pack_forget()
    processingText.pack_forget()

    # Calling UI Elements for account Options
    chcekAcount = Label(root, text="Choose Your Option", fg="black")
    balanceButton = Button(root, text="Check Balance", width=20, height=2, bg="#2d5cf7", fg="white")
    withdrawButton = Button(root, text="Withdraw Balance", width=20, height=2, bg="#2d5cf7", fg="white")
    transferButton = Button(root, text="Transfer Balance", width=20, height=2, bg="#2d5cf7", fg="white")
    # Showing in the Screen
    chcekAcount.pack(pady=15)
    balanceButton.pack(pady=10)
    withdrawButton.pack(pady=10)
    transferButton.pack(pady=10)

# Function of start screen
def next():
    global processing
    global processingText
    global contactNumber

    # Removing Elements from Screen after Button Clicked
    titleText.pack_forget()
    accountNumInput.pack_forget()
    accountPassInput.pack_forget()
    loginButton.pack_forget()

    # Calling UI Elements for Verifying Notice
    processingText = Label(root, text="Verifying Your Inputs")
    processing = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="indeterminate")
    # Showing in the Screen
    processingText.pack(pady=20)
    processing.pack()
    processing.start(10)

    # read data from db
    data = readDB()
    contactNumber = data[3]

    if len(data) > 0:
        pinDB = data[1]
        # Check if pin matched
        if pinDB == int(accountPassInput.get()):
            # Process image
            check = faceAuthentication()
            if check:
                result = matchFace()
                if result:
                    processing.after(1000, update)
                else:
                    # Set error message to face not matched
                    processing.after(1000, callOTP)
            else:
                # Set error message to face not matched
                processing.after(1000, warningUnkownFace)
        else:
            # Set error message to pin not matched
            processing.after(1000, warningPin)
    else:
        # Set error message to account not found
        processing.after(1000, warningAccountNumber)

# Functions to start authorization
def start():
    # Removing Elements from Screen after 3sec
    processing.pack_forget()
    processingText.pack_forget()

    global accountNumInput
    global accountPassInput
    global titleText
    global loginButton

    # Calling UI Elements
    titleText = Label(root, text="Enter Your Account Number & Password")
    accountNumInput = Entry(root, width=50, borderwidth=2)
    accountPassInput = Entry(root, width=50, borderwidth=2)
    loginButton = Button(root, text="Log In", width=20, height=2, bg="#2d5cf7", fg="white", command=next)

    # Showing in the Screen
    titleText.pack(pady=30)
    accountNumInput.pack(pady=10)
    accountPassInput.pack(pady=10)
    loginButton.pack(pady=20)

    accountNumInput.focus()

# Start the User Interface
root = Tk()
root.title("ATM Facial Recognition")
root.iconbitmap("Source.ico")
root.geometry("600x450")
# Calling UI Elements
logo = ImageTk.PhotoImage(Image.open("logo.png"))
my_img = Label(image=logo)
titleText = Label(root, text="Enter Your Account Number & Password")
accountNumInput = Entry(root, width=50, borderwidth=2)
accountPassInput = Entry(root, width=50, borderwidth=2)
loginButton = Button(root, text="NEXT", width=20, height=2, bg="#009B4B", fg="white", command=next)

# Showing in the Screen
my_img.pack(pady=30)
titleText.pack(pady=10)
accountNumInput.pack(pady=10)
accountPassInput.pack(pady=10)
loginButton.pack(pady=20)


accountNumInput.focus()
root.mainloop()
