import sqlite3

def delete_request(username, database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()

    # Select the rides
    c.execute("SELECT * FROM requests WHERE email = :u_name;", { "u_name":username })
    rides = c.fetchall()

    try:
        for ride in rides:
            print(ride)

        r_number = input("Please enter the id of the request you would like to delete or 'q' to quit: ")

        # Validate input
        valid_number = re.match('^[A-Za-z0-9_]*$', r_number)
        while (not valid_number):
            print("Please enter a valid id or 'q' to quit: ")
            r_number = input()
            valid_number = re.match('^[A-Za-z0-9_]*$', r_number)

        # End this function
        if (r_number == 'q'):
            return

        # Delete request
        c.execute("DELETE FROM requests WHERE rid = :r_no;", { "r_no":r_number})
        conn.commit()
    except:
        print("No requests to show!")

    conn.close()
    return