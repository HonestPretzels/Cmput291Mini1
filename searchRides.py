import sqlite3

def search_rides1(username, database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()

    print("Enter a location or location code: ")
    location = input()

    if len(location) > 3:
        c.execute("SELECT rid, email, rdate, pickup, dropoff, amount FROM requests r, locations l WHERE pickup = lcode AND city = :loc COLLATE NOCASE LIMIT 5;", {"loc":location})
        rides = c.fetchall()

    else:
        c.execute("SELECT * FROM requests WHERE pickup = :loc LIMIT 5;", {"loc":location})
        rides = c.fetchall()

    if (len(rides) > 0):
        for ride in rides:
            print(ride)
    else:
        print("No matching rides")
        return

    print("Type a request number to message the posting member: ")
    r_number = input()

    c.execute("SELECT email FROM requests WHERE rid = :number;", {"number":r_number})
    ride = c.fetchall

    rno = input("Which ride number is this regarding? ")
    message = input("Type what you would like to say, press enter to send: ")

    c.execute("INSERT INTO inbox (email, msgTimestamp, sender, content, rno, seen) VALUES (:recip, datetime('now'), :sender, :content, :rno, 'n');", {"recip":ride[1], "sender":username, "content":message, "rno":rno})
    conn.commit()