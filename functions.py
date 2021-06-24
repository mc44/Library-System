from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

def getcenterX(num, window):
    finnum = (window.winfo_screenwidth() / 2) - (num / 2)
    return finnum

def getcenterY(num, window):
    finnum = (window.winfo_screenheight() / 2) - (num / 2)
    return finnum

def filltree(my_tree, table, ID="", varlist="", searchlimiter=""):
    my_tree.delete(*my_tree.get_children())
    conn = sqlite3.connect("tplanner.db")
    if table == "Trip":
        data = conn.execute(f"SELECT * FROM {table} ").fetchall()
    elif table == "Trip_Destination":
        data = conn.execute(f"SELECT * FROM {table} WHERE Trip_ID = {ID} ").fetchall()
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



