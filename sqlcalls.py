import sqlite3

#This is where sql database is made if !exists, will run first in the main run

def setupDB():
    conn = sqlite3.connect('tplanner.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Traveler" (
            Traveler_ID INTEGER NOT NULL,
            Name        VARCHAR(100) NOT NULL,
            Age         INTEGER NOT NULL,
            Gender	    VARCHAR(50) NOT NULL,
            Address	    VARCHAR(255) NOT NULL,
            PRIMARY KEY(Traveler_ID)
        );
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS "Trip" (
                Trip_ID		        INTEGER NOT NULL,
                Trip_Name		    VARCHAR(50) NOT NULL,
                Start_date  		DATE NOT NULL,
                End_date		    DATE NOT NULL,
                Duration		    VARCHAR,
                Notes			    TEXT,
                Total_expenditure	DECIMAL(18,2),
                PRIMARY KEY(Trip_ID)
            );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Itinerary" (
            Itinerary_ID	 INTEGER NOT NULL,
            Itinerary_Name  VARCHAR(50) NOT NULL,
            Description 	 VARCHAR(255),
            Trip_ID	      INTEGER NOT NULL,
            PRIMARY KEY(Itinerary_ID)
            FOREIGN KEY(Trip_ID) REFERENCES Trip(Trip_ID)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Events" (
            Events_ID    	INTEGER NOT NULL,
            Name            VARCHAR NOT NULL,
            Location	    VARCHAR(100) NOT NULL,
            Start_DandT	    DATETIME NOT NULL,
            End_DandT 	    DATETIME NOT NULL,
            Type		    VARCHAR(50) NOT NULL,
            Notes		    TEXT,
            Expenses	    DECIMAL(18,2),
            Itinerary_ID	INTEGER NOT NULL,
            PRIMARY KEY(Events_ID)
            FOREIGN KEY("Itinerary_ID") REFERENCES Itinerary(Itinerary_ID)
        );
     """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Trip_Destination" (
            TripD_ID        INTEGER NOT NULL,
            Destination	    VARCHAR(100) NOT NULL,
            Trip_ID	        INTEGER NOT NULL,
            FOREIGN KEY(Trip_ID) REFERENCES Trip(Trip_ID)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Traveler_Trip" (
            TravTrip_ID	INTEGER NOT NULL,
            Traveler_ID	INTEGER NOT NULL,
            Trip_ID 	INTEGER NOT NULL,
            PRIMARY KEY(TravTrip_ID)
            FOREIGN KEY(Traveler_ID) REFERENCES Traveler(Traveler_ID)
            FOREIGN KEY(Trip_ID) REFERENCES Trip(Trip_ID)
            );
    """)
    conn.close()
    return 0