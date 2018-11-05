import sqlite3
import re

def delete_request(username, database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()

    # Select the rides
    c.execute("SELECT * FROM requests WHERE email = :u_name;", { "u_name":username })
    rides = c.fetchall()

    if rides:
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

        # Make sure the user owns the selected request
        c.execute("SELECT email FROM requests WHERE rid = :r_no;", { "r_no":r_number})
        name = c.fetchone()
        valid_name = True

        if not name:
            print("That request does not exist.")
            valid_name = False
        elif (name[0] != username):
            print("You do not own this request. Please select a request that you have made to delete it.")
            valid_name = False


        while not valid_name:
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

            # Make sure the user owns the selected request
            c.execute("SELECT email FROM requests WHERE rid = :r_no;", { "r_no":r_number})
            name = c.fetchone()

            if not name:
                print("That request does not exist.")
                valid_name = False
            elif (name[0] != username):
                print("You do not own this request. Please select a request that you have made to delete it.")
                valid_name = False
            else:
                valid_name = True

        # Delete request
        c.execute("DELETE FROM requests WHERE rid = :r_no;", { "r_no":r_number})
        conn.commit()
        print("Request number " + r_number + " has been deleted")
    else:
        print("No requests to show!")

    conn.close()
    return