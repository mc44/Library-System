import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import ttk, messagebox, Text, scrolledtext
import sqlite3
from tkinter import font
from tkinter.font import BOLD, Font
import sqlcalls
import functions
import tkcalendar
from tkcalendar import Calendar, DateEntry

#This is the mainrun file for the Travel-Planner, follows the following order of content:
#setupDB -> global variable -> mainscreen setup-> setup buttons,labels -> calls and executions -> eventhandling
#Note: Functions are found in functions.py

sqlcalls.setupDB()

LARGEFONT = ("Verdana", 35)

#Global Variables


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        width = 1200
        height = 700
        self.minsize(width, height)
        self.title("Travel Planner")
        self.resizable(False, False)
        x = functions.getcenterX(width, container)
        y = functions.getcenterY(height, container)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2, Page3, Page4, Page5):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        #if moving to page1, refresh treeview
        if "page1" in str(frame):
            for child in frame.winfo_children():
                if "frame" in str(child):
                    for chil in child.winfo_children():
                        if "treeview" in str(chil):
                            functions.filltree(chil, "Trip")
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label of frame Layout 2
        # configure row sizes relative to other rows in self
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)
        # configure only one column
        self.columnconfigure(0, weight=1)

        # label as StartPage title
        labelConfig = Font(self, size=60, weight=BOLD)
        label = ttk.Label(self, text="Travel Planner",
                          font=labelConfig, foreground='#101010')

        # labelSub as subtitle
        labelSubConfig = Font(self, size=18)
        labelSub = ttk.Label(self, text="Plan the details, enjoy your trip!",
                             font=labelSubConfig, foreground='#808080')

        # interactionFrame surrounding the buttons
        interactionFrame = LabelFrame(self, text="", padx=50, pady=75)

        # placing labels and frame in grid accordingly
        label.grid(row=0, pady=(0, 10), sticky=S)
        labelSub.grid(row=1, sticky=N)
        interactionFrame.grid(row=2, rowspan=2, padx=350, pady=(15, 50),
                              sticky=NSEW)

        # configure row sizes relative to other rows in interactionFrame
        interactionFrame.rowconfigure(0, weight=1)
        interactionFrame.rowconfigure(1, weight=1)
        interactionFrame.columnconfigure(0, weight=1)

        # button text style
        b = ttk.Style()
        b.configure("start.TButton", font=("Arial", 16))

        # button1 showing frame 5 (Page5)
        button1 = ttk.Button(interactionFrame, text="Add New Trip", style="start.TButton",
                             command=lambda: controller.show_frame(Page5))

        # button2 showing frame 1 (Page1)
        button2 = ttk.Button(interactionFrame, text="View All Trips", style="start.TButton",
                             command=lambda: controller.show_frame(Page1))

        # placing buttons in the interactionFrame rows respectively
        button1.grid(row=0, pady=(0, 5), sticky=NSEW)
        button2.grid(row=1, pady=(5, 0), sticky=NSEW)



# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Trips", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        #Navigation
        button1 = ttk.Button(self, text="Main Page",
                             command=lambda: controller.show_frame(StartPage))
        button2 = ttk.Button(self, text="Travelers",
                             command=lambda: controller.show_frame(Page2))
        button3 = ttk.Button(self, text="Add Trip",
                             command=lambda: controller.show_frame(Page5))

        button1.place(relx=0.01, rely=0.57, relheight=0.05, relwidth=0.2)
        button2.place(relx=0.01, rely=0.65, relheight=0.05, relwidth=0.2)
        button3.place(relx=0.4, rely=0.65, relheight=0.05, relwidth=0.2)

        # Treeview
        # building tree view
        tree_frame = tk.Frame(self)
        tree_frame.place(relx=0.01, rely=0.135, relheight=0.4, relwidth=0.98)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree['columns'] = (
            "Trip_ID", "Trip Name", "Destination", "Start Date", "End Date", "Duration", "Notes", "Total Expenditure")
        # #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
        my_tree.column("#0", width=0, stretch="NO")
        my_tree.column("Trip_ID", anchor="center", width=40)
        my_tree.column("Trip Name", anchor="w", width=160)
        my_tree.column("Destination", anchor="center", width=70)
        my_tree.column("Start Date", anchor="center", width=70)
        my_tree.column("End Date", anchor="center", width=70)
        my_tree.column("Duration", anchor="center", width=70)
        my_tree.column("Notes", anchor="w", width=70)
        my_tree.column("Total Expenditure", anchor="center", width=70)

        # my_tree.heading("#0", text="#", anchor=W)
        my_tree.heading("Trip_ID", text="Trip_ID", anchor="center")
        my_tree.heading("Trip Name", text="Trip Name", anchor="w")
        my_tree.heading("Destination", text="Destination", anchor="center")
        my_tree.heading("Start Date", text="Start Date", anchor="center")
        my_tree.heading("End Date", text="End Date", anchor="center")
        my_tree.heading("Duration", text="Duration", anchor="center")
        my_tree.heading("Notes", text="Notes", anchor="center")
        my_tree.heading("Total Expenditure", text="Total Expenditure", anchor="center")

        wrapper1 = tk.LabelFrame(self, text="Edit")


        # Placing widgets
        my_tree.pack(fill="x")
        tree_scroll.config(command=my_tree.yview)

        # Calls
        #functions.filltree(my_tree, "Trip")


# Travelers Screen
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Travelers", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Trip",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Main page",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

#Itinerary Screen
class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Itinerary", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Go back to Trips",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

#Events Screen
class Page4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Events", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Go back to Itinerary",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Main page",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

#Add Trip
class Page5(tk.Frame):
    def tripvalidate(self, name, start, end, dur, notes, controller):
        if name == "" or start == "" or end == "" or dur == "" or notes == "":
            messagebox.showinfo(parent=self, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return
        if int(dur) <= 0:
            messagebox.showinfo(parent=self, title="Trip Duration Error", message="End date cannot be earlier than the start date.")
            return
        conn = sqlite3.connect("tplanner.db")
        add = conn.execute("INSERT INTO Trip (Trip_Name, Start_Date, End_Date, Duration, Notes) VALUES ('{}','{}','{}','{}','{}')".format(name, start, end, dur, notes))
        conn.commit()
        conn.close()
        controller.show_frame(Page1)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # configuring column 0 to be the dominant column
        self.columnconfigure(0, weight=1)

        # header title and configuration
        labelConfig = Font(self, size=50, weight=BOLD)
        label = ttk.Label(self, text="Add New Trip", font=labelConfig, foreground='#101010')

        # subheader and congfiguration
        subheaderConfig = Font(self, size=16)
        subheader = ttk.Label(self, text='Enter the details of your trip', font=subheaderConfig, foreground='#808080')
        
        # LABELFRAME housing the required entries
        interactionFrame = LabelFrame(self, text="", pady=30)

        # placing header, subheader, and interactionframe
        # in grid-table in frame(self)
        label.grid(row=0, sticky=S, pady=(30,0))
        subheader.grid(row=1, pady=(0,20))
        interactionFrame.grid(row=2, padx=350, pady=(0,20), sticky=NSEW)

        # configuring column weights in interactionFrame
        interactionFrame.columnconfigure(0, weight=3)
        interactionFrame.columnconfigure(1, weight=5)

        # styling 'add trip' button font
        b = ttk.Style()
        b.configure("add.TButton", font=("Arial", 16))

        # button1 adding the information to the database
        button1 = ttk.Button(self, text="Add Trip", style="add.TButton",
                             command=lambda: self.tripvalidate(tb_name.get(), tb_start.get(),
                             tb_end.get(), tb_duration.get(), tb_notes.get("1.0", 'end-1c'), controller))
        # button2 showing Page1 (all trips page)
        button2 = ttk.Button(self, text="View All Trips",
                             command=lambda: controller.show_frame(Page1))
        # button3 showing StartPage (start menu)
        button3 = ttk.Button(self, text="Return to Main Menu",
                             command=lambda: controller.show_frame(StartPage))

        # placing the BUTTONS using grid in hierarchical arrangement
        # button1 being the largest button
        button1.grid(row=3, column=0, columnspan=2, ipady=15, padx=350, pady=(0,5), sticky=NSEW)
        button2.grid(row=4, column=0, ipady=5, padx=350, pady=(0,5), sticky=EW)
        button3.grid(row=5, column=0, ipady=5, padx=350, pady=(0,30), sticky=EW)

        # LABELS for the required information for 'add trip'
        lab_name = ttk.Label(interactionFrame, text="Name")
        lab_std = ttk.Label(interactionFrame, text="Start Date")
        lab_etd = ttk.Label(interactionFrame, text="End Date")
        lab_duration = ttk.Label(interactionFrame, text="Duration")
        lab_notes = ttk.Label(interactionFrame, text="Notes")

        # ENTRIES for the required information for 'add trip'
        tb_name = ttk.Entry(interactionFrame, width=15)
        tb_start = DateEntry(interactionFrame, width=15)
        tb_end = DateEntry(interactionFrame, width=15)
        tb_duration = ttk.Entry(interactionFrame, width=15)
        tb_notes = Text(interactionFrame, width=15, height=6)

        # placing the LABELS using GRID in the interactionFrame, column 0
        lab_name.grid(row=0, column=0)
        lab_std.grid(row=1, column=0)
        lab_etd.grid(row=2, column=0)
        lab_duration.grid(row=3, column=0)
        lab_notes.grid(row=4, column=0)

        # placing the ENTRIES using GRID in the interactionFrame, column 1
        tb_name.grid(row=0, column=1, ipady=5, padx=(0,50), pady=5, sticky=EW)
        tb_start.grid(row=1, column=1, ipady=5, padx=(0,50), pady=5, sticky=EW)
        tb_end.grid(row=2, column=1, ipady=5, padx=(0,50), pady=5, sticky=EW)
        tb_duration.grid(row=3, column=1, ipady=5, padx=(0,50), pady=5, sticky=EW)
        tb_notes.grid(row=4, column=1, ipady=5, padx=(0,50), pady=5, sticky=EW)

        # DURATION entry configuration
        tb_duration.config(state="disable")
        tb_start.bind('<<DateEntrySelected>>', lambda e: functions.calcdur(tb_start.get_date(), tb_end.get_date(), tb_duration))
        tb_end.bind('<<DateEntrySelected>>', lambda e: functions.calcdur(tb_start.get_date(), tb_end.get_date(), tb_duration))
        tb_duration.insert(END,' days')

# Driver Code
app = tkinterApp()
app.mainloop()


