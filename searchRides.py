import sqlite3

def search_rides(username):
    conn = sqlite3.connect('./proj.db')
    c = conn.cursor()

    print("Enter a location or location code: ")
    location = input()

    if len(location) > 3:
        c.execute("SELECT * FROM requests r, locations l WHERE pickup = lcode AND city = :loc COLLATE NOCASE LIMIT 5;", {"loc":location})
        rides = c.fetchall

    else:
        c.execute("SELECT * FROM requests WHERE pickup = :loc LIMIT 5;", {"loc":location})
        rides = c.fetchall

    print(rides)

    print("Type a request number to message the posting member: ")
    r_number = input()

    c.execute("SELECT email FROM requests WHERE rid = :number;", {"number":r_number})
    ride = c.fetchall

    print("Type what you would like to say, press enter to send: ")
    message = input()

    c.execute("INSERT INTO inbox (email, msgTimestamp, sender, content, rno, seen) VALUES (:recip, datetime('now'), :sender, :content, :rno, 'n');", {"recip":ride[1], "sender":username, "content":message, "rno":r_number })
    conn.commit()