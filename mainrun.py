from os import remove
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

# This is the mainrun file for the Travel-Planner, follows the following order of content:
# setupDB -> global variable -> mainscreen setup-> setup buttons,labels -> calls and executions -> eventhandling
# Note: Functions are found in functions.py

sqlcalls.setupDB()

LARGEFONT = ("Verdana", 35)

# Global Variables

trackTrip = ""
trackItin = ""


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        width = 1200
        height = 700
        self.minsize(width, height)
        self.title("Travel Planner")
        self.resizable(False, False)
        x = functions.getcenterX(width, self.container)
        y = functions.getcenterY(height, self.container)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2, Page3, Page4, Page5, TripDetails):
            frame = F(self.container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        updateframe = cont(self.container, controller=self)
        self.frames[cont] = updateframe
        updateframe.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]

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

        # Navigation
        button1 = ttk.Button(self, text="Main Page",
                             command=lambda: controller.show_frame(StartPage))
        button2 = ttk.Button(self, text="Travelers",
                             command=lambda: controller.show_frame(Page2))
        button3 = ttk.Button(self, text="Add Trip",
                             command=lambda: controller.show_frame(Page5))
        button4 = ttk.Button(self, text="View Trip Details",
                             command=lambda: controller.show_frame(TripDetails))

        button1.place(relx=0.01, rely=0.75, relheight=0.05, relwidth=0.2)
        button2.place(relx=0.01, rely=0.67, relheight=0.05, relwidth=0.2)
        button3.place(relx=0.01, rely=0.55, relheight=0.05, relwidth=0.2)
        button4.place(relx=0.01, rely=0.61, relheight=0.05, relwidth=0.2)

        # Treeview
        # building tree view
        tree_frame = tk.Frame(self)
        tree_frame.place(relx=0.01, rely=0.135, relheight=0.4, relwidth=0.98)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree['columns'] = (
            "Trip_ID", "Trip Name", "Start Date", "End Date", "Duration", "Notes", "Total Expenditure")
        # #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
        my_tree.column("#0", width=0, stretch="NO")
        my_tree.column("Trip_ID", anchor="center", width=40)
        my_tree.column("Trip Name", anchor="w", width=160)
        # my_tree.column("Destination", anchor="center", width=70)
        my_tree.column("Start Date", anchor="center", width=70)
        my_tree.column("End Date", anchor="center", width=70)
        my_tree.column("Duration", anchor="center", width=70)
        my_tree.column("Notes", anchor="w", width=70)
        my_tree.column("Total Expenditure", anchor="center", width=70)

        # my_tree.heading("#0", text="#", anchor=W)
        my_tree.heading("Trip_ID", text="Trip ID", anchor="center")
        my_tree.heading("Trip Name", text="Trip Name", anchor="w")
        # my_tree.heading("Destination", text="Destination", anchor="center")
        my_tree.heading("Start Date", text="Start Date", anchor="center")
        my_tree.heading("End Date", text="End Date", anchor="center")
        my_tree.heading("Duration", text="Duration", anchor="center")
        my_tree.heading("Notes", text="Notes", anchor="center")
        my_tree.heading("Total Expenditure", text="Total Expenditure", anchor="center")

        wrapper2 = tk.LabelFrame(self, text="Destinations")
        tree_frame1 = tk.Frame(wrapper2)
        tree_frame1.place(relx=0.01, rely=0.05, relheight=0.4, relwidth=0.98)
        tree_scroll1 = tk.Scrollbar(tree_frame1)
        tree_scroll1.pack(side="right", fill="y")
        my_tree1 = ttk.Treeview(tree_frame1, yscrollcommand=tree_scroll1.set)
        my_tree1['columns'] = (
            "ID", "Destination")
        my_tree1.column("#0", width=0, stretch="NO")
        my_tree1.column("ID", anchor="center", width=10)
        my_tree1.column("Destination", anchor="w", width=650)
        my_tree1.heading("ID", text="ID", anchor="center")
        my_tree1.heading("Destination", text="Destination", anchor="w")

        # wrapper1 = tk.LabelFrame(self, text="Edit")
        # buttonedit = ttk.Button(wrapper1, text="Edit Entry", command=lambda: editOrDeleteEntry())
        # buttondelete = ttk.Button(wrapper1, text="Delete Entry", command=lambda: editOrDeleteEntry(TRUE))

        destadd = ttk.Button(wrapper2, text="Add", command=lambda: functions.addEntry(destadd, my_tree, my_tree1, self))
        destedit = ttk.Button(wrapper2, text="Edit",
                              command=lambda: functions.editDestination(destedit, my_tree1, self))
        destdelete = ttk.Button(wrapper2, text="Delete", command=lambda: deleteDest())

        # lab_name = ttk.Label(wrapper1, text="Name")
        # lab_std = ttk.Label(wrapper1, text="Start Date")
        # lab_etd = ttk.Label(wrapper1, text="End Date")
        # lab_duration = ttk.Label(wrapper1, text="Duration")
        # lab_notes = ttk.Label(wrapper1, text="Notes")

        # tb_name = ttk.Entry(wrapper1, width=15)
        # tb_duration = ttk.Entry(wrapper1, width=15)
        # tb_notes = Text(wrapper1, width=15)
        # tb_start = DateEntry(wrapper1, width=15)
        # tb_end = DateEntry(wrapper1, width=15)

        # lab_name.place(relx=0.11, rely=0.07, relheight=0.06, relwidth=0.14)
        # lab_std.place(relx=0.103, rely=0.16, relheight=0.06, relwidth=0.14)
        # lab_etd.place(relx=0.105, rely=0.25, relheight=0.06, relwidth=0.14)
        # lab_duration.place(relx=0.105, rely=0.33, relheight=0.06, relwidth=0.14)
        # lab_notes.place(relx=0.11, rely=0.42, relheight=0.06, relwidth=0.14)

        # tb_name.place(relx=0.28, rely=0.07, relheight=0.07, relwidth=0.6)
        # tb_start.place(relx=0.28, rely=0.16, relheight=0.07, relwidth=0.6)
        # tb_end.place(relx=0.28, rely=0.25, relheight=0.07, relwidth=0.6)
        # tb_duration.place(relx=0.28, rely=0.33, relheight=0.07, relwidth=0.6)
        # tb_notes.place(relx=0.28, rely=0.42, relheight=0.33, relwidth=0.6)
        # tb_duration.config(state="disable")
        # tb_start.bind('<<DateEntrySelected>>', lambda e: functions.calcdur(tb_start.get_date(), tb_end.get_date(), tb_duration))
        # tb_end.bind('<<DateEntrySelected>>', lambda e: functions.calcdur(tb_start.get_date(), tb_end.get_date(), tb_duration))

        # wrapper1.place(relx=0.22, rely=0.48, relheight=0.5, relwidth=0.4)
        wrapper2.place(relx=0.22, rely=0.48, relheight=0.5, relwidth=0.76)
        # buttonedit.place(relx=0.28, rely=0.85, relheight=0.11, relwidth=0.2)
        # buttondelete.place(relx=0.52, rely=0.85, relheight=0.11, relwidth=0.2)
        destadd.place(relx=0.02, rely=0.85, relheight=0.11, relwidth=0.2)
        destedit.place(relx=0.26, rely=0.85, relheight=0.11, relwidth=0.2)
        destdelete.place(relx=0.50, rely=0.85, relheight=0.11, relwidth=0.2)
        functions.filltree(my_tree, "Trip")
        # Placing widgets
        my_tree.pack(fill="x")
        my_tree1.pack(fill="x")
        tree_scroll.config(command=my_tree.yview)
        my_tree.bind('<<TreeviewSelect>>', lambda e: onFocus())

        def onFocus():
            # tb_name.delete(0, END)
            # tb_start.delete(0, END)
            # tb_end.delete(0, END)
            # tb_duration.config(state=NORMAL)
            # tb_duration.delete(0, END)
            # tb_duration.config(state=DISABLED)
            # tb_notes.delete(1.0, END)
            selected = my_tree.focus()
            values = my_tree.item(selected, 'values')

            global trackTrip
            trackTrip = values[0]
            # print("Tracked:", trackTrip)
            try:
                conn = sqlite3.connect("tplanner.db")
                data = conn.execute(f"SELECT * FROM Trip WHERE Trip_id={values[0]} ").fetchall()[0]
                conn.close()
                # tb_name.insert(0, data[1])
                # tb_start.insert(0, data[2])
                # tb_end.insert(0, data[3])
                # tb_duration.config(state=NORMAL)
                # tb_duration.insert(0, data[4])
                # tb_duration.config(state=DISABLED)
                # tb_notes.insert(tk.END, data[5])
                functions.filltree(my_tree1, "Trip_Destination", data[0])
            except:
                print("")

        # Delete Dest
        def deleteDest():
            selected = my_tree1.focus()
            values = my_tree1.item(selected, 'values')
            conn = sqlite3.connect("tplanner.db")
            exec = conn.execute(f"DELETE FROM Trip_Destination WHERE TripD_ID = '{values[0]}'")
            conn.commit()
            conn.close()
            my_tree1.delete(*my_tree1.get_children())
            functions.filltree(my_tree1, "Trip_Destination", values[2])


# Travelers Screen
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        # title of page
        labelConfig = Font(self, size=50, weight=BOLD)
        label = ttk.Label(self, text="Travelers", font=labelConfig, foreground='#101010')
        label.grid(columnspan=2, padx=(20,0), pady=10, sticky=S)

        button1 = ttk.Button(self, text="Main Page",
                             command=lambda: controller.show_frame(Page1))
        # creating the wrapper for treeview of Travelers
        destTreeWrapper = tk.LabelFrame(self, text="Travelers")
        destTreeWrapper.grid(row=1, column=1, padx=(5, 50), pady=20, sticky=EW)
        # destTreeWrapper.columnconfigure(0, weight=1)
        # destTreeWrapper.rowconfigure(0, weight=1)

        # treeview of Travelers
        travTreeFrame = tk.Frame(destTreeWrapper)
        travTreeFrame.pack(fill='both', padx=20, pady=30)

        travTreeScroll = tk.Scrollbar(travTreeFrame)
        travTreeScroll.pack(side="right", fill="y")
        travTree = ttk.Treeview(travTreeFrame, yscrollcommand=travTreeScroll.set)
        travTree['columns'] = (
            "Traveler_ID", "Name", "Age", "Gender", "Address"
        )
        # defining columns in treeview
        travTree.column("#0", width=0, stretch="NO")
        travTree.column("Traveler_ID", anchor="w", width=2)
        travTree.column("Name", anchor="w", width=125)
        travTree.column("Age", anchor="w", width=2)
        travTree.column("Gender", anchor="w", width=20)
        travTree.column("Address", anchor="w", width=200)
        travTree.heading("Traveler_ID", text="ID", anchor="w")
        travTree.heading("Name", text="Name", anchor="w")
        travTree.heading("Age", text="Age", anchor="w")
        travTree.heading("Gender", text="Gender", anchor="w")
        travTree.heading("Address", text="Address", anchor="w")

        # packing treeview in travTree
        travTree.pack(fill='both')
        travTreeScroll.config(command=travTree.yview)

        # -----TRAVELER DETAILS-----
        travelerWrapper = tk.LabelFrame(self, text="Traveler Details")
        travelerWrapper.grid(row=1, column=0, padx=(50, 5), pady=20, sticky=EW)

        # travelerWrapper.rowconfigure(0, weight=1)
        travelerWrapper.columnconfigure(0, weight=1)
        travelerWrapper.columnconfigure(1, weight=1)
        travelerWrapper.columnconfigure(2, weight=1)

        # traveler labels
        nameTraveler = ttk.Label(travelerWrapper, text="Name")
        ageTraveler = ttk.Label(travelerWrapper, text="Age")
        genderTraveler = ttk.Label(travelerWrapper, text="Gender")
        addressTraveler = ttk.Label(travelerWrapper, text="Address")

        nameTravelerEnt = ttk.Entry(travelerWrapper, width=30)
        ageTravelerEnt = ttk.Entry(travelerWrapper, width=30)
        genderTravelerEnt = ttk.Entry(travelerWrapper, width=30)
        addressTravelerEnt = ttk.Entry(travelerWrapper, width=30)

        nameTraveler.grid(row=0, column=0, pady=(40, 0))
        ageTraveler.grid(row=1, column=0)
        genderTraveler.grid(row=2, column=0)
        addressTraveler.grid(row=3, column=0, pady=(0, 30))

        nameTravelerEnt.grid(row=0, column=1, columnspan=2, ipady=2, padx=(0, 20), pady=(40, 3), sticky=EW)
        ageTravelerEnt.grid(row=1, column=1, columnspan=2, ipady=2, padx=(0, 20), pady=3, sticky=EW)
        genderTravelerEnt.grid(row=2, column=1, columnspan=2, ipady=2, padx=(0, 20), pady=3, sticky=EW)
        addressTravelerEnt.grid(row=3, column=1, columnspan=2, ipady=2, padx=(0, 20), pady=(3, 30), sticky=EW)

        addTraveler = ttk.Button(travelerWrapper, text="Add Traveler", command=lambda: addtravel())
        updateTraveler = ttk.Button(travelerWrapper, text="Update Traveler", command=lambda: edittravel())
        removeTraveler = ttk.Button(travelerWrapper, text="Remove Traveler", command=lambda: deletetravel())

        addTraveler.grid(row=4, column=0, ipadx=14, ipady=3, padx=(30, 0), pady=34, sticky=SW)
        updateTraveler.grid(row=4, column=1, ipadx=10, ipady=3, pady=34, sticky=SW)
        removeTraveler.grid(row=4, column=2, ipadx=10, ipady=3, pady=34, sticky=SW)
        allTripsButton = ttk.Button(self, text="View All Trips",
                                    command=lambda: controller.show_frame(Page1))
        mainMenuButton = ttk.Button(self, text="Main Menu",
                                    command=lambda: controller.show_frame(StartPage))

        allTripsButton.grid(row=1, column=0, ipadx=50, ipady=10, padx=(250, 0), pady=(0, 80), sticky=SW)
        mainMenuButton.grid(row=1, column=0, ipadx=50, ipady=10, padx=(50, 0), pady=(0, 80), sticky=SW)

        functions.filltree(travTree, "Traveler")
        travTree.bind('<<TreeviewSelect>>', lambda e: onFocus())

        def onFocus():
            nameTravelerEnt.delete(0, END)
            ageTravelerEnt.delete(0, END)
            genderTravelerEnt.delete(0, END)
            addressTravelerEnt.delete(0, END)
            selected = travTree.focus()
            values = travTree.item(selected, 'values')
            nameTravelerEnt.insert(0, values[1])
            ageTravelerEnt.insert(0, values[2])
            genderTravelerEnt.insert(0, values[3])
            addressTravelerEnt.insert(0, values[4])

        def addtravel():
            t1 = nameTravelerEnt.get()
            t2 = ageTravelerEnt.get()
            t3 = genderTravelerEnt.get()
            t4 = addressTravelerEnt.get()
            if t1 == "" or t2 == "" or t3 == "" or t4 == "":
                messagebox.showinfo(parent=self, title="Incomplete Information",
                                    message="All textboxes need to be filled to complete the action")

            conn = sqlite3.connect("tplanner.db")
            data = conn.execute(f"SELECT * FROM Traveler")
            for line in data:
                if line[1].lower() == t1.lower():
                    messagebox.showinfo(parent=self, title="Already Exists",
                                        message="This Destination name already exists")
                    return
            add = conn.execute(
                "INSERT INTO Traveler (Name, Age, Gender, Address) VALUES ('{}', '{}', '{}', '{}')".format(t1, t2, t3,
                                                                                                           t4))
            conn.commit()
            conn.close()
            functions.filltree(travTree, "Traveler")
            nameTravelerEnt.delete(0, END)
            ageTravelerEnt.delete(0, END)
            genderTravelerEnt.delete(0, END)
            addressTravelerEnt.delete(0, END)
            return

        def edittravel():

            t1 = nameTravelerEnt.get()
            t2 = ageTravelerEnt.get()
            t3 = genderTravelerEnt.get()
            t4 = addressTravelerEnt.get()
            if t1 == "" or t2 == "" or t3 == "" or t4 == "":
                messagebox.showinfo(parent=self, title="Incomplete Information",
                                    message="All textboxes need to be filled to complete the action")
            selected = travTree.focus()
            values = travTree.item(selected, 'values')
            conn = sqlite3.connect("tplanner.db")
            data = conn.execute(f"SELECT * FROM Traveler")
            for line in data:
                if line[1].lower() == t1.lower() and line[1].lower() != values[1].lower():
                    messagebox.showinfo(parent=self, title="Already Exists",
                                        message="This Traveler name already exists")
                    return
            add = conn.execute(
                f"UPDATE Traveler Set Name = '{t1}', Age = '{t2}', Gender = '{t3}', Address = '{t4}' WHERE Traveler_ID = '{values[0]}'")
            conn.commit()
            conn.close()
            functions.filltree(travTree, "Traveler")
            nameTravelerEnt.delete(0, END)
            ageTravelerEnt.delete(0, END)
            genderTravelerEnt.delete(0, END)
            addressTravelerEnt.delete(0, END)
            return

        def deletetravel():
            result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
            if result == 'yes':
                selected = travTree.focus()
                values = travTree.item(selected, 'values')
                conn = sqlite3.connect("tplanner.db")
                exec = conn.execute(f"DELETE FROM Traveler WHERE Traveler_ID = '{values[0]}'")
                conn.commit()
                conn.close()
                functions.filltree(travTree, "Traveler")
            else:
                return


# Itinerary Screen
class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Itinerary", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Main Page",
                             command=lambda: controller.show_frame(StartPage))
        button2 = ttk.Button(self, text="Go Back",
                             command=lambda: controller.show_frame(TripDetails))
        button3 = ttk.Button(self, text="Add Itinerary",
                             command=lambda: functions.addItin(button3, my_tree, trackTrip, self))
        button4 = ttk.Button(self, text="Edit Itinerary",
                             command=lambda: functions.editItin(button4, my_tree, trackTrip, self))
        button5 = ttk.Button(self, text="Delete Itinerary",
                             command=lambda: deleteItin())

        button1.place(relx=0.01, rely=0.75, relheight=0.05, relwidth=0.2)
        button2.place(relx=0.01, rely=0.81, relheight=0.05, relwidth=0.2)
        button3.place(relx=0.01, rely=0.55, relheight=0.05, relwidth=0.2)
        button4.place(relx=0.01, rely=0.61, relheight=0.05, relwidth=0.2)
        button5.place(relx=0.01, rely=0.67, relheight=0.05, relwidth=0.2)
        # Treeview
        # building tree view
        tree_frame = tk.Frame(self)
        tree_frame.place(relx=0.01, rely=0.135, relheight=0.4, relwidth=0.98)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree['columns'] = (
            "Itinerary_ID", "Itinerary_Name", "Description")
        # #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
        my_tree.column("#0", width=0, stretch="NO")
        my_tree.column("Itinerary_ID", anchor="center", width=20)
        my_tree.column("Itinerary_Name", anchor="center", width=50)
        my_tree.column("Description", anchor="w", width=300)

        # my_tree.heading("#0", text="#", anchor=W)
        my_tree.heading("Itinerary_ID", text="ID", anchor="center")
        my_tree.heading("Itinerary_Name", text="Itinerary_Name", anchor="center")
        my_tree.heading("Description", text="Description", anchor="center")
        functions.filltree(my_tree, "Itinerary", trackTrip)
        wrapper2 = tk.LabelFrame(self, text="Destinations")
        tree_frame1 = tk.Frame(wrapper2)
        tree_frame1.place(relx=0.01, rely=0.05, relheight=0.7, relwidth=0.98)
        tree_scroll1 = tk.Scrollbar(tree_frame1)
        tree_scroll1.pack(side="right", fill="y")
        my_tree1 = ttk.Treeview(tree_frame1, yscrollcommand=tree_scroll1.set)
        my_tree1['columns'] = (
            "ID", "Name", "Location", "Start DateTime", "End DateTime", "Type", "Notes", "Expenses")
        my_tree1.column("#0", width=0, stretch="NO")
        my_tree1.column("ID", anchor="center", width=40)
        my_tree1.column("Name", anchor="w", width=40)
        my_tree1.column("Location", anchor="center", width=40)
        my_tree1.column("Start DateTime", anchor="center", width=40)
        my_tree1.column("End DateTime", anchor="center", width=40)
        my_tree1.column("Type", anchor="center", width=40)
        my_tree1.column("Notes", anchor="center", width=80)
        my_tree1.column("Expenses", anchor="center", width=40)

        my_tree1.heading("ID", text="ID", anchor="center")
        my_tree1.heading("Name", text="Name", anchor="w")
        my_tree1.heading("Location", text="Location", anchor="center")
        my_tree1.heading("Start DateTime", text="Start DateTime", anchor="center")
        my_tree1.heading("End DateTime", text="End DateTime", anchor="center")
        my_tree1.heading("Type", text="Type", anchor="center")
        my_tree1.heading("Notes", text="Notes", anchor="center")
        my_tree1.heading("Expenses", text="Expenses", anchor="center")
        wrapper2.place(relx=0.22, rely=0.48, relheight=0.5, relwidth=0.776)

        # destination edit and delete buttons
        destadd = ttk.Button(wrapper2, text="Add",
                             command=lambda: functions.addEvent(destadd, my_tree, my_tree1, trackItin, self))
        destedit = ttk.Button(wrapper2, text="Edit",
                              command=lambda: functions.editevent(destedit, my_tree, my_tree1, trackItin, self))
        destdelete = ttk.Button(wrapper2, text="Delete", command=lambda: deleteEvent())

        destadd.place(relx=0.02, rely=0.85, relheight=0.11, relwidth=0.2)
        destedit.place(relx=0.26, rely=0.85, relheight=0.11, relwidth=0.2)
        destdelete.place(relx=0.50, rely=0.85, relheight=0.11, relwidth=0.2)
        # Placing widgets
        my_tree.pack(fill="x")
        my_tree1.pack(fill="x")
        tree_scroll.config(command=my_tree.yview)
        my_tree.bind('<<TreeviewSelect>>', lambda e: onFocus())

        def onFocus():
            global trackItin
            # clear textboxes
            # get info from selected
            selected = my_tree.focus()
            values = my_tree.item(selected, 'values')
            print(values)
            #
            trackItin = values[0]
            functions.filltree(my_tree1, "Events", values[0])

        # Delete Dest
        def deleteItin():
            result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
            if result == 'yes':
                selected = my_tree.focus()
                values = my_tree.item(selected, 'values')
                conn = sqlite3.connect("tplanner.db")
                exec = conn.execute(f"DELETE FROM Itinerary WHERE Itinerary_ID = '{values[0]}'")
                conn.commit()
                conn.close()
                my_tree.delete(*my_tree.get_children())
                functions.filltree(my_tree, "Itinerary", values[3])
            else:
                return

        # Delete Dest
        def deleteEvent():
            result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
            if result == 'yes':
                selected = my_tree1.focus()
                values = my_tree1.item(selected, 'values')
                conn = sqlite3.connect("tplanner.db")
                exec = conn.execute(f"DELETE FROM Events WHERE Events_ID = '{values[0]}'")
                conn.commit()
                conn.close()
                my_tree1.delete(*my_tree1.get_children())
                functions.filltree(my_tree, "Events", values[8])
            else:
                return


# Events Screen
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


# Add Trip
class Page5(tk.Frame):
    def tripvalidate(self, name, start, end, dur, notes, controller):
        if name == "" or start == "" or end == "" or dur == "" or notes == "":
            messagebox.showinfo(parent=self, title="Incomplete Information",
                                message="All textboxes need to be filled to complete the action")
            return
        if int(dur) <= 0:
            messagebox.showinfo(parent=self, title="Trip Duration Error",
                                message="End date cannot be earlier than the start date.")
            return
        conn = sqlite3.connect("tplanner.db")
        add = conn.execute(
            "INSERT INTO Trip (Trip_Name, Start_Date, End_Date, Duration, Notes) VALUES ('{}','{}','{}','{}','{}')".format(
                name, start, end, dur, notes))
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
        label.grid(row=0, sticky=S, pady=(30, 0))
        subheader.grid(row=1, pady=(0, 20))
        interactionFrame.grid(row=2, padx=350, pady=(0, 20), sticky=NSEW)

        # configuring column weights in interactionFrame
        interactionFrame.columnconfigure(0, weight=3)
        interactionFrame.columnconfigure(1, weight=5)

        # styling 'add trip' button font
        b = ttk.Style()
        b.configure("add.TButton", font=("Arial", 16))

        # button1 adding the information to the database
        button1 = ttk.Button(self, text="Add Trip", style="add.TButton",
                             command=lambda: self.tripvalidate(tb_name.get(), tb_start.get(),
                                                               tb_end.get(), tb_duration.get(),
                                                               tb_notes.get("1.0", 'end-1c'), controller))
        # button2 showing Page1 (all trips page)
        button2 = ttk.Button(self, text="View All Trips",
                             command=lambda: controller.show_frame(Page1))
        # button3 showing StartPage (start menu)
        button3 = ttk.Button(self, text="Return to Main Menu",
                             command=lambda: controller.show_frame(StartPage))

        # placing the BUTTONS using grid in hierarchical arrangement
        # button1 being the largest button
        button1.grid(row=3, column=0, columnspan=2, ipady=15, padx=350, pady=(0, 5), sticky=NSEW)
        button2.grid(row=4, column=0, ipady=5, padx=350, pady=(0, 5), sticky=EW)
        button3.grid(row=5, column=0, ipady=5, padx=350, pady=(0, 30), sticky=EW)

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
        tb_name.grid(row=0, column=1, ipady=5, padx=(0, 50), pady=5, sticky=EW)
        tb_start.grid(row=1, column=1, ipady=5, padx=(0, 50), pady=5, sticky=EW)
        tb_end.grid(row=2, column=1, ipady=5, padx=(0, 50), pady=5, sticky=EW)
        tb_duration.grid(row=3, column=1, ipady=5, padx=(0, 50), pady=5, sticky=EW)
        tb_notes.grid(row=4, column=1, ipady=5, padx=(0, 50), pady=5, sticky=EW)

        # DURATION entry configuration
        tb_duration.config(state="disable")
        tb_start.bind('<<DateEntrySelected>>',
                      lambda e: functions.calcdur(tb_start.get_date(), tb_end.get_date(), tb_duration))
        tb_end.bind('<<DateEntrySelected>>',
                    lambda e: functions.calcdur(tb_start.get_date(), tb_end.get_date(), tb_duration))


# Trip Details Screen
class TripDetails(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # configuring column-row weights in self
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)

        # page title
        label = ttk.Label(self, text="Trip Details", font=LARGEFONT)
        label.grid(row=0, column=0, padx=20, pady=20, sticky=SW)

        # RETURN to Trips page button
        tripPageButton = ttk.Button(self, text="Return to All Trips",
                                    command=lambda: controller.show_frame(Page1))
        tripPageButton.grid(row=0, column=0, ipadx=10, ipady=5, padx=20, sticky=SE)
        tripPageButton.grid(row=2, column=0, ipadx=80, ipady=10, padx=50, pady=(0, 70), sticky=S)

        # VIEW ALL TRAVELLERS page button
        travelersButton = ttk.Button(self, text="View All Travelers",
                                     command=lambda: controller.show_frame(Page2))
        travelersButton.grid(row=2, column=0, ipadx=82, ipady=10, padx=50, pady=(70, 0), sticky=N)
        GoItinerary = ttk.Button(self, text="Check Itinerary",
                                 command=lambda: controller.show_frame(Page3))
        GoItinerary.grid(row=0, column=1, ipadx=10, ipady=5, padx=20, sticky=SE)

        # creating the wrapper for treeview of Travelers
        destTreeWrapper = tk.LabelFrame(self, text="Travelers")
        destTreeWrapper.grid(row=1, column=1, padx=(5, 20), pady=(20, 5), sticky=NSEW)
        # destTreeWrapper.columnconfigure(0, weight=1)
        # destTreeWrapper.rowconfigure(0, weight=1)

        # treeview of Travelers
        travTreeFrame = tk.Frame(destTreeWrapper)
        travTreeFrame.pack(fill='both', padx=20, pady=30)

        travTreeScroll = tk.Scrollbar(travTreeFrame)
        travTreeScroll.pack(side="right", fill="y")
        travTree = ttk.Treeview(travTreeFrame, yscrollcommand=travTreeScroll.set)
        travTree['columns'] = (
            "Traveler_ID", "Name", "Age", "Gender", "Address"
        )
        # defining columns in treeview
        travTree.column("#0", width=0, stretch="NO")
        travTree.column("Traveler_ID", anchor="w", width=2)
        travTree.column("Name", anchor="w", width=125)
        travTree.column("Age", anchor="w", width=2)
        travTree.column("Gender", anchor="w", width=20)
        travTree.column("Address", anchor="w", width=200)
        travTree.heading("Traveler_ID", text="ID", anchor="w")
        travTree.heading("Name", text="Name", anchor="w")
        travTree.heading("Age", text="Age", anchor="w")
        travTree.heading("Gender", text="Gender", anchor="w")
        travTree.heading("Address", text="Address", anchor="w")

        # packing treeview in travTree
        travTree.pack(fill='both')
        travTreeScroll.config(command=travTree.yview)

        # wrapper for trip details
        editWrapper = tk.LabelFrame(self, text="Trip Details")
        editWrapper.grid(row=1, column=0, padx=(20, 5), pady=(20, 5), sticky=NSEW)

        # configuring column in editWrapper
        editWrapper.columnconfigure(0, weight=1)

        # labels in editWrapper
        lab_name = ttk.Label(editWrapper, text="Name")
        lab_std = ttk.Label(editWrapper, text="Start Date")
        lab_etd = ttk.Label(editWrapper, text="End Date")
        lab_duration = ttk.Label(editWrapper, text="Duration")
        lab_notes = ttk.Label(editWrapper, text="Notes")

        # entries in editWrapper
        tb_name = ttk.Entry(editWrapper, width=30)
        tb_start = DateEntry(editWrapper, width=30)
        tb_end = DateEntry(editWrapper, width=30)
        tb_duration = ttk.Entry(editWrapper, width=30)
        tb_notes = Text(editWrapper, width=30, height=6)  # height -> line numbers NOT pixels

        # placing the labels and entries in editWrapper
        lab_name.grid(row=0, column=0, pady=(20, 0))
        lab_std.grid(row=1, column=0)
        lab_etd.grid(row=2, column=0)
        lab_duration.grid(row=3, column=0)
        lab_notes.grid(row=4, column=0)

        tb_name.grid(row=0, column=1, ipady=1, padx=(0, 20), pady=(20, 2), sticky=EW)
        tb_start.grid(row=1, column=1, ipady=1, padx=(0, 20), pady=2, sticky=EW)
        tb_end.grid(row=2, column=1, ipady=1, padx=(0, 20), pady=2, sticky=EW)
        tb_duration.grid(row=3, column=1, ipady=1, padx=(0, 20), pady=2, sticky=EW)
        tb_notes.grid(row=4, column=1, ipady=1, padx=(0, 20), pady=(2, 20), sticky=NSEW)

        tripEditButton = ttk.Button(editWrapper, text="Update Trip", width=15,
                                    command=lambda: editOrDeleteEntry())
        tripDeleteButton = ttk.Button(editWrapper, text="Remove Trip", width=15,
                                      command=lambda: editOrDeleteEntry(TRUE))

        tripEditButton.grid(row=5, column=0, ipady=3, padx=(20, 0), sticky=SW)
        tripDeleteButton.grid(row=5, column=1, ipady=3, sticky=SW)

        # -----TRAVELER DETAILS-----
        travelerWrapper = tk.LabelFrame(self, text="Traveler Details")
        travelerWrapper.grid(row=2, column=1, padx=(5, 20), pady=(5, 20), sticky=NSEW)

        # travelerWrapper.rowconfigure(0, weight=1)
        travelerWrapper.columnconfigure(0, weight=1)
        travelerWrapper.columnconfigure(1, weight=1)
        travelerWrapper.columnconfigure(2, weight=1)

        # traveler labels
        nameTraveler = ttk.Label(travelerWrapper, text="Name")
        ageTraveler = ttk.Label(travelerWrapper, text="Age")
        genderTraveler = ttk.Label(travelerWrapper, text="Gender")
        addressTraveler = ttk.Label(travelerWrapper, text="Address")

        nameTravelerEnt = ttk.Entry(travelerWrapper, width=30)
        ageTravelerEnt = ttk.Entry(travelerWrapper, width=30)
        genderTravelerEnt = ttk.Entry(travelerWrapper, width=30)
        addressTravelerEnt = ttk.Entry(travelerWrapper, width=30)

        nameTraveler.grid(row=0, column=0, pady=(30, 0))
        ageTraveler.grid(row=1, column=0)
        genderTraveler.grid(row=2, column=0)
        addressTraveler.grid(row=3, column=0, pady=(0, 30))

        nameTravelerEnt.grid(row=0, column=1, columnspan=2, padx=(0, 20), pady=(30, 2), sticky=EW)
        ageTravelerEnt.grid(row=1, column=1, columnspan=2, padx=(0, 20), pady=2, sticky=EW)
        genderTravelerEnt.grid(row=2, column=1, columnspan=2, padx=(0, 20), pady=2, sticky=EW)
        addressTravelerEnt.grid(row=3, column=1, columnspan=2, padx=(0, 20), pady=(2, 30), sticky=EW)

        addTraveler = ttk.Button(travelerWrapper, text="Add Traveler",
                                 command=lambda: functions.addtriptrav(addTraveler, travTree, trackTrip, self))
        updateTraveler = ttk.Button(travelerWrapper, text="Updated Traveler")
        removeTraveler = ttk.Button(travelerWrapper, text="Remove Traveler", command=lambda: deletetrav())

        addTraveler.grid(row=4, column=0, ipadx=10, ipady=3, padx=20, sticky=SW)
        updateTraveler.grid(row=4, column=1, ipadx=10, ipady=3, sticky=SW)
        removeTraveler.grid(row=4, column=2, ipadx=10, ipady=3, sticky=SW)

        # clearing entries per refresh
        tb_name.delete(0, END)
        tb_start.delete(0, END)
        tb_end.delete(0, END)
        tb_duration.config(state=NORMAL)
        tb_duration.delete(0, END)
        tb_duration.config(state=DISABLED)
        tb_notes.delete(1.0, END)

        # requesting data from DB
        try:
            conn = sqlite3.connect("tplanner.db")
            data = conn.execute(f"SELECT * FROM Trip WHERE Trip_id={trackTrip} ").fetchall()[0]
            conn.close()

            # inserting gathered data from DB to entries
            tb_name.insert(0, data[1])
            tb_start.insert(0, data[2])
            tb_end.insert(0, data[3])
            tb_duration.config(state=NORMAL)
            tb_duration.insert(0, data[4])
            tb_duration.config(state=DISABLED)
            tb_notes.insert(tk.END, data[5])
        except:
            print("")
        functions.filltree(travTree, "Traveler_Trip", trackTrip)

        # delete/edit function for trip details
        def editOrDeleteEntry(delete=FALSE):

            # from global trackTrip
            edit_ID = str(trackTrip)
            conn = sqlite3.connect("tplanner.db")
            data = conn.execute(f"SELECT * FROM Trip WHERE Trip_id={edit_ID} ").fetchall()[0]
            conn.close()

            # from Entries
            n_tb = tb_name.get()
            s_tb = tb_start.get()
            e_tb = tb_end.get()
            d_tb = tb_duration.get()
            no_tb = tb_notes.get("1.0", 'end-1c')
            counter = 0

            if delete:
                result = messagebox.askquestion("Delete",
                                                "Are you sure you would like to delete this trip? This action cannot be undone.",
                                                icon='warning')
                if result == 'yes':
                    conn = sqlite3.connect("tplanner.db")
                    data = conn.execute("DELETE FROM Trip WHERE Trip_ID='{}'".format(edit_ID))
                    conn.commit()
                    conn.close()
                    controller.show_frame(Page1)
                else:
                    return
            else:
                conn = sqlite3.connect("tplanner.db")
                edit = conn.execute(
                    f'UPDATE Trip SET Trip_Name=\'{n_tb}\', Start_date=\'{s_tb}\', End_date=\'{e_tb}\', Duration=\'{d_tb}\', Notes=\'{no_tb}\' WHERE Trip_ID=\'{edit_ID}\'')
                conn.commit()
                conn.close()
                messagebox.showinfo("Edit Trip", "Trip has been successfully updated.")

        def onFocus():
            nameTravelerEnt.delete(0, END)
            ageTravelerEnt.delete(0, END)
            genderTravelerEnt.delete(0, END)
            addressTravelerEnt.delete(0, END)
            selected = travTree.focus()
            values = travTree.item(selected, 'values')
            nameTravelerEnt.insert(0, values[1])
            ageTravelerEnt.insert(0, values[2])
            genderTravelerEnt.insert(0, values[3])
            addressTravelerEnt.insert(0, values[4])

        def deletetrav():
            result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
            if result == 'yes':
                selected = travTree.focus()
                values = travTree.item(selected, 'values')
                conn = sqlite3.connect("tplanner.db")
                exec = conn.execute(f"DELETE FROM Traveler_Trip WHERE TravTrip_ID = '{values[0]}'")
                conn.commit()
                conn.close()
                functions.filltree(travTree, "Traveler_Trip", trackTrip)
            else:
                return


# Driver Code
app = tkinterApp()
app.mainloop()


