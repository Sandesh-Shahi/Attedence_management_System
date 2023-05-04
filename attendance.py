
import tkinter as tk
from tkinter import*
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import time
import tkcalendar
import re
class Attendance:
    def __init__(self):   
         #---------------Initial Window-------#
        self.root=tk.Tk()
        #-----------variables for all the interface-------------#
        self.username_for_login_var=tk.StringVar() #for login only
        self.password_for_login_var=tk.StringVar() #for login only
        self.password_for_signup_var=tk.StringVar() #for signup only
        #----title-----#
        self.root.title("Attendance Management System")
        self.root.configure(bg='white')
        #----geometry----#
        self.root.geometry('500x500')
        #-----resizeable----#
        self.root.resizable(False,False)
        #----title of this program----#
        title_of_this_program=tk.Label(self.root,text="Log in As a Admin",font=('sans serif',10),fg='red',bg='white')
        title_of_this_program.place(x=200,y=10)
        #--------labels and titles for login------#
        username_login_label=tk.Label(self.root,text="Username:",fg='red',bg='white')
        username_login_label.place(x=100,y=40)
        username_login_entry=ttk.Entry(self.root,textvariable=self.username_for_login_var)
        username_login_entry.place(x=180,y=60)
        username_login_entry.focus()
        #------labels and entry for passwords-----#
        password_login_label=tk.Label(self.root,text="Password:",fg='red',bg='white')
        password_login_label.place(x=100,y=90)
        password_login_entry=ttk.Entry(self.root,textvariable=self.password_for_login_var)
        password_login_entry.place(x=180,y=110)
        #----------callback functions------#
        def login():
            self.loggedin(self.username_for_login_var.get(),self.password_for_login_var.get())
        def signup():
            self.signup()
        #------loginbutton----------#
        login_button=Button(self.root,text="Login",bd='0',bg='blue',fg='white',command=login)
        login_button.place(x=180,y=160)
        #-----signupbutton---------#
        signup_button=Button(self.root,text="Signup",bd='0',bg='blue',fg='white',command=signup)
        signup_button.place(x=280,y=160)

        signup_nara=Label(self.root,text="''This is the  login panel for Admin.\n \t Admin only can take attendence''",bg='white',fg='red')
        signup_nara.place(x=100,y=250)
        # ----------database connection-----------#
        try:
            self.connection = mysql.connector.connect(host="localhost",password="",username="root",database="pythonproject")
        except:
            messagebox.showerror("Database not found","Couldnot connect to database")
            self.root.destroy()
        self.root.mainloop()
    def loggedin(self,username,password):
       cursor = self.connection.cursor()
       query=f"SELECT * FROM admins where username='{username}' and password='{password}'"
       try:
           cursor.execute(query)
           data = cursor.fetchone()
           if data[0]==username and data[1]==password:
               messagebox.showinfo("Sucess","Login Sucess")
               self.login_sucess(data[0])
           else:
               messagebox.showerror("Login Failed","Please Check your Details Again")
       except:
           messagebox.showerror("Login Failed","Your Account Doesnot exists")
    def signup(self):
        #-----signup interface--------#
        signup_interface=tk.Tk()
        signup_interface.configure(bg='white')
        #-----variables for signup----#
        self.username_for_signup_var=tk.StringVar() #for signup only
        #-------title-----------#
        signup_interface.title("Create Account")
        #----geometry-----#
        signup_interface.geometry('300x300')
        signup_interface.resizable(False,False)
        #-------lables for username and entry------#
        username_for_signup_label=tk.Label(signup_interface,text="Enter Username:-",fg='white',bg='blue')
        username_for_signup_label.place(x=10,y=70)
        username_entry_for_signup=ttk.Entry(signup_interface,textvariable=self.username_for_signup_var)
        username_entry_for_signup.place(x=100,y=90)
        #-------------lables for password and entry-----#
        password_for_signup_label=tk.Label(signup_interface,text="Enter Password:- ",bg='blue',fg='white')
        password_for_signup_label.place(x=10,y=130)
        password_entry_for_signup=ttk.Entry(signup_interface,textvariable=self.password_for_signup_var)
        password_entry_for_signup.place(x=100,y=150)
        
        #----callback function----#
        # validation-----------------#
        def createaccount():
            name = username_entry_for_signup.get()
            password = password_entry_for_signup.get()
            msg = ''
            match=re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password)
            mat = len(name)
            if(match and mat!=0):
                self.createaccountwithus(username_entry_for_signup.get(),password_entry_for_signup.get())
                signup_interface.destroy()
            else:
                messagebox.showerror("Invalid  ","Please enter valid name & password")
     
        #-----create account button------#
        create_account_button=tk.Button(signup_interface,text="Create Account",command=createaccount,bg='blue',fg='white')
        create_account_button.place(x=100,y=190)
        signup_interface.mainloop()
    def createaccountwithus(self,username,password):
        query=f"INSERT INTO admins values('{username}','{password}')"
        cursor=self.connection.cursor()
        try:
            cursor.execute(query)
            messagebox.showinfo("Account Created","Account Created Sucess,Proceed towards login")
            self.connection.commit()
           
            
        except:
            messagebox.showerror("Username already in use","This username is already in use choose another username")

       
    def login_sucess(self,username):
        self.root.destroy()
        login_sucess_interface=tk.Tk()
        #-------title--------#
        login_sucess_interface.title(f"Welcome {username}")
        # login_sucess_interface.configure(bg='white')
        #----geometry-------#
        login_sucess_interface.geometry('500x450')
        login_sucess_interface.resizable(False,False)
        login_sucess_interface.config(bg="blue")
        #-------date display----#
        t = time.ctime()
        date=t.split(' ')
        todays_date=date[0]+" "+date[1]+" "+date[2]+" "+date[-1]
        date_label=tk.Label(login_sucess_interface,text="{}".format(todays_date),font=("sans serif",10),fg='white',bg='blue')
        date_label.place(x=10,y=0)
        #-----you are now logged in as ----#
        logged_in_as_label=tk.Label(login_sucess_interface,text=f"You are now logged in as {username}",font=("sans serif",11),fg='white',bg='blue')
        logged_in_as_label.place(x=100,y=20)
        #------select divisions-----#
        select_division=tk.Label(login_sucess_interface,text="Select Division",fg='white',bg='blue')
        select_division.place(x=10,y=80)
        #------divisions combobox-------#
        divisions_combobox=ttk.Combobox(login_sucess_interface,state="readonly",width=10)
        divisions_combobox['values']=("CEA","CEB","CEC","CED","CEE")
        divisions_combobox.current(0)
        divisions_combobox.place(x=10,y=100)
        
        #--------callback functions----#
        def getdetails():
            cursor = self.connection.cursor()
            division_name = divisions_combobox.get()
            division_name = division_name.lower()
            query = f"SELECT enrollment, name FROM {division_name};"
            cursor.execute(query)
            self.data = cursor.fetchall()
            start = 220
            self.checkboxes = []  # create a list to store the checkboxes
            for enrollment, name in self.data:
                records_label = ttk.Label(login_sucess_interface, text=f"{enrollment} {name}",foreground='white',background='blue')
                records_label.place(x=110, y=start)
                checkbox = tk.Checkbutton(login_sucess_interface,bg='blue')
                checkbox.place(x=350, y=start)
                
                self.checkboxes.append(checkbox)  # add the checkbox to the list
                start += 40
        def update():
            try:
                final_check=[]
                selected_date = date_entry.get_date()
                for checkbox in self.checkboxes:
                    value = checkbox.instate(['selected'])
                    final_check.append(value)
                details_with_status=list(zip(self.data,final_check))
                for details in details_with_status:
                    if False in details:
                        division=divisions_combobox.get()
                        try:
                            enrollment=details[0][0]
                            division = division.lower()
                            query = f"UPDATE {division} SET status='Absent',date_day='{selected_date}' where enrollment='{enrollment}'"
                            cursor=self.connection.cursor()
                            cursor.execute(query)
                            self.connection.commit()
                        except:
                            messagebox.showerror("Failed","Failed to Update Attendance")
                    else:
                        division=divisions_combobox.get()
                        try:
                            division = division.lower()
                            enrollment=details[0][0]
                            query = f"UPDATE {division} SET status='Present',date_day='{selected_date}' where enrollment='{enrollment}'"
                            cursor=self.connection.cursor()
                            cursor.execute(query)
                            self.connection.commit()
                        except:
                            messagebox.showerror("Failed","Failed to Update Attendance")
                else:
                    messagebox.showinfo("Sucess","Attendance Updated Sucessfully")
            except:
                messagebox.showerror("Select Student","Please Select Student to update attendance")
        def cleardata():
            # Clear the labels and checkboxes
            for widget in login_sucess_interface.winfo_children():
                if isinstance(widget, ttk.Label) or isinstance(widget, ttk.Checkbutton):
                    widget.destroy()
        def change_pass():
            change_pas_interface=tk.Tk()
            change_pas_interface.configure(bg='white')
            #----old password----#
            old_password_label=tk.Label(change_pas_interface,text="Old Password",fg='blue',bg='white')
            old_password_label.place(x=65,y=30)
            old_password_entry=ttk.Entry(change_pas_interface)
            old_password_entry.place(x=40,y=50)
            #-----new password-----#
            new_password_label=tk.Label(change_pas_interface,text="New Password",fg='blue',bg='white')
            new_password_label.place(x=65,y=80)
            new_password_entry=ttk.Entry(change_pas_interface)
            new_password_entry.place(x=40,y=100)
            #----callback functions----#
            def change():
                old_pass=old_password_entry.get()
                new_password=new_password_entry.get()
                current_username=self.username_for_login_var.get()
                current_password=self.password_for_login_var.get()
                if old_pass!=current_password:
                    messagebox.showerror("Password Did not match","Password Didnot Matched check again")
                    change_pas_interface.destroy()
                else:
                    try:
                        cursor=self.connection.cursor()
                        query=f"UPDATE admins set password='{new_password}' where username='{current_username}'"
                        cursor.execute(query)
                        self.connection.commit()
                        messagebox.showinfo("Update Sucess","Password Updated Successfully")
                        change_pas_interface.destroy()
                    except:
                        messagebox.showerror("Error","Error updating Password")
            #-----update password----#
            update_password_button=tk.Button(change_pas_interface,text="Change",command=change,fg="white",bg='blue')
            update_password_button.place(x=60,y=150)
            #-----title-----#
            change_pas_interface.title("Change admin Password")
            #----mainloop----#
            change_pas_interface.mainloop()
        def add_student():
            add_student_window=tk.Tk()
            #-----title-----#
            add_student_window.title("Add Student")
            #---geometry-----#
            add_student_window.geometry('300x300')
            add_student_window.configure(bg='white')
            add_student_window.resizable(False,False)
            #------enrollment label and entry----#
            enrollment_var=tk.StringVar()
            enrollment_label=tk.Label(add_student_window,text="Enrollment",fg='blue',bg='white')
            enrollment_label.place(x=130,y=30)
            enrollment_entry=ttk.Entry(add_student_window,textvariable=enrollment_var)
            enrollment_entry.place(x=100,y=50)
            #------name entry------#
            name_var=tk.StringVar()
            name_label=tk.Label(add_student_window,text="Name",fg='blue',bg='white')
            name_label.place(x=140,y=80)
            name_entry=ttk.Entry(add_student_window,textvariable=name_var)
            name_entry.place(x=100,y=100)
            #----select division label----#
            select_division_label_combo=tk.Label(add_student_window,text="Select Division",fg='blue',bg='white')
            select_division_label_combo.place(x=130,y=130)
            #-----division combobox----#
            select_division_combobox=ttk.Combobox(add_student_window,state="readonly",width=18)
            select_division_combobox['values']=('CEA','CEB','CEC','CED','CEE')
            select_division_combobox.current(0)
            select_division_combobox.place(x=100,y=150)
            #----callback function---#
            def add_new_student():
                enrollment =enrollment_entry.get()
                name=name_entry.get()
                division=select_division_combobox.get()
                division = division.lower()
                if len(enrollment)==0 or len(name)==0 or len(division)==0:
                    messagebox.showwarning("No Empty Fields","Please Fill the details")
                else:
                    try:
                        cursor=self.connection.cursor()
                        query=f"INSERT INTO {division} (enrollment,name) values ('{enrollment}','{name}')"
                        cursor.execute(query)
                        self.connection.commit()
                        messagebox.showinfo("Sucess","Student's Details Added")
                        add_student_window.destroy()
                    except:
                        messagebox.showwarning("Student Already exits","Student's Details Already Exits")
            #----add data----# 
            add_student_btn=tk.Button(add_student_window,text="Add Student",command=add_new_student,fg="white",bg='blue')
            add_student_btn.place(x=128,y=200)
            add_student_window.mainloop()
        #------date entry------#
        date_entry = tkcalendar.DateEntry(login_sucess_interface, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.place(x=150,y=100)
        #-----student details-----#
        student_details_button=tk.Button(login_sucess_interface,text="Get Students Details",command=getdetails,fg='white',bg='blue')
        student_details_button.place(x=320,y=100)
        #-----clear data-------#
        clear_data_button=tk.Button(login_sucess_interface,text="Clear Data",command=cleardata,fg='white',bg='blue')
        clear_data_button.place(x=350,y=400)
        #----change password button-----#
        change_password_button=tk.Button(login_sucess_interface,text="Change Pass",command=change_pass,bg='blue',fg='white')
        change_password_button.place(x=50,y=400)
        #----update attendance button-----#
        update_attendance=tk.Button(login_sucess_interface,text="Update",command=update,fg='white',bg='blue')
        update_attendance.place(x=200,y=400)
        #-----add student----#
        add_student_button=Button(login_sucess_interface,text="Add Student",command=add_student,fg='white',bg='blue')

        add_student_button.place(x=380,y=160)
    

        login_sucess_interface.mainloop()
if __name__=="__main__":
    s= Attendance()
