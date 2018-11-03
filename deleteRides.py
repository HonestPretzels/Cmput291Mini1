import sqlite3

def delete_ride(username):
    conn = sqlite3.connect('./proj.db')
    c = conn.cursor()

    c.execute("SELECT * FROM rides WHERE driver = :u_name;", { "u_name":username })
    rides = c.fetchall

    try:
        for ride in rides:
            print(ride)

            print("Please enter the number of the ride you would like to delete or 'q' to quit: ")
            r_number = input()

            if (r_number == 'q'):
                return

            c.execute("DELETE FROM rides WHERE rno = :r_no;", { "r_no":r_number})
    except:
        print("No rides to show!")

    conn.close()
    return