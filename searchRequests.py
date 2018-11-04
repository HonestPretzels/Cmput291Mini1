import sqlite3
import re

def search_requests(username, database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()

    # Get input
    location = input("Enter a location or location code: ")

    # Validate input
    valid_location = re.match('^[A-Za-z0-9_]*$', location)
    while (not valid_location):
        location = input("Please enter a valid location or location code: ")
        valid_location = re.match('^[A-Za-z0-9_]*$', location)


    # Find the rides
    if len(location) > 5:
        c.execute("SELECT rid, email, rdate, pickup, dropoff, amount FROM requests r, locations l WHERE pickup = lcode AND city = :loc COLLATE NOCASE;", {"loc":location})
        rides = c.fetchmany(5)

    else:
        c.execute("SELECT * FROM requests WHERE pickup = :loc COLLATE NOCASE;", {"loc":location})
        rides = c.fetchmany(5)
    if (len(rides) == 0):
            print("No matching rides")
            return
    
    while (len(rides) > 0):
        for ride in rides:
            print(ride)

        choice = input("To see more requests, press enter. Type 'm' to message a posting member: ")

        if (choice.lower() == 'm'):
            # Send the message
            r_number = input("Type a request number to message the posting member: ")
            valid_number = re.match('^[A-Za-z0-9_]*$', r_number)

            # Validate the input
            valid_number = int(r_number)
            while not valid_number:
                r_number = input("Please enter a valid number: ")
                valid_number = re.match('^[A-Za-z0-9_]*$', r_number)
                valid_number = int(r_number)


            c.execute("SELECT email FROM requests WHERE rid = :number;", {"number":r_number})
            email = c.fetchone()

            rno = input("Which ride number is this regarding? ")

            # Validate the input
            valid_no = re.match('^[A-Za-z0-9_]*$', rno)
            valid_no = int(r_number)
            while not valid_no:
                rno = input("Please enter a valid number: ")
                valid_no = re.match('^[A-Za-z0-9_]*$', rno)
                valid_no = int(r_number)

            message = input("Type what you would like to say, press enter to send: ")

            # Validate the input
            valid_message = re.match('^[A-Za-z0-9_]*$', message)
            while not valid_number:
                message = input("Please enter a valid message: ")
                valid_message = re.match('^[A-Za-z0-9_]*$', message)

            # Commit the message to the DB
            c.execute("INSERT INTO inbox (email, msgTimestamp, sender, content, rno, seen) VALUES (:recip, datetime('now'), :sender, :content, :rno, 'n');", {"recip":email[0], "sender":username, "content":message, "rno":rno})
            return
        else:
            rides = c.fetchmany(5)

    print("There are no more locations to view")

    conn.commit()