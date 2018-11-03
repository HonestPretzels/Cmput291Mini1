import sqlite3

def delete_ride(username):
    conn = sqlite3.connect('./proj.db')
    c = conn.cursor()

    c.execute("SELECT * FROM requests WHERE email = :u_name;", { "u_name":username })
    rides = c.fetchall

    try:
        for ride in rides:
            print(ride)

            print("Please enter the id of the request you would like to delete or 'q' to quit: ")
            r_number = input()

            if (r_number == 'q'):
                return

            c.execute("DELETE FROM requests WHERE rid = :r_no;", { "r_no":r_number})
    except:
        print("No requests to show!")

    conn.close()
    return