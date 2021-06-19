import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
import sqlite3
import sqlcalls
import functions
#This is the mainrun file for the Travel-Planner, follows the following order of content:
#setupDB -> mainscreen setup-> setup buttons,labels -> calls and executions -> eventhandling
#Note: Functions are found in functions.py

sqlcalls.setupDB()

LARGEFONT = ("Verdana", 35)


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
        for F in (StartPage, Page1, Page2):
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
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label of frame Layout 2
        label = ttk.Label(self, text="Travel Planner", font=LARGEFONT)
        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Trips",
                             command=lambda: controller.show_frame(Page1))
        # putting the button in its place by
        # using grid

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Travelers",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button1.place(relx=0.01, rely=0.45, relheight=0.05, relwidth=0.2)
        button2.place(relx=0.01, rely=0.55, relheight=0.05, relwidth=0.2)


        #place here



# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Trips", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Main Page",
                             command=lambda: controller.show_frame(StartPage))

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Travelers",
                             command=lambda: controller.show_frame(Page2))

        button1.place(relx=0.01, rely=0.45, relheight=0.05, relwidth=0.2)
        button2.place(relx=0.01, rely=0.55, relheight=0.05, relwidth=0.2)

        # Treeview
        # building tree view
        tree_frame = tk.Frame(self)
        tree_frame.place(relx=0.01, rely=0.035, relheight=0.4, relwidth=0.98)
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

        # Placing widgets
        my_tree.pack(fill="both")
        tree_scroll.config(command=my_tree.yview)

        # Calls
        functions.filltree(my_tree, "Trip")


# third window frame page2
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


# Driver Code
app = tkinterApp()
app.mainloop()


