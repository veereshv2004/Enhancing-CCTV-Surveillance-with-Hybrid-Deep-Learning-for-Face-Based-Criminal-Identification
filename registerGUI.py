from tkinter import *
import shutil
from PIL import ImageTk, Image
import sqlite3
from tkinter import filedialog
import tkinter.messagebox as tmsg
from subprocess import call

# ------------------- FUNCTIONS -------------------

def callTrainer():
    call(["python", "trainer.py"])

# ✅ Validation function (only alphabets + spaces)
def is_valid_text(text):
    return text.replace(" ", "").isalpha()

def ask():
    value = tmsg.askquestion(
        "CFIS WARNING !",
        "Select all (*) mandatory fields.\n(name,gender,religion,crime,pic)\n\nProceed?"
    )
    if value == "yes":
        x = databaseEnter()
        if x == 1:
            tmsg.showinfo("Success", "New Face Recorded Successfully")
            root.destroy()
        else:
            tmsg.showerror("Error", "Only alphabets allowed in Name, Parents, Body Mark, Crime, Nationality")

def getid():
    conn = sqlite3.connect('criminal.db')
    cursor = conn.cursor()
    cursor.execute('select max(ID) from People')
    row = cursor.fetchone()
    return row[0] if row[0] else 1

def databaseEnter():
    name = Fullname.get().strip()
    father = Fathername.get().strip()
    mother = Mothername.get().strip()
    body = Bodymark.get().strip()
    crime = Crime.get().strip()
    nat = Nationality.get().strip()
    bl = blood.get()
    gender = gen.get()
    religion = rel.get()

    if bl == "Select Blood Group":
        bl = None
    if religion == "Select Religion":
        religion = None

    gen1 = "Male" if gender == 1 else "Female" if gender == 2 else ""

    # ✅ Validation condition (including nationality)
    if (name and crime and gen1 and nat and
        is_valid_text(name) and
        is_valid_text(nat) and
        (father == "" or is_valid_text(father)) and
        (mother == "" or is_valid_text(mother)) and
        (body == "" or is_valid_text(body)) and
        is_valid_text(crime)):

        conn = sqlite3.connect('criminal.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO People 
            (Name, Gender, Father, Mother, Religion, Blood, Bodymark, Nationality, Crime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, gen1, father, mother, religion, bl, body, nat, crime))

        conn.commit()

        x = getid()
        file = f"images/user.{x}.png"
        shutil.copy('temp/1.png', file)

        return 1
    else:
        return 0

def mfileopen():
    file1 = filedialog.askopenfilename()
    shutil.copy(file1, 'temp/1.png')

    image = Image.open('temp/1.png')
    image = image.resize((500, 500))
    photo = ImageTk.PhotoImage(image)

    label = Label(image=photo, width=500, height=500)
    label.image = photo
    label.place(x=740, y=140)

# ------------------- GUI -------------------

root = Tk()
root.geometry('1350x720')
root.state("zoomed")
root.title("Enhancing CCTV Surveillance with Hybrid Deep Learning for Face Based Criminal Identification")

# Variables
Fullname = StringVar()
Fathername = StringVar()
Mothername = StringVar()
Bodymark = StringVar()
Nationality = StringVar()
Crime = StringVar()
gen = IntVar()
rel = StringVar()
blood = StringVar()

# Image
image = Image.open("images.jpg")
photo = ImageTk.PhotoImage(image)
Label(image=photo, width=500, height=500).place(x=740, y=140)

# Title
Label(root, text="Enhancing CCTV Surveillance with Hybrid Deep Learning for Face Based Criminal Identification",
      width=87, font=("bold", 20), bg="#386184", fg="white").place(x=0, y=0)

Label(root, text="Registration Form",
      width=95, font=("bold", 16), bg="#180020", fg='white').place(x=70, y=42)

# Form Fields
Label(root, text="Name *", font=("bold", 12)).place(x=70, y=130)
Entry(root, width=50, textvar=Fullname).place(x=260, y=130)

Label(root, text="Father Name", font=("bold", 12)).place(x=70, y=180)
Entry(root, width=50, textvar=Fathername).place(x=260, y=180)

Label(root, text="Mother Name", font=("bold", 12)).place(x=70, y=230)
Entry(root, width=50, textvar=Mothername).place(x=260, y=230)

Label(root, text="Gender *", font=("bold", 12)).place(x=70, y=280)
Radiobutton(root, text="Male", variable=gen, value=1).place(x=260, y=280)
Radiobutton(root, text="Female", variable=gen, value=2).place(x=330, y=280)

Label(root, text="Religion *", font=("bold", 12)).place(x=70, y=330)
OptionMenu(root, rel, 'Hindu','Muslim','Buddhist','Christian','Sikh','Jain','Others').place(x=260, y=325)
rel.set('Select Religion')

Label(root, text="Blood Group", font=("bold", 12)).place(x=70, y=380)
OptionMenu(root, blood, 'A+','A-','B+','B-','AB+','AB-','O+','O-','Not known').place(x=260, y=380)
blood.set('Select Blood Group')

Label(root, text="Body Mark", font=("bold", 12)).place(x=70, y=430)
Entry(root, width=50, textvar=Bodymark).place(x=260, y=430)

Label(root, text="Nationality *", font=("bold", 12)).place(x=70, y=480)
Entry(root, width=50, textvar=Nationality).place(x=260, y=480)

Label(root, text="Crime *", font=("bold", 12)).place(x=70, y=530)
Entry(root, width=50, textvar=Crime).place(x=260, y=530)

Label(root, text="Face Image *", font=("bold", 12)).place(x=70, y=590)
Button(root, text="Select", width=20, command=mfileopen).place(x=260, y=590)

Button(root, text='Register', width=15, font=("bold",10),
       bg='brown', fg='white', command=ask).place(x=250, y=650)

root.mainloop()