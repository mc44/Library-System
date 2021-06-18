from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import sqlcalls
import functions
#This is the mainrun file for the Travel-Planner, follows the following order of content:
#setupDB -> mainscreen setup-> setup buttons,labels -> calls and executions -> eventhandling
#Note: Functions are found in functions.py

sqlcalls.setupDB()

#MainScreen Setup
window = Tk()
width = 1200
height = 700
window.minsize(width, height)
window.title("Travel Planner")
window.resizable(False, False)
x = functions.getcenterX(width, window)
y = functions.getcenterY(height, window)
window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

#Treeview
# building tree view
tree_frame = Frame(window)
tree_frame.place(relx=0.01, rely=0.025, relheight=0.4, relwidth=0.98)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
my_tree['columns'] = ("Trip_ID", "Trip Name", "Destination", "Start Date", "End Date", "Duration", "Notes", "Total Expenditure")
# #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Trip_ID", anchor=CENTER, width=40)
my_tree.column("Trip Name", anchor=W, width=160)
my_tree.column("Destination", anchor=CENTER, width=70)
my_tree.column("Start Date", anchor=CENTER, width=70)
my_tree.column("End Date", anchor=CENTER, width=70)
my_tree.column("Duration", anchor=CENTER, width=70)
my_tree.column("Notes", anchor=W, width=70)
my_tree.column("Total Expenditure", anchor=CENTER, width=70)

# my_tree.heading("#0", text="#", anchor=W)
my_tree.heading("Trip_ID", text="Trip_ID", anchor=CENTER)
my_tree.heading("Trip Name", text="Trip Name", anchor=W)
my_tree.heading("Destination", text="Destination", anchor=CENTER)
my_tree.heading("Start Date", text="Start Date", anchor=CENTER)
my_tree.heading("End Date", text="End Date", anchor=CENTER)
my_tree.heading("Duration", text="Duration", anchor=CENTER)
my_tree.heading("Notes", text="Notes", anchor=CENTER)
my_tree.heading("Total Expenditure", text="Total Expenditure", anchor=CENTER)

#Placing widgets
my_tree.pack(fill=BOTH)
tree_scroll.config(command=my_tree.yview)

#Calls
functions.filltree(my_tree, "Trip")

window.mainloop()


