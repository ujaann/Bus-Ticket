from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
import ast,sqlite3

window=Tk()
window.title("BST")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False,False)

destinations=["swoyambhu","balaju","dillibazaar","bagbazaar"]
def creation(username):
    home=Tk()
    home.title("Ticket viewer")
    home.geometry("240x80")
    home.resizable(False,False)
    labfram=LabelFrame(home,text="Welcome "+username,font=("Microsoft YaHei UI Light",13),border=20,borderwidth=5,cursor="dotbox")
    labfram.pack()
    create_button=Button(labfram,text="make ticket",activebackground="purple",activeforeground="white",font=24,padx=10,pady=10,bg="yellow",command=lambda:run_code(username))
    create_button.grid(row=0,column=0)
    view_tickets_button=Button(labfram,text="view ticket",activebackground="purple",font=24,padx=10,pady=10,bg="blue",fg="white",command=lambda:view_tickets(username))
    view_tickets_button.grid(row=0,column=2)
    home.mainloop()

def view_tickets(username):
    conn=sqlite3.connect("project.db")
    c=conn.cursor()
    # we check if given username already exists
    c.execute("SELECT user_id,username FROM USER_RECORDS")
    records=c.fetchall()
    for record in records:
        lstedrecord=list(record)
        if lstedrecord[1]==username:
            uid=lstedrecord[0]
    conn.commit()
    c.execute("SELECT * FROM TICKET_RECORDS WHERE uid="+str(uid)+"")
    tickets=c.fetchall()
    conn.close()

    view=Tk()
    view.geometry("350x120")
    view.resizable(False,True)
    view.title("View")
    labelfor_identity=Label(view,bg="white",text="Ticket_id\tDate\tTo\tFrom\tUser_id",font=23)
    labelfor_identity.grid(row=0,column=0,columnspan=2)
    i=""
    FrameforTickets=Frame(view)
    FrameforTickets.grid(row=1,column=0,columnspan=2)
    for ticket in tickets:
        i=str(ticket)
        ticketLabel=Label(FrameforTickets,bg="white",text=i,font=20)
        ticketLabel.pack()
    ticket_idEntry=Entry(view,bg="grey",fg="white",font=12)
    ticket_idEntry.grid(row=3,column=0,columnspan=2)
    delete_button=Button(view,text="Remove ticket",bg="red",fg="white",activebackground="white",activeforeground="red",font=23,command=lambda:delete_ticket(uid,ticket_idEntry.get()))
    delete_button.grid(row=2,column=0,padx=30)
    update_button=Button(view,text="Modify ticket",bg="green",fg="white",activebackground="white",activeforeground="green",font=23,command=lambda:update_ticket(uid,ticket_idEntry.get()))
    update_button.grid(row=2,column=1,padx=30)
    view.mainloop()

def delete_ticket(uid,ticket_id):   
    conn=sqlite3.connect("project.db")
    try:
        c=conn.cursor()
        # we check if given username already exists
        c.execute("SELECT uid FROM TICKET_RECORDS WHERE ticket_id="+str(ticket_id)+"")
        records=c.fetchall()
        print(records,ticket_id) 
        for record in records:
            lstedrecord=list(record)
            print(lstedrecord)
        conn.commit()
        if lstedrecord[0]==uid:
            c=conn.cursor()
            query="DELETE FROM TICKET_RECORDS WHERE ticket_id="+ticket_id+""
            print(query)
            c.execute(query)
            conn.commit()
            messagebox.showinfo("good","delete successful")
    except:
        messagebox.showerror("error","try again with different ticket")
    conn.close()


def update_ticket(uid,ticket_id):
    conn=sqlite3.connect("project.db")
    try:
        c=conn.cursor()
        # we check if given username already exists
        c.execute("SELECT uid FROM TICKET_RECORDS WHERE ticket_id="+str(ticket_id)+"")
        records=c.fetchall()
        print(records)
        for record in records:
            lstedrecord=list(record)
            print(lstedrecord)
        conn.commit()
    except:
        messagebox.showerror("oops","your ticket not found")
    def inserting_tickt_editor():
        c=conn.cursor()
        try:
            c.execute("""UPDATE TICKET_RECORDS SET
            date=:dat,
            to_=:strt,
            from_=:ed
            WHERE ticket_id="""+str(ticket_id),
            {'dat':date_editor.get(),
            'strt':starting_editor.get(),
            'ed':ending_editor.get()
            })
            conn.commit()
            messagebox.showinfo("good","updated succesfully")
        except:
            messagebox.showerror("sorry","pls try again after checking ticket")
        update_view.destroy()
            # c.execute("SELECT * FROM TICKET_RECORDS ORDER BY ticket_id DESC LIMIT 1;")
            # last_entry=c.fetchone()
            # last_entryList=list(last_entry)
            # print(last_entryList)
            # lastUser=[last_entryList[0]+1]
                # to maintain primary key we only add values with id in increasing order    
                # so we increment by one to add after last entry
            # values=tuple(lastUser+values+[uid])
            # conn.commit()
            # c.execute("INSERT INTO TICKET_RECORDS VALUES"+str(values)+'')
            # conn.commit()
            # conn.close()

    try:
        if lstedrecord[0]==uid:
                update_view=Tk()
                update_view.title("Update view")
                update_view.geometry("280x180")
                update_view.resizable(False,False)
                dateLabel=Label(update_view,text="Enter date:",font=24,bg="white")
                dateLabel.grid(row=0,column=0)
                date_editor=Entry(update_view)
                date_editor.grid(row=0,column=1)
                beginLabel1=Label(update_view,text="Enter Starting point:",font=24,bg="white")
                beginLabel1.grid(row=1,column=0)
                # btn_end = Button(update_view, text='ending point', command=lambda:item_inending_editor())
                # btn_end.pack()
                starting_editor = StringVar(update_view)
                starting_editor.set("From") # default value

                l1e = Label(update_view,  text='Select One',font=24 ,width=10 )  
                l1e.grid(row=1,column=1)
                om1e =OptionMenu(update_view, starting_editor,*destinations)
                om1e.grid(row=2,column=0,columnspan=2)

                endLabel2=Label(update_view,text="Enter Ending point:",font=24,bg="white")
                endLabel2.grid(row=3,column=0)


                ending_editor = StringVar(update_view)
                ending_editor.set("To") # default value

                l3e = Label(update_view,  text='Select One',font=24, width=10 )  
                l3e.grid(row=3,column=1)
                om2e =OptionMenu(update_view, ending_editor,*destinations)
                om2e.grid(row=4,column=0,columnspan=2)
                
                confirmer = Button(update_view, text='Confirm',font=24,bg="#57a1f8",fg="white", command=lambda:inserting_tickt_editor())
                confirmer.grid(row=5,column=0,columnspan=2)
                update_view.mainloop()
    except:
        messagebox.showerror("oops","ticket not found")
    conn.close()

def run_code(username):
    def inserting_tickt():
        values=[dateEntry.get(),startingoptions.get(),endingoptions.get()]
        conn=sqlite3.connect("project.db")
        c=conn.cursor()
        c.execute("SELECT * FROM TICKET_RECORDS ORDER BY ticket_id DESC LIMIT 1;")
        last_entry=c.fetchone()
        last_entryList=list(last_entry)
        print(last_entryList)
        lastUser=[last_entryList[0]+1]
            # to maintain primary key we only add values with id in increasing order    
            # so we increment by one to add after last entry
        values=tuple(lastUser+values+[uid])
        conn.commit()
        c.execute("INSERT INTO TICKET_RECORDS VALUES"+str(values)+'')
        conn.commit()
        conn.close()
        creation_panel.destroy()

    conn=sqlite3.connect("project.db")
    c=conn.cursor()
    # we check if given username already exists
    c.execute("SELECT user_id,username FROM USER_RECORDS")
    records=c.fetchall()
    for record in records:
        lstedrecord=list(record)
        if lstedrecord[1]==username:
            uid=lstedrecord[0]
    conn.commit()
    conn.close()
    creation_panel=Toplevel()
    creation_panel.title("Creation view")
    creation_panel.geometry("280x180")
    creation_panel.resizable(False,False)
    dateLabel=Label(creation_panel,text="Enter date:",font=24,bg="white")
    dateLabel.grid(row=0,column=0)
    dateEntry=Entry(creation_panel)
    dateEntry.grid(row=0,column=1)
    beginLabel=Label(creation_panel,text="Enter Starting point:",font=24,bg="white")
    beginLabel.grid(row=1,column=0)
    startingoptions = StringVar(creation_panel)
    startingoptions.set("From") # default value

    l1 = Label(creation_panel,  text='Select One',font=24, width=10 )  
    l1.grid(row=1,column=1)
    om1 =OptionMenu(creation_panel, startingoptions,*destinations)
    om1.grid(row=2,column=0,columnspan=2)

    endLabel=Label(creation_panel,text="Enter Ending point:",font=24,bg="white")
    endLabel.grid(row=3,column=0)
    endingoptions = StringVar(creation_panel)
    endingoptions.set("To") # default value

    l3 = Label(creation_panel,  text='Select One',font=24, width=10 )  
    l3.grid(row=3,column=1)
    om2 =OptionMenu(creation_panel, endingoptions,*destinations)
    om2.grid(row=4,column=0,columnspan=2)
    
    confirmer = Button(creation_panel, text='Confirm',font=24,bg="#57a1f8",fg="white", command=lambda:inserting_tickt())
    confirmer.grid(row=5,column=0,columnspan=2)
    creation_panel.mainloop()




def signup_window():
    def insertion():
        try:
            global b
            b=username.get()
            p=password.get()
            co=contact_no.get()
            if b=='' or p=='' or co=='':
                raise Exception
            conn=sqlite3.connect("project.db")
            c=conn.cursor()
            # we check if given username already exists
            c.execute("SELECT * FROM USER_RECORDS")
            records=c.fetchall()
            for record in records:
                lstedrecord=list(record)
                if lstedrecord[1]==b:
                    raise Exception
            conn.commit()
            conn.close()
            vals=[username.get(),password.get(),contact_no.get()]
            print(vals)
            root.destroy()
            register_function(vals)
        except Exception as exc:
            print(exc)
            messagebox.showerror("Invalid Username","Please try again")
            username.delete(0,END)
            password.delete(0,END)
            contact_no.delete(0,END)
    window.destroy()
    root = Tk()
    root.geometry('700x525')
    root.resizable(False,False)
    root.title("Registration Form")
    img=Image.open('busright.png')
    img=img.resize((700,525))
    img= ImageTk.PhotoImage(img)
    background=Label(root,image=img,border=0,bg='white')
    background.place(x=0,y=30)


    Titleof = Label(root, text="Registration form",width=20,font=("bold", 20))
    Titleof.place(x=180,y=53)


    usernameLabel = Label(root, text="Username:",width=20,font=("bold", 10))
    usernameLabel.place(x=170,y=130)

    username = Entry(root)
    username.place(x=330,y=130)

    passwordLabel = Label(root, text="Password:",width=20,font=("bold", 10))
    passwordLabel.place(x=170,y=180)

    password = Entry(root)
    password.place(x=330,y=180)


    contactLabel = Label(root, text="Contact:",width=20,font=("bold", 10))
    contactLabel.place(x=170,y=230)


    contact_no = Entry(root)
    contact_no.place(x=330,y=230)


    signup_submit=Button(root, text='Submit',width=20,bg='brown',fg='white',command=insertion)
    signup_submit.place(x=240,y=280)
    # it is use for display the registration form on the window
    root.mainloop()
    # print("registration form  seccussfully created...")

def register_function(values):
    conn=sqlite3.connect("project.db")
    c=conn.cursor()
    c.execute("SELECT * FROM USER_RECORDS ORDER BY user_id DESC LIMIT 1;")
    last_entry=c.fetchone()
    last_entryList=list(last_entry)
    print(last_entryList)
    lastUser=[last_entryList[0]+1]
    # to maintain primary key we only add values with id in increasing order    
    # so we increment by one to add after last entry
    values=tuple(lastUser+values)
    conn.commit()
    c.execute("INSERT INTO USER_RECORDS VALUES"+str(values)+'')
    conn.commit()
    c.execute("SELECT * FROM USER_RECORDS ORDER BY user_id DESC LIMIT 1;")
    last_entry=c.fetchone()
    last_entryList=list(last_entry)
    username=last_entryList[1]
    print(username)
    print(last_entryList)
    conn.commit()
    conn.close()
    messagebox.showinfo("Success","you have succesfully registered")
    creation(username)

def signin():
    username=user.get()
    password=code.get()
    confirm_password=confirm_code.get()
    # we connect to our database using connect from sqlite module
    conn=sqlite3.connect("project.db")
    c=conn.cursor()
    # execute query to get records
    c.execute("SELECT * FROM USER_RECORDS")
    records=c.fetchall()
    for record in records:
        # each record from table USER_RECORDS is retrieved as tuple 
        # which is converted to list
        lstedrecord=list(record)
            # here we take the second field which is username to check if it is present
        if lstedrecord[1]==username:
                # we retrieve password from given username
            c.execute("SELECT password FROM USER_RECORDS WHERE username='"+username+"'")
            passwordTuple=c.fetchone()
    conn.commit()
    conn.close()
    try:
        pass_as_list=list(passwordTuple)
        correct_password=pass_as_list[0]
        # since data is in tuple we convert it to list for indexing and get password
        print(correct_password)
        if password==correct_password:
            messagebox.showinfo("Signed in","Welcome user")
            window.destroy()
            creation(username)
            return
        else:
            messagebox.showerror("Invalid","Incorrect password")
            return
    except UnboundLocalError as c:
        print(c)
        # if try block finds error we assume it is username related
        messagebox.showerror("Invalid","Enterred username does not exist")
        return

img=Image.open('busleft.png')
img=img.resize((500,500))
img= ImageTk.PhotoImage(img)
Label(window,image=img,border=0,bg='white').place(x=0,y=30)

frame=Frame(window,width=350,height=390,bg="#fff")
frame.place(x=480,y=50)

heading=Label(frame,text="Sign in",fg="#57a1f8",bg="white",font=("Microsoft YaHei UI Light",23,"bold"))
heading.place(x=100,y=5)

def on_enter(e):
    user.delete(0,"end")
def on_leave(e):
    name=user.get()
    if name=="":
        user.insert(0,"Username")

user=Entry(frame,width=25,fg='black',border=2,bg="white",font=("Microsoft YaHei UI Light",11))
user.place(x=30,y=80)
user.insert(0,"Username")
user.bind('<FocusIn>',on_enter)
user.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg="black").place(x=25,y=105)

def on_enter(e):
    code.delete(0,"end")
def on_leave(e):
    name=code.get()
    if name=="":
        code.insert(0,"Password")

code=Entry(frame,width=25,fg='black',border=0,bg="white",font=("Microsoft YaHei UI Light",11))
code.place(x=30,y=150)
code.insert(0,"Password")
code.bind("<FocusIn>",on_enter)
code.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg="black").place(x=25,y=177)

def on_enter(e):
    confirm_code.delete(0,"end")
def on_leave(e):
    name=user.get()
    if name=="":
        confirm_code.insert(0,"Confirm Password")

confirm_code=Entry(frame,width=25,fg='black',border=2,bg="white",font=("Microsoft YaHei UI Light",11))
confirm_code.place(x=30,y=220)
confirm_code.insert(0,"Confirm Password")
confirm_code.bind('<FocusIn>',on_enter)
confirm_code.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg="black").place(x=25,y=247)

Button(frame,width=39,pady=7,text='Sign in',bg="#57a1f8",fg='white',border=0,command=signin).place(x=35,y=280)
label=Label(frame,text="Don't have an account",fg='black',bg="white",font=("Microsoft YaHei UI Light",9))
label.place(x=75,y=340)

sign_up=Button(frame,width=6,text="Sign up",border=0,bg="white",cursor="hand2",fg="#57a1f8",command=signup_window)
sign_up.place(x=215,y=340)

window.mainloop()