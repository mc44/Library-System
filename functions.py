from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

def getcenterX(num, window):
    finnum = (window.winfo_screenwidth() / 2) - (num / 2)
    return finnum

def getcenterY(num, window):
    finnum = (window.winfo_screenheight() / 2) - (num / 2)
    return finnum

def filltree(my_tree, table, varlist="", searchlimiter=""):
    my_tree.delete(*my_tree.get_children())
    conn = sqlite3.connect("tplanner.db")
    data = conn.execute(f"SELECT * FROM {table} ").fetchall()
    conn.close()
    #varlist = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get()]
    iid = 1
    desti=""
    arr=[]
    for line in data:
        if table=="Trip":
            conn = sqlite3.connect("tplanner.db")
            dest = conn.execute(f"SELECT * FROM Trip_Destination WHERE Trip_ID={line[0]} ").fetchall()
            conn.close()
            for name in dest:
                desti+=name[1]+", "
            for val in line:
                arr.append(val)
            arr.insert(2, desti)
            line=arr
        my_tree.insert(parent='', index='end', iid=iid, text="", values=line)
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
