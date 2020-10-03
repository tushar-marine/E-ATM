from tkinter import *
from tkinter import filedialog
import sqlite3


# Functions
def insert():
    connect = sqlite3.connect("bank_database.db")
    c = connect.cursor()
    c.execute("INSERT INTO accounts (account_number, account_pin, customer_img, contact_number) VALUES (?, ?, ?, ?)", (accountNumberInput.get(),accountPinInput.get(),img, contactNumberInput.get()))

    connect.commit()
    connect.close()

    accountNumberInput.delete(0, END)
    accountPinInput.delete(0, END)
    contactNumberInput.delete(0, END)

def load():
    global img
    file = filedialog.askopenfilename(initialdir='/', title='Select an image', filetypes=((("JPG File"), ("*.jpg")), (("JPEG File"), ("*.jpeg")), (("PNG File"), ("*.png"))))
    #img = cv2.imread(file)
    with open(file,'rb') as f:
        img = f.read()


# Create a Window
root = Tk()
root.title("ATM Database")
root.iconbitmap("icon.ico")
root.geometry("500x500")

# Create a Database
connect = sqlite3.connect("bank_database.db")

# Create Cursor
c = connect.cursor()

# Create Table
c.execute("""CREATE TABLE if not exists accounts (
        account_number integer not null,
        account_pin integer not null,
        customer_img mediumblob not null,
        contact_number text not null
        )""")

# -----------------------
# Adding Data to Database
# -----------------------

# Calling UI Elements
accountNumberLable = Label(root, text="Enter Account Number")
accountNumberInput = Entry(root, width=50, borderwidth=2)
accountPinLable = Label(root, text="Enter Account Pin")
accountPinInput = Entry(root, width=50, borderwidth=2)
contactNumberLable = Label(root, text="Enter Your Contact Number")
contactNumberInput = Entry(root, width=50, borderwidth=2)
loadImg = Button(root, text="Select Image", width=20, height=2, bg="#2d5cf7", fg="white", command=load)
submitButton = Button(root, text="Insert to Table", width=20, height=2, bg="#2d5cf7", fg="white", command=insert)
accountNumberLable.pack(pady=20)
accountNumberInput.pack()
accountPinLable.pack(pady=20)
accountPinInput.pack()
contactNumberLable.pack(pady=20)
contactNumberInput.pack()
loadImg.pack(pady=20)
submitButton.pack(pady=20)

# Commit Changes
connect.commit()

# Close Connection
connect.close()

accountNumberInput.focus()
root.mainloop()