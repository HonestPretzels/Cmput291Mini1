import sqlite3

def search_requests(username, database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()

    # Get input
    print("Enter a location or location code: ")
    location = input()

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

    if (len(rides) > 0):
        for ride in rides:
            print(ride)
    else:
        print("No matching rides")
        return

    # Send the message
    print("Type a request number to message the posting member: ")
    r_number = input()

    c.execute("SELECT email FROM requests WHERE rid = :number;", {"number":r_number})
    email = c.fetchone()

    rno = input("Which ride number is this regarding? ")
    message = input("Type what you would like to say, press enter to send: ")

    # Commit the message to the DB
    c.execute("INSERT INTO inbox (email, msgTimestamp, sender, content, rno, seen) VALUES (:recip, datetime('now'), :sender, :content, :rno, 'n');", {"recip":email[0], "sender":username, "content":message, "rno":rno})
    conn.commit()