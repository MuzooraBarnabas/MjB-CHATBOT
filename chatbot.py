from tkinter import*
import africastalking
import tkinter
import tkinter as ttk
from tkinter import ttk, messagebox, filedialog, simpledialog, scrolledtext

import tkinter.ttk
from datetime import datetime, date, time

import mysql.connector
from mysql.connector import Error
import time, webbrowser, sqlite3
import time


today = date.today()
now = today.strftime("%a %d/%B/%Y")

timenow = (str(time.strftime('%H:%M:%S')))

msgtime = ("On "+now+" at "+timenow)

db = Tk()
db.title("MjB CHAT-BOT")
db.resizable(height=False, width=False)
db.iconbitmap("icon/logo.ico")
db.config(bg="lightgray")

#time
today = date.today()
now1 = today.strftime("%A, %d %B %Y")

time1 = ''

def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        db.title(now1+"  <•>  "+str(time2))     
        
    db.after(200, tick) 
tick()
#time


#-------logo---------

pic = PhotoImage(file="images/mjb.png")
Label(db, image=pic, bg="lightgray").pack()
#-------logo end----



#---------notebook--------
note= ttk.Notebook(db)
note.pack(anchor=N, padx=10, pady=10)


tab1 = Frame(note, bg="gray")
tab2 = Frame(note, bg="green")
tab3 = Frame(note, bg="sky blue")
tab4 = Frame(note, bg="gray")
tab5 = Frame(note, bg="gray")
tab6 = Frame(note, bg="gray")
tab7 = Frame(note, bg="gray")
tab8 = Frame(note, bg="gray")
tab1.pack(padx=10)
tab2.pack(padx=10)
tab3.pack(padx=10)
tab4.pack(padx=10)
tab5.pack(padx=10)
tab6.pack(padx=10)
tab7.pack(padx=10)
tab8.pack(padx=10)

note.add(tab1, text="LOGIN")
note.add(tab2, text="NEW ACCOUNT")
note.add(tab3, text="CHAT ROOM")
note.add(tab4, text="ALL SENT")
note.add(tab5, text="READ MESSAGE")
note.add(tab6, text="CONTACTS")
note.add(tab7, text="ABOUT ME")
note.add(tab8, text="ALL RECIEVED")
note.tab(1, state="hidden")
note.tab(2, state="hidden")
note.tab(3, state="hidden")
note.tab(4, state="hidden")
note.tab(5, state="hidden")
note.tab(6, state="hidden")
note.tab(7, state="hidden")

#------end--notebook---------

#---------------creating database for the chatbot
try:
	mydb = mysql.connector.connect(host="localhost", user="root", password="")
	cursor = mydb.cursor()

	#creating database
	cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot")
	

	#creating database tables
	mydb = mysql.connector.connect(host="localhost", user="root", password="", database="chatbot")
	cursor = mydb.cursor()
	print("Connected to the chatbot database!\n")

	table1 = "CREATE TABLE IF NOT EXISTS chatbot.signup(Id int(10) AUTO_INCREMENT PRIMARY KEY,FirstName VARCHAR(20) NOT NULL, LastName VARCHAR(20) NOT NULL, UserName VARCHAR(20) UNIQUE NOT NULL, DateOfBirth VARCHAR(20) NOT NULL, Email VARCHAR(30) UNIQUE NOT NULL, PhoneNumber VARCHAR(15), PassWord VARCHAR(10) NOT NULL)"
	table2 = "CREATE TABLE IF NOT EXISTS chatbot.chat_messages(MsgId int(10) AUTO_INCREMENT PRIMARY KEY, SenderEmail VARCHAR(30), RecieverEmail VARCHAR(30), Message Text(20000), Attachment VARCHAR(1000), DateAndTime VARCHAR(100))"
	table4 = "CREATE TABLE IF NOT EXISTS chatbot.mycontacts(Id int(10) AUTO_INCREMENT PRIMARY KEY, UserId int(10), Name VARCHAR(30), Email VARCHAR(100))"

	cursor.execute(table1)
	cursor.execute(table2)
	cursor.execute(table4)

except Exception as e:
	print(e)

def newA():		
	#ans = messagebox.askokcancel("MjB CHAT-BOT Informer", "Welcome friend to this amasing CHAT-BOT app\n\nSelect OK to create a new account now and enjoy the rest of our services!\n\n\tIT'S FREE TO USE THIS BOT.")
	note.tab(1, state="normal")
	note.select(1)
	#messagebox.showinfo("MjB CHAT-BOT Informer","To use this CHAT-BOT, you MUST be logged in!\n\nLOGIN NOW IF YOU ALREADY HAVE AN ACCOUNT!.")


#=====================fetch inbox==================
def delt(*args):	
	x = viewSent.get_children()
	for item in x:
	  viewSent.delete(item)

def fetchmsgs(*args):
	try:
		delt()
		mydb = mysql.connector.connect(host="localhost", user="root", password="", database="chatbot")
		cursor = mydb.cursor()

		fetchM = "SELECT RecieverEmail, Message, Attachment, DateAndTime FROM chat_messages WHERE SenderEmail=%s"
		fetchMval = (str(LoginEmail), )
		cursor.execute(fetchM, fetchMval)

		results = cursor.fetchall()
		for RecieverEmail, Message, Attachment, DateAndTime in results:
			print(RecieverEmail, Message, Attachment, DateAndTime)
			sender.config(state="normal")
			sender.delete("1.0", END)
			sender.insert("1.0", " To : "+str(RecieverEmail)+" \n",'big')
			sender.insert("2.0", "Msg : •••> "+str(Message),'color')
			sender.insert(END, "\n "+str(DateAndTime)+" \n",'bold_italics')
			sender.insert(END, "================================\n")
			sender.config(state="disabled")
		
		fetchMv = "SELECT MsgId, RecieverEmail, Message, Attachment, DateAndTime AS sent FROM chat_messages WHERE SenderEmail=%s"
		fetchMvalv = (str(LoginEmail), )
		cursor.execute(fetchMv, fetchMvalv)
		rows = cursor.fetchall()
		for sent in rows:
			viewSent.insert('', END, values=sent)


		fetchMr = "SELECT SenderEmail, Message, Attachment, DateAndTime FROM chat_messages WHERE RecieverEmail=%s"
		fetchMvalr = (str(LoginEmail), )
		cursor.execute(fetchMr, fetchMvalr)
		result = cursor.fetchall()
		for SenderEmail, Message, Attachment, DateAndTime in result:
			print(SenderEmail, Message, Attachment, DateAndTime)
			reciever.config(state="normal")
			reciever.delete("1.0", END)
			reciever.insert("1.0", " From : "+str(SenderEmail)+" \n",'big')
			reciever.insert("2.0", "Msg : •••> "+str(Message),'color')
			reciever.insert(END, "\n "+str(DateAndTime)+" \n",'bold_italics')
			reciever.insert(END, "================================\n")
			reciever.config(state="disabled")

	except Exception as e:
		raise e

#=====================login===================
def loadCont(*args):
	mycont = open("contacts/"+str(LoginId)+".txt","w")
	mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
	cursor = mydb.cursor()
	fetchc = "SELECT Name, Email FROM mycontacts WHERE UserId=%s "
	valc = (LoginId,)
	cursor.execute(fetchc, valc)
	results = cursor.fetchall()
	count = cursor.rowcount+1
	num = 1
	for (Name, Email) in results:
		mycont.write("Contact "+str(num))
		mycont.write("\n--------------------------------------------------")
		mycont.write("\nName : "+Name)
		mycont.write("\nEmail  : "+Email+"\n")
		mycont.write("-=============================-\n\n")
		num = num+1
	mycont.close()
	rCont = open("contacts/"+str(LoginId)+".txt","r")
	contL = rCont.read()
	contLI.config(state="normal")
	contLI.delete("1.0", END)
	contLI.insert(END, str(contL),'big')
	contLI.config(state="disabled")
	print(str(contL))

				

#===================load contacts============
Cotl=[("No contacts available..."), ]
def access(*args):
	try:
		#about me from the database
		global LoginId, UserName, PassWord, LoginNames, LoginEmail
		LoginId = "**no =="
		UserName=" null =="
		PassWord=" invalid**"
		LoginNames=""
		LoginEmail=""
		Email=""
		try:
			mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
			cursor = mydb.cursor()

			fetchr = "SELECT Id, UserName, Email, FirstName, LastName, PassWord FROM signup WHERE Email=%s AND PassWord=%s "
			valz = (str(userN.get()), str(passW.get()))
			cursor.execute(fetchr, valz)
			results = cursor.fetchall()
			for (Id, UserName, Email, FirstName, LastName, PassWord) in results:
				innF=str(FirstName[0])
				innL=str(LastName[0])
			if (str(userN.get())=="" and str(passW.get())==""):
				messagebox.showerror("Empty Creditials!","Email and Password are required!")
				userN.focus()
			elif (str(userN.get())==""):
				messagebox.showerror("Empty Username!","Email is required!")
				userN.focus()
			elif (str(passW.get())==""):
				messagebox.showerror("Empty Password!","Password is required!")
				passW.focus()
			elif (Email==str(userN.get()) and PassWord==str(PassWord)):				
				note.tab(2, state="normal")
				note.select(2)
				UseN.config(text=" USER-NAME :> "+str(UserName)+"  ")
				Phne.config(text=" STATUS :> Online"+"  ")
				note.tab(0, state="hidden")
				LoginId = Id
				LoginNames = FirstName+" "+LastName
				LoginEmail = Email
				inni.config(text=innF+innL, image="")
				fetchmsgs()
				loadCont()
			else:
				messagebox.showerror("Invalid Creditials!","Invalid Email or Password!")
				userN.focus()
				userN.delete(0, END)
				passW.delete(0, END)
		except Exception as e:
			print("An Error Occured : "+str(e))
	except Exception as e:
		print("An Error Occured : "+str(e))
	finally:
		contDl = []
		print(str(LoginId))
		fetchc = "SELECT Id, UserId, Name, Email FROM mycontacts WHERE UserId=%s "
		valc = (LoginId,)
		cursor.execute(fetchc, valc)
		results = cursor.fetchall()
		for (Id, UserId, Name, Email) in results:
			print(Email)
			contDl.append(str(Email))
		to.config(values=contDl)



f0 = LabelFrame(tab1, bg="gray")
f0.pack(side=RIGHT, padx=10)

f_0 = LabelFrame(tab1, bg="gray")
f_0.pack(side=LEFT, padx=10, pady=5)

logo = PhotoImage(file="images/logo.png")
Label(f_0, text="...CHAT PREVIEW...\nLOGIN OR SIGNUP TO ENJOY", image=logo, compound="center", font=("Lucida Handwriting",15,"bold"), fg="green").pack()


Label(f0, text="STARTING MjB CHAT-BOT", font=("Lucida Handwriting",15,"bold","underline"), fg="white", bg="gray").grid(row=0, column=0, pady=10, padx=10)
Label(f0, text="LOGIN TO CONTINUE", font=("Lucida Handwriting",10,"bold","underline"), fg="white", bg="gray").grid(row=1, column=0, pady=10, padx=10)

f = Frame(f0, bg="gray")
f.grid(row=2, column=0)

f2 = Frame(f0, bg="gray")
f2.grid(sticky=N)

Label(f, text="EMAIL ", font=("Lucida Handwriting",10,"bold"), fg="white", bg="gray").grid(row=0, column=0, pady=5, padx=10, sticky=W)
Label(f, text="PASSWORD ", font=("Lucida Handwriting",10,"bold"), fg="white", bg="gray").grid(row=1, column=0, pady=5, padx=10, sticky=W)


userN = ttk.Entry(f, font=("Verdana",15,), width=20, justify="center")
userN.grid(row=0, column=1, sticky=W, padx=10)
userN.bind("<Return>", access)

passW = ttk.Entry(f, font=("MS Outlook",15,), width=26, show="B", justify="center")
passW.grid(row=1, column=1, sticky=W, padx=10)
passW.bind("<Return>", access)

logN = ttk.Button(f2, text="LOGIN", command= access)
logN.grid(padx = 10, pady=5, sticky=E)

Label(f2, text="Don`t have an account?", justify="center", bg="gray", fg="white", font=("Lucida Handwriting",10,)).grid(row = 1,column=0,padx=5, sticky=W)

new = Button(f2, text="CREATE ONE", relief="flat", bg="gray", cursor="hand2", fg="lightblue",command=newA, font=("Lucida Handwriting",10,"underline"))
new.grid(row = 1,column=1, sticky=E, padx=5, pady=10)
#-----------------------login done--------------------------------------------

#-----------------------create account-------------------
def close2():
	note.tab(1, state="hidden")
	note.select(0)

x = Button(tab2, text=" X ", relief=FLAT, bg="red", fg="white", cursor="X_cursor", command=close2)
x.pack(side=RIGHT, anchor=N)

Label(tab2, text="SIGN UP NOW!", font=("Lucida Handwriting",15,"underline","bold"), fg="white", bg="green").pack()

F = Frame(tab2, bg="green")
F.pack(pady=5, anchor=S)



F1 = LabelFrame(F, bg="green")
F1.pack(side=LEFT, anchor=N,padx=5, pady=5)

F2 = LabelFrame(F, bg="green")
F2.pack(side=RIGHT, anchor=N, pady=5)



Label(F1, text="FIRST NAME  *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=0, column=0, pady=10, padx=10, sticky=W)
Label(F1, text="LAST NAME   *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=1, column=0, pady=10, padx=10, sticky=W)
Label(F1, text="USERNAME    *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=2, column=0, pady=10, padx=10, sticky=W)
Label(F1, text="DATE OF BIRTH *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=3, column=0, pady=10, padx=10, sticky=W)
Label(F2, text="PASSWORD    *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=2, column=0, pady=10, padx=10, sticky=W)
Label(F2, text="EMAIL       *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=0, column=0, pady=10, padx=10, sticky=W)
Label(F2, text="PHONE NUMBER *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=1, column=0, pady=10, padx=10, sticky=W)
Label(F2, text="PASSWORD    *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=2, column=0, pady=10, padx=10, sticky=W)
Label(F2, text="CONFIRM PASSWORD *", font=("Lucida Handwriting",10,"bold"), fg="white", bg="green").grid(row=3, column=0, pady=10, padx=10, sticky=W)



fname = ttk.Entry(F1, font=("Verdana",15,), width=20)
fname.grid(row=0, column=1, sticky=W, padx=10, pady=10)

lname = ttk.Entry(F1, font=("Verdana",15,), width=20)
lname.grid(row=1, column=1, sticky=W, padx=10, pady=10)

uname = ttk.Entry(F1, font=("Verdana",15,), width=20)
uname.grid(row=2, column=1, sticky=W, padx=10, pady=10)

values = ('01','02','03','04','05','06','07','08','09',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)

month = ['January',
		 'February',
		 'March',
		 'April',
		 'May',
		 'June',
		 'July',
		 'August',
		 'September',
		 'October',
		 'November',
		 'December'
		 ]


	
dobF = Frame(F1, bg="green")
dobF.grid(row=3, column=1, sticky=W, padx=10, pady=10)
Label(dobF, text="Date", font=("Lucida",8,"bold"), fg="white", bg="green").grid(row=0,column=0)
Label(dobF, text="Month", font=("Lucida",8,"bold"), fg="white", bg="green").grid(row=0,column=1)
Label(dobF, text="Year", font=("Lucida",8,"bold"), fg="white", bg="green").grid(row=0,column=2)
dob = ttk.Combobox(dobF, font=("Verdana",15,), width=2, values=values)
dob.grid(row=1, column=0)
month = ttk.Combobox(dobF, font=("Verdana",15,), width=8, values=month)
month.grid(row=1, column=1, padx=3, ipadx=5, pady=2)
yr = ttk.Combobox(dobF, font=("Verdana",15), width=4)
yr.grid(row=1, column=2)


y=[]

for x in range(1920,2081):
	y.append(x)
yr.config(values=y)

email = ttk.Entry(F2, font=("Verdana",15,), width=20)
email.grid(row=0, column=1, sticky=W, padx=10, pady=10)

phoneno = ttk.Entry(F2, font=("Verdana",15,), width=20)
phoneno.grid(row=1, column=1, sticky=W, padx=10, pady=10)

password= ttk.Entry(F2, font=("Verdana",15,), show="*", width=20)
password.grid(row=2, column=1, sticky=W, padx=10, pady=10)

Cpassword= ttk.Entry(F2, font=("Verdana",15,),show="*", width=20)
Cpassword.grid(row=3, column=1, sticky=W, padx=10, pady=10)

Label(F2, text="Note:  * fields are required", bg="green", fg="white", font=("Verdana",10,"italic")).grid(columnspan=2, pady=1)

btF = LabelFrame(tab2, bg="green")
btF.pack(padx=5, pady=5)

#submittng data into database
def submit():
	UserNameL=[]
	EmailL=[]
	mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
	cursor = mydb.cursor()

	nameTest = " SELECT UserName, Email FROM signup WHERE UserName=%s or Email=%s"
	val = (uname.get(), email.get())
	cursor.execute(nameTest, val)
	result = cursor.fetchall()
	for Id, UserName, Email in result:
		UserNameL.append(str(UserName))
		EmailL.append(str(Email))
	

	if (fname.get() and lname.get() and uname.get() and email.get() and phoneno.get() and password.get() and Cpassword.get()) =="":
		messagebox.showerror("Submit Error","All fields are required!")
		

	elif (uname.get() in UserNameL):
		messagebox.showerror("Submit Error","Sorry Username: '"+str(uname.get())+"' is already taken.")
		uname.delete(0, END)
		uname.focus()
	elif (email.get() in EmailL):
		messagebox.showerror("Submit Error","Sorry Email: '"+str(email.get())+"' is already taken.")
		email.delete(0, END)
		email.focus()

	elif("@" and ".com" not in email.get()):
		messagebox.showerror("Submit Error","Invalid email!")
		email.delete(0, END)
		email.focus()

	elif(password.get()!=Cpassword.get()):
		messagebox.showerror("Submit Error","Password do not match!")
		password.delete(0, END)
		Cpassword.delete(0, END)
		password.focus()
	else:
		try:
			mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
			cursor = mydb.cursor()


			stmt1 = "INSERT INTO chatbot.signup (FirstName, LastName, UserName, DateOfBirth, Email, PhoneNumber, PassWord) values (%s,%s,%s,%s,%s,%s,%s)"
			DOB = dob.get()+"/"+month.get()+"/"+yr.get()
			value = (fname.get(), lname.get(), uname.get(), DOB, email.get(), phoneno.get(), password.get())

			cursor.execute(stmt1, value)
			print("Signup Successfull!")

			messagebox.showinfo("MjB CHAT-BOT Informer", "MjB CHAT-BOT Account created successfully!\n\nLOGIN NOW!")
			note.tab(1, state="hidden")
			note.select(0)
		except Exception as e:
			raise e


bt1 = ttk.Button(btF,text="SUBMIT", command=submit, cursor="hand2")
bt1.grid(row=0, column=0, padx=5, pady=5)

#resetting signup entries
def reset():
	fname.delete(0, END)
	lname.delete(0, END)
	uname.delete(0, END)
	dob.delete(0, END)
	month.delete(0, END)
	yr.delete(0, END)
	email.delete(0, END)
	phoneno.delete(0, END)
	password.delete(0, END)
	Cpassword.delete(0, END)



bt2 = ttk.Button(btF,text="RESET", command=reset, cursor="X_cursor")
bt2.grid(row=0, column=1)
#-----------------------create account done-------------------



#--------------------------chat bot----------------
rframe = Frame(tab3, relief="flat", bd=1)
rframe.pack(anchor="e", fill=X)
Label(rframe, text="Welcome to the MjB CHAT-BOT: Add 'bmuzoora@gmail.com' to contacts and send any querries!", bg="orange").pack(fill=X)

Ff1 = LabelFrame(tab3, bg="skyblue")
Ff1.pack(side=LEFT, anchor=N, fill=BOTH)


lframe = Frame(Ff1, relief="groove", bd=1,)
lframe.pack(anchor="center", pady=5)


mainF = Frame(lframe, bg="gray")
mainF.grid(sticky=(W+E))

avatarF = LabelFrame(mainF, bg="red")
avatarF.pack(side=LEFT, fill=X)

info = Frame(mainF, bg="gray")
info.pack(side=RIGHT, fill=X)


avatar = PhotoImage(file="images/avatar.png")
inni = Label(avatarF, bg="sky blue",image=avatar, font=("Lucida",30,"bold"), text="MjB", compound="center", fg="blue")
inni.grid(sticky=W,rowspan=2)

UseN = Label(info, text="USER NAME : ", bg="gray",fg="white", compound="left", font=("Lucida Handwriting",10,"bold"))
UseN.grid(sticky=E, row=0)

Phne = Label(info, text="STATUS  : ", bg="gray",fg="white", compound="left", font=("Lucida Handwriting",10,"bold"))
Phne.grid(sticky=E, row=1)

msgFrame = Frame(Ff1, bg="skyblue", relief="raised", bd=4)
msgFrame.pack(pady=10, padx=10)


Label(msgFrame, text="SEND TO ", bg="sky blue", font=("Lucida Handwriting",10,"bold")).grid(row=0, column=0,pady=10, sticky=W)

Label(msgFrame, text="MESSAGE", bg="sky blue", font=("Lucida Handwriting",10,"bold")).grid(row=1, column=0,pady=10, sticky=W)

Label(msgFrame, text="ATTACH\nFILE", bg="sky blue", font=("Lucida Handwriting",10,"bold")).grid(row=2, column=0,pady=10, sticky=W)

def deactivate(*args):
	to.config(state="disabled")
def activate(*args):
	to.config(state="normal")

to = ttk.Combobox(msgFrame, width=35, font=("Lucida",10,), values=Cotl)
to.grid(row=0, column=1,pady=10, padx=5, ipadx=20, sticky=(W+E))
to.bind("<KeyPress>", deactivate)
to.bind("<KeyRelease>", activate)

chatmsg = scrolledtext.ScrolledText(msgFrame, height=4, width=40, bg="lightgray", font=("Lucida", 10,"bold"))
chatmsg.grid(row=1, column=1,pady=10, padx=5, sticky=(W+E))

textF = Frame(msgFrame, bg="sky blue")
textF.grid(row=2, column=1, padx=5, sticky=W+E)
attach = Entry(textF, width=38, font=("Lucida",10,"italic"), cursor="hand1")
attach.grid(sticky=E+W)
attach.insert(0, "Select file...")
attach.config(state="disabled")

#==================send messages part==============
types=[('ALL FILES','*.*'), ('WORD FILE','*.doc'), ('PDF FILE','*.pdf'), ('JPEG','*.jpeg;*.jpg'), ('PNG','*.png')]


def attac(*args):	
	path = filedialog.askopenfilename(title="Open file to send...",filetypes=types)
	attach.config(state="normal")
	attach.delete(0, END)
	attach.insert(0, str(path))
	attach.config(state="disabled")

def sendmessage(*args):
	Reciver="None"
	ReciverN="None"
	delt()
	if to.get()=="":
		messagebox.showerror("Sender Empty","Select who to send message please.")
		to.focus()
	elif chatmsg.get("1.0", "end")=="":
		messagebox.showerror("Message Empty","Please enter message to send!.")
		chatmsg.focus()
	else:	
		if attach.get()=="Select file...":
			path = "No File"
			print(path)
		elif attach.get()=="":
			path = "No File"
			print(path)
		else:
			path = (attach.get())
			print(path)
		try: 
			mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
			cursor = mydb.cursor()

			fetcRec = "SELECT Id, Name, Email FROM mycontacts WHERE Email=%s"
			RecVal = (str(to.get()),)
			cursor.execute(fetcRec,RecVal)
			resu = cursor.fetchall()
			for Id, Name, Email in resu:
				print(Id)
				Reciver = Id
				ReciverN = Email

			msgTosend = str(chatmsg.get("1.0", "end"))
			print(msgTosend)

			msgsql = "INSERT INTO chat_messages(SenderEmail, RecieverEmail, Message, Attachment, DateAndTime) VALUES(%s,%s,%s,%s,%s)"

			msgvalz = (LoginEmail, ReciverN, msgTosend, path, msgtime)

			cursor.execute(msgsql, msgvalz)
			print("Message sent")
			to.delete(0, END)	
			chatmsg.delete("1.0", "end")
			attach.config(state="normal")
			attach.delete(0, END)
			attach.config(state="disabled")
			attach.insert(0, "Select file...")
			to.focus()

		except Exception as e:
			raise e	
		finally:
			fetchmsgs()


def discar(*args):
		to.delete(0, END)	
		chatmsg.delete("1.0", "end")
		attach.config(state="normal")
		attach.delete(0, END)
		attach.insert(0, "Select file...")
		attach.config(state="disabled")
		to.focus()

load = ttk.Button(textF, text="Select", command=attac, cursor="plus")
load.grid(row=0, column=1,sticky=E)

btF= Frame(msgFrame, bg="skyblue")
btF.grid(row=3, columnspan=2)


sendP = PhotoImage(file="images/send.png")
Bt1 = Button(btF, text="SEND  ", relief="groove", compound=RIGHT, image=sendP, bg="blue", cursor="hand2", command=sendmessage, fg="white", font=("Lucida Handwriting",10,"bold"))
Bt1.grid(row=0, column=0, ipadx=10, pady=10, padx=10)

Bt2 = Button(btF, text="DISCARD", relief="groove", cursor="X_cursor", command=discar, bg="yellow", fg="red", font=("Lucida Handwriting",10,"bold"))
Bt2.grid(row=0, column=1, ipadx=10, pady=10, padx=10)

Ff2 = LabelFrame(tab3, bg="skyblue")
Ff2.pack(side=RIGHT, anchor=NW)

#-----------------actions------------------------------------------

def Back1():
	note.tab(3, state="hidden")
	note.select(2)

def viewallsent(*args):
	note.select(3)

#-----------------sent msgs--------------------
Label(tab4, text="ALL SENT MESSAGES", bg="gray",fg="white", font=("Lucida Handwriting",12,"bold","underline")).pack(side=TOP, pady=10)

treeF = LabelFrame(tab4,)
treeF.pack(pady=10, padx=10)

vF = LabelFrame(treeF)
vF.pack(side=RIGHT, fill=Y)

def repl(*args):
	for selected in viewSent.selection():
		Id,RECIEVER, MESSAGE, ATTACHMENT, DATE_TIME = viewSent.item(selected, 'values')
	to.delete(0,END)
	to.focus()
	chatmsg.delete("1.0",END)
	chatmsg.insert(END, str(MESSAGE))
	attach.config(state="normal")
	attach.delete(0,END)
	attach.insert(0,str(ATTACHMENT))
	attach.config(state="disabled")
	note.select(2)

 

cols=("Id","RECIEVER", "MESSAGE", "ATTACHMENT", "DATE_TIME")
viewSent = ttk.Treeview(treeF, column=cols, show="headings")
viewSent.pack(anchor=N, fill=BOTH)
scoreOUTh = Scrollbar(treeF,orient=HORIZONTAL, command=viewSent.xview)
scoreOUTh.pack(fill=X,anchor=S)
scoreOUTv = Scrollbar(vF, command=viewSent.yview)
scoreOUTv.pack(side=RIGHT, fill=Y)
viewSent.config(xscrollcommand=scoreOUTh.set, yscrollcommand=scoreOUTv.set)
viewSent.column(0, width=30)
viewSent.column(1, width=200)
viewSent.column(2, width=300)
viewSent.column(3, width=100)
viewSent.column(4, width=200)

for col in cols:
	viewSent.heading(col, text=col)
	
goBack = ttk.Button(tab4, text="GO BACK TO CHAT", command=Back1)
goBack.pack(anchor=SE, side=BOTTOM, pady=10, padx=10)


#-----------------view message--------------
def viewall(*args):
	note.select(4)
	global Attac
	for selected in viewSent.selection():
		Id, RECIEVER, MESSAGE, ATTACHMENT, DATE_TIME = viewSent.item(selected, 'values')

	try:
		conn= mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
		cursor = mydb.cursor()

		fetchMv = "SELECT RecieverEmail, Message, Attachment, DateAndTime FROM chat_messages WHERE MsgId=%s"
		fetchMvalv = (int(Id), )
		cursor.execute(fetchMv, fetchMvalv)
		rows = cursor.fetchall()
		for RecieverEmail, Message, Attachment, DateAndTime in rows:
			print(RecieverEmail, Message, Attachment, DateAndTime)
		viewallTo.config(text=str(RecieverEmail))
		viewallAt.config(text=str(Attachment))
		viewallmsg.config(text=str(Message))
		viewalldate.config(text=str(DateAndTime))
		Attac = str(Attachment)

	except Exception as e:
		raise e

def openpath(*args):	
	import os
	import webbrowser
	try:
		if True:
			os.startfile(str(Attac), "open")
		else:
			webbrowser.open_new((str(Attac)))
	except Exception as e:
		messagebox.showerror("MjB CHAT-BOT","Cannot load the specified path!")

def focus(*args):
	viewallAt.config(font=('arial',12,"bold","italic","underline"))

def leave(*args):
	viewallAt.config(font=('arial',12,"bold","italic"))

#note.select(7)

userL = Label(tab5, text="MjB CHAT-BOT MESSAGES.", font=('arial',18,"bold"), bg="lightblue", fg="blue", relief=FLAT, bd=2)
userL.pack(fill=X)
Hfr = Frame(tab5, relief=SOLID, bd=1, bg="black")
Hfr.pack(padx=20, pady=20)


darsh = Label(Hfr, font=('arial',15,"bold"),text="MESSAGE DETAILS", fg="white", bg="black")
darsh.pack(fill=X,)

headF = Frame(Hfr, bg="lightgray")
headF.pack(fill=X)



LHf = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
LHf.grid(row=0, column=0, sticky=E+S+N+W)

RHf = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
RHf.grid(row=0, column=1, sticky=E+S+N+W)

LHf11 = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
LHf11.grid(row=1, column=0, sticky=E+S+N+W)

RHf22 = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
RHf22.grid(row=1, column=1, sticky=E+S+N+W)

LHf1 = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
LHf1.grid(row=2, column=0, sticky=E+S+N+W)

RHf1 = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
RHf1.grid(row=2, column=1, sticky=E+S+N+W)

LHf12 = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
LHf12.grid(row=3, column=0, sticky=E+S+N+W)

RHf12 = LabelFrame(headF,bg="light gray", font=('times',12,"bold"),relief=SOLID, bd=1)
RHf12.grid(row=3, column=1, sticky=E+S+N+W)

Label(LHf, text="To", fg="black", bg="lightgray", font=('arial',12,"bold")).grid(sticky=(W))

Label(LHf11, text="Attachment", fg="black", bg="lightgray", font=('arial',12,"bold")).grid(row=1, sticky=(W))

Label(LHf1, text="Message", fg="black", bg="lightgray", font=('arial',12,"bold")).grid(row=0, sticky=(W))

Label(LHf12, text="Date and Time", fg="black", bg="lightgray", font=('arial',12,"bold")).grid(row=1)

viewallTo = Label(RHf, text="................................................................", fg="darkblue", bg="lightgray", font=('arial',12,"bold"))
viewallTo.grid(row=0, sticky=(W+N))

viewallAt = Label(RHf22, text="................................................................", fg="blue", bg="lightgray", font=('arial',12,"bold","italic"), cursor="hand2")
viewallAt.grid(row=1, sticky=(W+N))
viewallAt.bind("<1>",openpath)
viewallAt.bind("<Enter>",focus)
viewallAt.bind("<Leave>",leave)

viewallmsg = Label(RHf1, text="................................................................", fg="black", bg="lightgray", font=('arial',12,"bold"))
viewallmsg.grid(row=0, sticky=(W))

viewalldate = Label(RHf12, text="................................................................", fg="black", bg="lightgray", font=('arial',12,"bold"))
viewalldate.grid(row=1, sticky=(W))

def bac():
	note.tab(4, state="hidden")
	note.select(3)

ttk.Button(tab5, text=" BACK ", command=bac).pack(anchor=SE, side=BOTTOM, padx=10, pady=10)


def popup(event):
  id=viewSent.identify_row(event.y)
  if id:
    viewSent.selection_set(id)
    menu1.post(event.x_root, event.y_root)    

viewSent.configure(selectmode="extended")

menu1 = Menu(db, tearoff=0)
menu1.add_command(label=" View ", command=viewall)
menu1.add_command(label=" Forward ", command=repl)
menu1.add_command(label=" Delete ")
viewSent.bind("<Button-3>", popup)
viewSent.bind("<Button-1>", popup)

#-------------------------about-me----------------------
def Back4():
	note.tab(6, state="hidden")
	note.select(2)

global PassWord
PassWord="Not availalbe"
def Abt():	
	note.tab(6, state="normal")
	note.select(6)

	mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
	cursor = mydb.cursor()

	fetcC1 = ("SELECT FirstName, LastName, UserName, Email, PhoneNumber, PassWord FROM signup WHERE Id=%s")
	eml1 = (LoginId, )
	cursor.execute(fetcC1, eml1)
	res1 = cursor.fetchall()
	for FirstName, LastName, UserName, Email, PhoneNumber, PassWord in res1:
		insertName.config(text=str(FirstName)+" "+str(LastName))
		insertUName.config(text=str(UserName))
		insertEmail.config(text=str(Email))
		insertPhone.config(text=str(PhoneNumber))
		 



Label(tab7, text="MY DETAILS", bg="gray",fg="white", font=("Lucida Handwriting",12,"bold","underline")).pack(side=TOP, pady=10)

treeF = LabelFrame(tab7, bg="gray")
treeF.pack(pady=10, padx=10)
Label(treeF, text="FULL NAME    : ", bg="gray", font=("Lucida Handwriting",12,"bold",)).grid(row=0, column=0, sticky=W, pady=10, padx=10)
insertName = Label(treeF,text="Not availalbe", bg="gray",  font=("Lucida",12,"bold",), justify=LEFT)
insertName.grid(row=0, column=1, pady=10, padx=10, sticky=W)

Label(treeF, text="USERNAME     : ", bg="gray", font=("Lucida Handwriting",12,"bold",)).grid(row=1, column=0, sticky=W, pady=10, padx=10)
insertUName = Label(treeF,text="Not availalbe", bg="gray",  font=("Lucida",12,"bold",), justify=LEFT)
insertUName.grid(row=1, column=1, pady=10, padx=10, sticky=W)

Label(treeF, text="EMAIL            : ", bg="gray", font=("Lucida Handwriting",12,"bold",)).grid(row=2, column=0, sticky=W, pady=10, padx=10)
insertEmail = Label(treeF,text="Not availalbe", bg="gray",  font=("Lucida",12,"bold",), justify=LEFT)
insertEmail.grid(row=2, column=1, pady=10, padx=10, sticky=W)

Label(treeF, text="PHONE N☺     : ", bg="gray", font=("Lucida Handwriting",12,"bold",)).grid(row=3, column=0, sticky=W, pady=10, padx=10)
insertPhone = Label(treeF,text="Not availalbe", bg="gray",  font=("Lucida",12,"bold",), justify=LEFT)
insertPhone.grid(row=3, column=1, pady=10, padx=10, sticky=W)

Label(treeF, text="PASSWORD     : ", bg="gray", font=("Lucida Handwriting",12,"bold",)).grid(row=4, column=0, sticky=W, pady=10, padx=10)
insertPass = Entry(treeF, bg="gray", justify="center", font=("MS Outlook",8,), relief="flat")
insertPass.grid(row=4, column=1, pady=10, padx=10, sticky=W)
insertPass.insert(0, "Not availalbe")
insertPass.config(state="disabled", bg="gray")

def show(*args):
	insertPass.config(state="normal", bg="gray", font=("Lucida",8,))
	insertPass.delete(0, END)
	insertPass.insert(0, (str(PassWord)))
	insertPass.config(bg="gray", justify=LEFT)
	insertPass.config(state="disabled")

def hide(*args):
	insertPass.config(state="normal", bg="gray", font=("MS Outlook",8,))
	insertPass.delete(0, END)
	insertPass.insert(0, ("Not availalbe"))
	insertPass.config(bg="gray", justify=LEFT)
	insertPass.config(state="disabled")


showpass = ttk.Button(treeF, text="show")
showpass.grid(row=4, column=2, pady=10)
showpass.bind("<ButtonPress-1>", show)
showpass.bind("<ButtonRelease-1>", hide)

goBack = ttk.Button(tab7, text="GO BACK TO CHAT", command=Back4)
goBack.pack(anchor=SE, side=BOTTOM, pady=10, padx=10)

#-----------------add contact------------------
def close5():
	note.tab(5, state="hidden")

def open5():
	note.tab(5, state="normal")
	note.select(5)

x = Button(tab6, text=" X ", relief=FLAT, bg="red", fg="white", cursor="X_cursor", command=close5)
x.pack(side=RIGHT, anchor=N)

Label(tab6, text="MANAGE YOUR CONTACT LIST!", font=("Lucida Handwriting",15,"underline","bold"), fg="white", bg="gray").pack()

F = Frame(tab6, bg="gray")
F.pack(pady=5, anchor=S)



F1 = LabelFrame(F, bg="gray", text="ADD NEW", font=("Lucida",12,"bold"))
F1.pack(side=LEFT, anchor=N,padx=5, pady=5, fill=Y)

F2 = LabelFrame(F, bg="gray", text="YOUR CONTACTS", font=("Lucida",12,"bold"))
F2.pack(side=RIGHT, anchor=N, pady=5, fill=Y)



Label(F1, text="CONTACT NAME *", font=("Lucida",10,"bold"), fg="white", bg="gray").grid(row=0, column=0, pady=10, padx=10, sticky=W)
Label(F1, text="EMAIL       *", font=("Lucida",10,"bold"), fg="white", bg="gray").grid(row=2, column=0, pady=10, padx=10, sticky=W)

conName = ttk.Entry(F1, font=("Verdana",15,), width=25, justify="center")
conName.grid(row=1, column=0, sticky=W, padx=10)

conEmail = ttk.Entry(F1, font=("Verdana",15,), width=25, justify="center")
conEmail.grid(row=3, column=0, sticky=W, padx=10)

contLI = scrolledtext.ScrolledText(F2, height=10, width=50, relief="flat", bg="gray", fg="white")
contLI.grid(row=1, column=0)

contLI.tag_configure('big', font=('Verdana', 12, 'bold'), background="lightblue", foreground="blue")
contLI.tag_configure('color', foreground='black', font=('Lucida', 10), background="orange")
contLI.config(state="disabled")

btF = Frame(tab6, bg="gray")
btF.pack()

def cle():
	conName.delete(0, END)
	conEmail.delete(0, END)
	conName.focus()

def SaveC(*args):
	if conEmail.get()=="bmuzoora@gmail.com":
		conName.delete(0, END)
		conName.insert(0,"Barnabas")
	if conName.get()=="":
		messagebox.showerror("MjB CHAT-BOT Informer", "Contact Name cannot be empty!")
		conName.focus()
	elif conEmail.get()=="":
		messagebox.showerror("MjB CHAT-BOT Informer", "Contact Email cannot be empty!")
		conEmail.focus()
	elif ("@" and ".com" in conEmail.get()):
		try:
			contL=[]
			mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
			cursor = mydb.cursor()
			Email=""

			fetcC = ("SELECT UserId FROM mycontacts WHERE Email=%s")
			eml = (conEmail.get(), )
			cursor.execute(fetcC, eml)
			res = cursor.fetchall()
			for UserId in res:
				contL.append(UserId)

			if (conEmail.get()) not in contL:
				fetcC1 = ("SELECT Id,Email FROM signup WHERE Email=%s")
				eml1 = (conEmail.get(), )
				cursor.execute(fetcC1, eml1)
				res1 = cursor.fetchall()
				for Id, Email in res1:
					pass 
				if conEmail.get()!=str(Email):
					messagebox.showerror("MjB CHAT-BOT Informer", "Contact Email"+conEmail.get()+" Cannot be added since it has no account here!\nPlease Create its account and then add again!")
					conEmail.delete(0, END)
				else:
					try:
						addSql = "INSERT INTO  mycontacts(UserId, Name, Email) VALUES (%s, %s, %s)"
						valx = (LoginId, conName.get(), conEmail.get())
						cursor.execute(addSql, valx)
						messagebox.showinfo("MjB CHAT-BOT Informer", "Contact Added Successfully")
						loadCont()
						conName.delete(0, END)
						conEmail.delete(0, END)
					except Exception as e:
						raise e
					finally:
						contDl = []
						print(str(LoginId))
						fetchc = "SELECT Id, UserId, Name, Email FROM mycontacts WHERE UserId=%s "
						valc = (LoginId,)
						cursor.execute(fetchc, valc)
						results = cursor.fetchall()
						for (Id, UserId, Name, Email) in results:
							print(Email)
							contDl.append(str(Email))
						to.config(values=contDl)

			else:
				messagebox.showerror("MjB CHAT-BOT Informer", "Contact Email "+str(conEmail.get())+" already exists!\nPlease try again!")
				conEmail.delete(0, END)
				conEmail.focus()
		except Exception as e:
			raise e
	else:
		messagebox.showerror("MjB CHAT-BOT Informer", "Invalid email '"+conEmail.get()+"'.\nIt should contain _ _@ _ _.com!\nPlease try again!")
		conEmail.delete(0, END)
		conEmail.focus()



ttk.Button(btF, text=" SAVE ", cursor="exchange", command=SaveC).grid(row=0, column=0)
ttk.Button(btF, text=" CLEAR ", cursor="X_cursor", command=cle).grid(row=0, column=1, padx=5)



def AddC():
	try:
		ask = simpledialog.askstring("MjB CHAT-BOT Informer", "Enter Contact Name below please!.")
		if(ask==None):
			pass
		elif (ask!=""):			
			ask2 = simpledialog.askstring("MjB CHAT-BOT Informer", "Enter Contact Email below please!.\n\nInclude @ and .com in the Email!\n\n\tlike bmuzoor@gmail.com")
			if(ask2==None):
				pass
			elif(ask2!=""):
				if ("@" and ".com" in ask2):
					print(ask)
					print(ask2)
					try:
						contL=[]
						mydb = mysql.connector.connect(host="localhost", user="root",password="", database="chatbot")
						cursor = mydb.cursor()

						fetcC = ("SELECT UserId FROM mycontacts WHERE Email=%s")
						eml = (ask2, )
						cursor.execute(fetcC, eml)
						res = cursor.fetchall()
						for UserId in res:
							contL.append(UserId)

						if ask2 not in contL:
							emL=[]
							fetcC1 = ("SELECT Id FROM signup WHERE Email=%s")
							eml1 = (ask2, )
							cursor.execute(fetcC1, eml1)
							res1 = cursor.fetchall()
							for Id in res1:
								emL.append(Id) 
							if ask2 not in emL:
								messagebox.showerror("MjB CHAT-BOT Informer", "Contact Email"+ask2+" Cannot be added since it has no account here!\nPlease Create its account and then add again!")
							else:
								addSql = "INSERT INTO  mycontacts(UserId, Name, Email) VALUES (%s, %s, %s)"
								valx = (LoginId, ask, ask2)
								cursor.execute(addSql, valx)
						else:
							messagebox.showerror("MjB CHAT-BOT Informer", "Contact Email "+str(x)+" already exists!\nPlease try again!")
					except Exception as e:
						raise e

				else:
					messagebox.showerror("MjB CHAT-BOT Informer", "Invalid email '"+ask2+"'.\nIt should contain _ _@ _ _.com!\nPlease try again!")
			else:
				messagebox.showerror("MjB CHAT-BOT Informer", "Contact Email cannot be empty!!\nPlease try again!")
		else:
			messagebox.showerror("MjB CHAT-BOT Informer", "Contact Name cannot be empty!\nPlease try again!")


	except Error as e:
		messagebox.showerror("MjB CHAT-BOT Informer", "Add contact process closed!\nPlease try again!")
		raise e


#------------------more actions-------------------------------------
outF = Frame(Ff2, bg="skyblue", relief="raised", bd=2)
outF.pack(side=TOP, anchor="center",pady=7, expand=1)



def LoUt():
	userN.delete(0, END)
	passW.delete(0, END)
	note.tab(2, state="hidden")
	note.tab(0, state="hidden")
	note.tab(1, state="hidden")
	note.tab(2, state="hidden")
	note.tab(3, state="hidden")
	note.tab(4, state="hidden")
	note.tab(5, state="hidden")
	note.tab(6, state="hidden")
	note.select(0)

online = Button(outF, text="Refresh ☻", fg="green", relief="flat", bg="skyblue", cursor="exchange")
online.grid(row=0, column=0)
Label(outF, text="|",bg="skyblue", fg="skyblue", relief="raised").grid(row=0, column=1, padx=10)

info = Button(outF, text="About me", fg="brown", relief="flat", bg="skyblue", command=Abt, cursor="hand2")
info.grid(row=0, column=6)
Label(outF, text="|",bg="skyblue", fg="skyblue", relief="raised").grid(row=0, column=7, padx=10)

addC = Button(outF, text="Add Contact", fg="brown", relief="flat", bg="skyblue", command=open5, cursor="hand2")
addC.grid(row=0, column=8)
Label(outF, text="|",bg="skyblue", fg="skyblue", relief="raised").grid(row=0, column=9, padx=10)

logout = Button(outF, text="log out", fg="red", relief="flat", bg="skyblue", command=LoUt, cursor="X_cursor")
logout.grid(row=0, column=10)

#-----------------message displays--------------
mainF1 = LabelFrame(Ff2)
mainF1.pack(side=BOTTOM, pady=2, padx=2)

senderF = Frame(mainF1)
senderF.pack(side=LEFT)

recieverF = Frame(mainF1)
recieverF.pack(side=RIGHT)



Label(senderF, text="LAST SENT", font=("Lucida Handwriting",10,"bold")).grid(row=0, column=0, pady=5)
Label(recieverF, text="LAST RECIEVED", font=("Lucida Handwriting",10,"bold")).grid(row=0, column=0, pady=5)

sender = scrolledtext.ScrolledText(senderF, height=15, width=32, relief="flat", bg="lightgray")
reciever = scrolledtext.ScrolledText(recieverF, height=15, width=32, relief="flat", bg="lightgray")
sender.grid(row=1, column=0)
reciever.grid(row=1, column=0, sticky=(N,S))
reciever.config(state="disabled")

def viewF(*args):
	viewM1.config(font=("Lucida", 10,"italic","underline"), cursor="hand2")
def viewL(*args):
	viewM1.config(font=("Lucida", 10,"italic"), cursor="hand2")

def viewF2(*args):
	viewM2.config(font=("Lucida", 10,"italic","underline"), cursor="hand2")
def viewL2(*args):
	viewM2.config(font=("Lucida", 10,"italic"), cursor="hand2")

viewM1 = Label(senderF, text="View All", fg="blue", font=("Lucida", 10,"italic"), relief=GROOVE)
viewM1.grid(sticky="e", padx=10, ipadx=4)
viewM1.bind("<Enter>", viewF)
viewM1.bind("<Leave>", viewL)
viewM1.bind("<1>",viewallsent)
#-------------designing messages------------

#---------------sent--------------
sender.tag_configure('bold_italics', font=('Arial', 8, 'bold', 'italic'), background="yellow", foreground="red")
sender.tag_configure('big', font=('Verdana', 10, 'bold'), background="blue", foreground="white")
sender.tag_configure('color', foreground='black', font=('Lucida', 12), background="lightblue")
sender.config(state="disabled")

viewM2 = Label(recieverF, text="View All", fg="blue", font=("Lucida", 10,"italic"), relief=GROOVE)
viewM2.grid(sticky="e",ipadx=4)
viewM2.bind("<Enter>", viewF2)
viewM2.bind("<Leave>", viewL2)
#---------------inbox--------------
reciever.tag_configure('bold_italics', font=('Arial', 8, 'bold', 'italic'), background="yellow", foreground="red")
reciever.tag_configure('big', font=('Verdana', 10, 'bold'), background="blue", foreground="white")
reciever.tag_configure('color', foreground='black', font=('Lucida', 12), background="lightblue")
reciever.tag_configure('color1', foreground='green', font=('Lucida', 8, "underline"), background="blue")
#--------------------------chat bot ends-------------


online.config(command=fetchmsgs)

today = date.today()
now = today.strftime("%Y")

Label(db, text="@ MjB SYSTEM "+now+" | ALL RIGHTS RESERVED", bg="light gray", fg="gray").pack()

db.rowconfigure(0, weight=2)
db.columnconfigure(0, weight=2)
db.mainloop()