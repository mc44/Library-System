import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import Calendar, DateEntry
import re

def getcenterX(num, window):
    finnum = (window.winfo_screenwidth() / 2) - (num / 2)
    return finnum

def getcenterY(num, window):
    finnum = (window.winfo_screenheight() / 2) - (num / 2)
    return finnum

#universal for filltree, (treename, dbtable ---
def filltree(my_tree, table, ID="", varlist="", searchlimiter=""):
    #if varlist:
    #    for button in varlist:
    #        button.config(state=DISABLED)
    my_tree.delete(*my_tree.get_children())
    conn = sqlite3.connect("tplanner.db")
    try:
        if table == "Trip" or table == "Traveler":
                data = conn.execute(f"SELECT * FROM {table} ").fetchall()
        elif table == "Trip_Destination":
            data = conn.execute(f"SELECT * FROM {table} WHERE Trip_ID = {ID} ").fetchall()
        elif table == "Itinerary":
            data = conn.execute(f"SELECT * FROM {table} WHERE Trip_ID = {ID} ").fetchall()
        elif table == "Events":
            data = conn.execute(f"SELECT * FROM {table} WHERE Itinerary_ID = {ID} ORDER BY Start_DandT, End_DandT").fetchall()
        elif table == "Traveler_Trip":
            data = conn.execute(f"SELECT Traveler_Trip.TravTrip_ID, Traveler.Name, Traveler.Age, Traveler.Gender, Traveler.Address FROM {table} INNER JOIN Traveler ON Traveler_Trip.Traveler_ID=Traveler.Traveler_ID WHERE Traveler_Trip.Trip_ID = {ID}").fetchall()
    except:
        return
    conn.close()
    #varlist = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get()]
    iid = 1
    desti=""
    for line in data:
        arr = []
        #if table == "Trip":
            #conn = sqlite3.connect("tplanner.db")
            #dest = conn.execute(f"SELECT * FROM Trip_Destination WHERE Trip_ID={line[0]} ").fetchall()
            #conn.close()
            #for name in dest:
            #    desti += name[1]+", "
            #for val in line:
            #    arr.append(val)
            #arr.insert(2, desti)
        if table == "Trip":
            for val in line:
                arr.append(val)
            arr[5] = str(line[5]).replace("\n", " ")
            line = arr
        elif table == "Itinerary":
            for val in line:
                arr.append(val)
            arr[2] = str(line[2]).replace("\n", " ")
            line = arr
        my_tree.insert(parent='', index='end', iid=iid, text="", values=line)
        iid+=1
#        if searchlimiter == "" or varlist == [0]*:
#            my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1], line[2], line[3], line[4]))
#        else:
#            c = 0
#            text = ""
#            for item in varlist:
#                if item == 1:
 #                   text += str(line[c])
 #               c+=1
#            if searchlimiter.lower() in text.lower():
#                my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1], line[2], line[3], line[4]))
#        iid += 1

def calcdur(start, end, tbox):
    tbox.config(state=NORMAL)
    tbox.delete(0, END)
    tbox.insert(0,str((end-start).days+1))
    tbox.config(state=DISABLED)
    return

#Add new Trip Destination
def addEntry(button, my_tree, my_tree1, self):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()
    def validate():
        t1 = tbox1.get()
        if t1 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        if values=="":
            messagebox.showinfo(parent=addscreen, title="No Selected Trip", message="Select a Trip to add a Destination to")
            return

        conn = sqlite3.connect("tplanner.db")
        data = conn.execute(f"SELECT * FROM Trip_Destination WHERE Trip_ID = {values[0]}")
        for line in data:
            if line[1].lower() == t1.lower():
                messagebox.showinfo(parent=addscreen, title="Already Exists", message="This Destination name already exists")
                return
        add = conn.execute("INSERT INTO Trip_Destination (Destination, Trip_ID) VALUES ('{}', '{}')".format(t1, values[0]))
        conn.commit()
        conn.close()
        filltree(my_tree1, "Trip_Destination", values[0])
        button.configure(state="normal")
        addscreen.destroy()

    addscreen = Toplevel(self)
    addscreen.resizable(False, False)
    addscreen.title("Add new Destination")
    addscreen.geometry(f'{300}x{100}+{int(getcenterX(300,self))}+{int(getcenterY(100,self))}')
    addscreen.minsize(300, 100)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    label1 = ttk.Label(addscreen, text="Destination:")
    tbox1 = ttk.Entry(addscreen, width=15)
    label1.place(relx=0.03, rely=0.095, relheight=0.3, relwidth=0.4)
    tbox1.place(relx=0.31, rely=0.095, relheight=0.31, relwidth=0.65)
    add = ttk.Button(addscreen, text="Add", command=lambda: validate())
    add.place(relx=0.35, rely=0.6, relheight=0.25, relwidth=0.3)

def editDestination(button, my_tree1, self):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()
    def edit(values):
        t1 = tbox1.get()
        if t1 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return

        conn = sqlite3.connect("tplanner.db")
        data = conn.execute(f"SELECT * FROM Trip_Destination WHERE Trip_ID = {values[2]}")
        for line in data:
            if line[1].lower() == t1.lower() and t1.lower() != values[1].lower():
                messagebox.showinfo(parent=addscreen, title="Already Exists", message="This Destination name already exists")
                return
        add = conn.execute("UPDATE Trip_Destination SET Destination='{}' WHERE TripD_ID='{}'".format(t1, values[0]))
        conn.commit()
        conn.close()
        filltree(my_tree1, "Trip_Destination", values[2])
        button.configure(state="normal")
        addscreen.destroy()

    addscreen = Toplevel(self)
    addscreen.resizable(False, False)
    addscreen.title("Edit Destination")
    addscreen.geometry(f'{300}x{100}+{int(getcenterX(300,self))}+{int(getcenterY(100,self))}')
    addscreen.minsize(300, 100)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    selected = my_tree1.focus()
    values = my_tree1.item(selected, 'values')
    print(values)
    label1 = ttk.Label(addscreen, text="Destination:")
    tbox1 = ttk.Entry(addscreen, width=15)
    label1.place(relx=0.03, rely=0.095, relheight=0.3, relwidth=0.4)
    tbox1.place(relx=0.31, rely=0.095, relheight=0.31, relwidth=0.65)
    try:
        tbox1.insert(0, values[1])
    except:
        return
    add = ttk.Button(addscreen, text="Edit", command=lambda: edit(values))
    add.place(relx=0.35, rely=0.6, relheight=0.25, relwidth=0.3)

##For Itinerary
#Add new Trip Destination
def addItin(button, my_tree, trackTrip, self, edit, delete):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()
    def validate():
        t1 = tbox1.get()
        t2 = tbox2.get("1.0", 'end-1c')
        if t1 == "" or t2 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return
        conn = sqlite3.connect("tplanner.db")
        data = conn.execute(f"SELECT * FROM Itinerary WHERE Trip_ID = {trackTrip}")
        for line in data:
            if line[1].lower() == t1.lower():
                messagebox.showinfo(parent=addscreen, title="Already Exists", message="Itinerary name already exists")
                return
        add = conn.execute("INSERT INTO Itinerary (Itinerary_Name, Description, Trip_ID) VALUES ('{}', '{}', '{}')".format(t1, t2, trackTrip))
        conn.commit()
        conn.close()
        filltree(my_tree, "Itinerary", trackTrip)
        button.configure(state="normal")
        edit.config(state=DISABLED)
        delete.config(state=DISABLED)
        addscreen.destroy()

    addscreen = Toplevel(self)
    addscreen.resizable(False, False)
    addscreen.title("Add new Destination")
    addscreen.geometry(f'{900}x{600}+{int(getcenterX(900,self))}+{int(getcenterY(600,self))}')
    addscreen.minsize(300, 100)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    label1 = ttk.Label(addscreen, text="Itinerary Name:")
    label2 = ttk.Label(addscreen, text="Description:")
    tbox1 = ttk.Entry(addscreen, width=15)
    tbox2 = Text(addscreen, width=15)
    label1.place(relx=0.13, rely=0.085, relheight=0.08, relwidth=0.4)
    label2.place(relx=0.14, rely=0.17, relheight=0.08, relwidth=0.4)
    tbox1.place(relx=0.31, rely=0.1, relheight=0.05, relwidth=0.65)
    tbox2.place(relx=0.31, rely=0.195, relheight=0.45, relwidth=0.65)
    add = ttk.Button(addscreen, text="Add", command=lambda: validate())
    add.place(relx=0.35, rely=0.85, relheight=0.1, relwidth=0.3)

def editItin(button, my_tree1, trackTrip, self, delete):
    def on_close():
        #button.configure(state="normal")
        addscreen.destroy()

    def edit():
        t1 = tbox1.get()
        t2 = tbox2.get("1.0", 'end-1c')
        if t1 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return

        conn = sqlite3.connect("tplanner.db")
        data = conn.execute(f"SELECT * FROM Itinerary WHERE Trip_ID = {trackTrip}")
        for line in data:
            if line[1].lower() == t1.lower() and t1.lower() != values[1].lower():
                messagebox.showinfo(parent=addscreen, title="Already Exists", message="This Itinerary name already exists")
                return
        add = conn.execute("UPDATE Itinerary SET Itinerary_Name='{}', Description='{}' WHERE Itinerary_ID='{}'".format(t1, t2, values[0]))
        conn.commit()
        conn.close()
        filltree(my_tree1, "Itinerary", values[3])
        delete.config(state=DISABLED)
        addscreen.destroy()

    addscreen = Toplevel(self)
    addscreen.resizable(False, False)
    addscreen.title("Add new Destination")
    addscreen.geometry(f'{900}x{600}+{int(getcenterX(900, self))}+{int(getcenterY(600, self))}')
    addscreen.minsize(300, 100)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    selected = my_tree1.focus()
    values = my_tree1.item(selected, 'values')
    label1 = ttk.Label(addscreen, text="Itinerary Name:")
    label2 = ttk.Label(addscreen, text="Description:")
    tbox1 = ttk.Entry(addscreen, width=15)
    tbox2 = Text(addscreen, width=15)
    label1.place(relx=0.13, rely=0.085, relheight=0.08, relwidth=0.4)
    label2.place(relx=0.14, rely=0.17, relheight=0.08, relwidth=0.4)
    tbox1.place(relx=0.31, rely=0.1, relheight=0.05, relwidth=0.65)
    tbox2.place(relx=0.31, rely=0.195, relheight=0.45, relwidth=0.65)
    tbox1.insert(0, values[1])
    tbox2.insert(tk.END, values[2])
    add = ttk.Button(addscreen, text="Edit", command=lambda: edit())
    add.place(relx=0.35, rely=0.85, relheight=0.1, relwidth=0.3)

#Add new Event
def addEvent(button, my_tree, my_tree1, trackItin, self, edit, delete):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()
    def validate():
        t1 = tb_name.get()
        t2 = tb_loc.get()
        t3 = tb_start.get()
        t4 = tb_end.get()
        t5 = tb_type.get()
        t6 = tb_notes.get("1.0", 'end-1c')
        t7 = tb_expenses.get()

        if len(t4) == 4:
            t4 = '0' + t4

        time = re.compile('^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$')

        money = re.compile(r'^\$?(\d*(\d\.?|\.\d{1,2}))$')
        #if re.match(money, t7):

        if not time.match(t4):
            messagebox.showinfo(parent=addscreen, title="Time not in 24hour format", message="Time needs to be on a 24hour format, ex. 01:12, 13:40, 00:01")
            return

        if not money.match(t7):
            messagebox.showinfo(parent=addscreen, title="Currency not in format", message="Expenses should not have commas, any text and only allows 2 maximum decimal values")
            return

        if t1 == "" or t2 == "" or t3 == "" or t4 == "" or t5 == "" or t6 == "" or t7 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        if values=="":
            messagebox.showinfo(parent=addscreen, title="No Selected Trip", message="Select an Itinerary to add an Event to")
            return

        conn = sqlite3.connect("tplanner.db")
        data = conn.execute(f"SELECT * FROM Events WHERE Itinerary_ID = {trackItin}")
        for line in data:
            if line[1].lower() == t1.lower():
                messagebox.showinfo(parent=addscreen, title="Already Exists", message="This Event name already exists")
                return
        add = conn.execute(f"INSERT INTO Events (Name, Location, Start_DandT, End_DandT, Type, Notes, Expenses, Itinerary_ID) VALUES ('{t1}', '{t2}', '{t3}', '{t4}', '{t5}', '{t6}', '{t7}', '{trackItin}')")
        conn.commit()
        conn.close()
        filltree(my_tree1, "Events", trackItin)
        button.configure(state="normal")
        edit.config(state=DISABLED)
        delete.config(state=DISABLED)
        addscreen.destroy()

    addscreen = Toplevel(self)
    addscreen.resizable(False, False)
    addscreen.title("Add new Event")
    addscreen.geometry(f'{900}x{600}+{int(getcenterX(900,self))}+{int(getcenterY(600,self))}')
    addscreen.minsize(300, 100)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    add = ttk.Button(addscreen, text="Add", command=lambda: validate())
    add.place(relx=0.45, rely=0.8, relheight=0.08, relwidth=0.1)
    # LABELS for the required information for 'add trip'
    lab_name = ttk.Label(addscreen, text="Name")
    lab_loc = ttk.Label(addscreen, text="Location")
    lab_std = ttk.Label(addscreen, text="Date")
    lab_etd = ttk.Label(addscreen, text="Time (00:00 - 23:59")
    lab_type = ttk.Label(addscreen, text="Type")
    lab_notes = ttk.Label(addscreen, text="Notes")
    lab_expenses = ttk.Label(addscreen, text="Expenses")

    # ENTRIES for the required information for 'add trip'
    tb_name = ttk.Entry(addscreen, width=15)
    tb_loc = ttk.Entry(addscreen, width=15)
    tb_start = DateEntry(addscreen, width=15)
    tb_end = ttk.Entry(addscreen, width=15)
    tb_type = ttk.Entry(addscreen, width=15)
    tb_notes = Text(addscreen, width=15, height=6)
    tb_expenses = ttk.Entry(addscreen, width=15)

    lab_name.place(relx=0.21, rely=0.025, relheight=0.06, relwidth=0.1)
    lab_loc.place(relx=0.21, rely=0.085, relheight=0.06, relwidth=0.1)
    lab_std.place(relx=0.21, rely=0.145, relheight=0.06, relwidth=0.1)
    lab_etd.place(relx=0.21, rely=0.205, relheight=0.06, relwidth=0.25)
    lab_type.place(relx=0.21, rely=0.265, relheight=0.06, relwidth=0.1)
    lab_notes.place(relx=0.21, rely=0.325, relheight=0.06, relwidth=0.1)
    lab_expenses.place(relx=0.21, rely=0.6, relheight=0.06, relwidth=0.1)

    tb_name.place(relx=0.41, rely=0.04, relheight=0.03, relwidth=0.4)
    tb_loc.place(relx=0.41, rely=0.1, relheight=0.03, relwidth=0.4)
    tb_start.place(relx=0.41, rely=0.16, relheight=0.03, relwidth=0.4)
    tb_end.place(relx=0.41, rely=0.22, relheight=0.03, relwidth=0.4)
    tb_type.place(relx=0.41, rely=0.28, relheight=0.03, relwidth=0.4)
    tb_notes.place(relx=0.41, rely=0.36, relheight=0.24, relwidth=0.4)
    tb_expenses.place(relx=0.41, rely=0.62, relheight=0.03, relwidth=0.4)

def editevent(button, my_tree, my_tree1, trackItin, self, delete):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()

    def edit():
        t1 = tb_name.get()
        t2 = tb_loc.get()
        t3 = tb_start.get()
        t4 = tb_end.get()
        t5 = tb_type.get()
        t6 = tb_notes.get("1.0", 'end-1c')
        t7 = tb_expenses.get()

        if len(t4) == 4:
            t4 ='0'+t4

        time = re.compile('^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$')

        money = re.compile(r'^\$?(\d*(\d\.?|\.\d{1,2}))$')
        #if re.match(money, t7):

        if not time.match(t4):
            messagebox.showinfo(parent=addscreen, title="Time not in 24hour format", message="Time needs to be on a 24hour format, ex. 01:12, 13:40, 00:01")
            return

        if not money.match(t7):
            messagebox.showinfo(parent=addscreen, title="Currency not in format", message="Expenses should not have commas, any text and only allows 2 maximum decimal values")
            return

        if t1 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return

        if t1 == "" or t2 == "" or t3 == "" or t4 == "" or t5 == "" or t6 == "" or t7 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information",
                                message="All textboxes need to be filled to complete the action")
            return
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        if values == "":
            messagebox.showinfo(parent=addscreen, title="No Selected Trip",
                                message="Select a Trip to add a Destination to")
            return

        conn = sqlite3.connect("tplanner.db")
        data = conn.execute(f"SELECT * FROM Events WHERE Itinerary_ID = {trackItin}")
        for line in data:
            if line[1].lower() == t1.lower() and line[1].lower() != values1[1].lower():
                messagebox.showinfo(parent=addscreen, title="Already Exists", message="This Event name already exists")
                return
        add = conn.execute(f"UPDATE Events SET Name = '{t1}', Location = '{t2}', Start_DandT = '{t3}', End_DandT = '{t4}', Type = '{t5}', Notes = '{t6}', Expenses = '{t7}', Itinerary_ID = '{trackItin}' WHERE Events_ID = '{values1[0]}'")
        conn.commit()
        conn.close()
        filltree(my_tree1, "Events", trackItin)
        delete.config(state=DISABLED)
        addscreen.destroy()

    addscreen = Toplevel(self)
    addscreen.resizable(False, False)
    addscreen.title("Edit Event")
    addscreen.geometry(f'{900}x{600}+{int(getcenterX(900, self))}+{int(getcenterY(600, self))}')
    addscreen.minsize(300, 100)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    add = ttk.Button(addscreen, text="Edit", command=lambda: edit())
    add.place(relx=0.45, rely=0.8, relheight=0.08, relwidth=0.1)
    # LABELS for the required information for 'add trip'
    lab_name = ttk.Label(addscreen, text="Name")
    lab_loc = ttk.Label(addscreen, text="Location")
    lab_std = ttk.Label(addscreen, text="Start Date")
    lab_etd = ttk.Label(addscreen, text="End Date")
    lab_type = ttk.Label(addscreen, text="Type")
    lab_notes = ttk.Label(addscreen, text="Notes")
    lab_expenses = ttk.Label(addscreen, text="Expenses")

    # ENTRIES for the required information for 'add trip'
    tb_name = ttk.Entry(addscreen, width=15)
    tb_loc = ttk.Entry(addscreen, width=15)
    tb_start = DateEntry(addscreen, width=15)
    tb_end = DateEntry(addscreen, width=15)
    tb_type = ttk.Entry(addscreen, width=15)
    tb_notes = Text(addscreen, width=15, height=6)
    tb_expenses = ttk.Entry(addscreen, width=15)

    lab_name.place(relx=0.21, rely=0.025, relheight=0.06, relwidth=0.1)
    lab_loc.place(relx=0.21, rely=0.085, relheight=0.06, relwidth=0.1)
    lab_std.place(relx=0.203, rely=0.145, relheight=0.06, relwidth=0.1)
    lab_etd.place(relx=0.205, rely=0.205, relheight=0.06, relwidth=0.1)
    lab_type.place(relx=0.205, rely=0.265, relheight=0.06, relwidth=0.1)
    lab_notes.place(relx=0.21, rely=0.325, relheight=0.06, relwidth=0.1)
    lab_expenses.place(relx=0.205, rely=0.6, relheight=0.06, relwidth=0.1)

    select = my_tree1.focus()
    values1 = my_tree1.item(select, 'values')
    tb_name.place(relx=0.41, rely=0.04, relheight=0.03, relwidth=0.4)
    tb_loc.place(relx=0.41, rely=0.1, relheight=0.03, relwidth=0.4)
    tb_start.place(relx=0.41, rely=0.16, relheight=0.03, relwidth=0.4)
    tb_end.place(relx=0.41, rely=0.22, relheight=0.03, relwidth=0.4)
    tb_type.place(relx=0.41, rely=0.28, relheight=0.03, relwidth=0.4)
    tb_notes.place(relx=0.41, rely=0.36, relheight=0.24, relwidth=0.4)
    tb_expenses.place(relx=0.41, rely=0.62, relheight=0.03, relwidth=0.4)
    tb_start.delete(0, END)
    tb_end.delete(0, END)

    tb_name.insert(0, values1[1])
    tb_loc.insert(0, values1[2])
    tb_start.insert(0, values1[3])
    tb_end.insert(0, values1[4])
    tb_type.insert(0, values1[5])
    tb_notes.insert(tk.END, values1[6])
    tb_expenses.insert(0, values1[7])

def addtriptrav(button, my_tree, tracktrip, self, removebutton):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()
    def validate():
        t1 = tbox1.get()
        if t1 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return

        conn = sqlite3.connect("tplanner.db")
        data = conn.execute(f"SELECT Traveler_Trip.TravTrip_ID, Traveler.Name, Traveler.Age, Traveler.Gender, Traveler.Address FROM Traveler_Trip INNER JOIN Traveler ON Traveler_Trip.Traveler_ID=Traveler.Traveler_ID WHERE Traveler_Trip.Trip_ID = '{tracktrip}'").fetchall()
        #data = conn.execute(f"SELECT * FROM Traveler_Trip WHERE Trip_ID = '{tracktrip}'")
        data1 = conn.execute(f"SELECT * FROM Traveler WHERE Name = '{t1}'")
        for line in data:
            if line[1].lower() == t1.lower():
                messagebox.showinfo(parent=addscreen, title="Already Exists", message="Traveler name already in this Trip")
                return
        for line1 in data1:
            add = conn.execute("INSERT INTO Traveler_Trip (Traveler_ID, Trip_ID) VALUES ('{}', '{}')".format(line1[0], tracktrip))
        conn.commit()
        conn.close()
        filltree(my_tree, "Traveler_Trip", tracktrip)
        button.configure(state="normal")
        removebutton.config(state=DISABLED)
        addscreen.destroy()

    addscreen = Toplevel(self)
    addscreen.resizable(False, False)
    addscreen.title("Add new Traveler")
    addscreen.geometry(f'{300}x{100}+{int(getcenterX(300,self))}+{int(getcenterY(100,self))}')
    addscreen.minsize(300, 100)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    label1 = ttk.Label(addscreen, text="Traveler:")
    tbox1 = ttk.Combobox(addscreen)
    label1.place(relx=0.03, rely=0.095, relheight=0.3, relwidth=0.4)
    add = ttk.Button(addscreen, text="Add", command=lambda: validate())
    add.place(relx=0.35, rely=0.6, relheight=0.25, relwidth=0.3)
    tbox1.config(state="readonly")
    courselist = makecoursedropdown(tbox1, tracktrip)
    tbox1.place(relx=0.31, rely=0.095, relheight=0.31, relwidth=0.65)


def makecoursedropdown(ddbox, tracktrip):
    conn = sqlite3.connect("tplanner.db")
    #course = conn.execute(f"SELECT * FROM Traveler_Trip WHERE Trip_ID ='{tracktrip}'").fetchall()
    course = conn.execute(f"SELECT * FROM Traveler").fetchall()
    conn.close()
    Options = []
    for line in course:
        Options.append("{}".format(line[1]))
    ddbox['values'] = Options
    return course
