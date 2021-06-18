from tkinter import *
from tkinter import ttk, messagebox
import csv
import sqlite3

def getcenterX(num, window):
    finnum = (window.winfo_screenwidth() / 2) - (num / 2)
    return finnum

def getcenterY(num, window):
    finnum = (window.winfo_screenheight() / 2) - (num / 2)
    return finnum