from tkinter import *
from tkinter import ttk, messagebox
import csv
import sqlite3
import sqlcalls
import functions
#This is the mainrun file for the Travel-Planner, follows the following order of content:
#setupDB -> mainscreen setup-> setup buttons,labels -> calls and executions -> eventhandling
#Note: Functions are found in functions.py

sqlcalls.setupDB()

#MainScreen Setup
window = Tk()
window.minsize(900, 600)
window.title("Travel Planner")
window.resizable(False, False)
width = 900
height = 600
x = functions.getcenterX(width, window)
y = functions.getcenterY(height, window)
window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


#

window.mainloop()


