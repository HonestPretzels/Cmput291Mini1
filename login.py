import sqlite3
import getpass
import re


def login(database):

    conn = sqlite3.connect('./'+database)
    c = conn.cursor()

    # Get and validate email address
    print("Enter your email to login or create a new account: ")
    username = input()
    valid_email = True if re.match("[^@]+@[^@]+\.[^@]+", username) else False
    while not valid_email:
        username = input("Please enter a valid email of the format 'example@123.ca': ")
        valid_email = True if re.match("[^@]+@[^@]+\.[^@]+", username) else False

    c.execute("SELECT * FROM members WHERE email = :name;", {"name":username})
    rows = c.fetchone()
    found = False

    # Check for email address in entries
    if len(rows) > 0:
        found = True

        # Login if found
        print("Please enter your password: ")
        password = getpass.getpass('')
        c.execute("SELECT pwd FROM members WHERE email = :name;", {"name":username})
        pwd = c.fetchone()
        valid_pwd = True if pwd[0] == password else False
        if valid_pwd:
            print("You are now logged in as: ", username)
        tries = 1

        # Check for correct password
        while (tries < 3 and not valid_pwd):
            print("Incorrect password, please try again: ")
            password = getpass.getpass('')
            c.execute("SELECT pwd FROM members WHERE email = :name;", {"name":username})
            pwd = c.fetchone()
            valid_pwd = True if pwd[0] == password else False
            if pwd == password:
                print("You are now logged in as: ", username)
            else:
                tries += 1

        # End program after 3 incorrect password attempts
        if (tries == 3):
            print("3 incorrect password attempts, please try again later")
            quit()

    # Make a new account if the entry does not exist
    if not found:
        print("To make a new account with the address entered, type \'y\', to quit type \'n\'")
        make_new = input()
        valid_make_new = True if make_new == 'y' or make_new == 'n' else False
        while not valid_make_new:
            print("Please type \'y\' or \'n\'")
            make_new = input()
        if (make_new.lower() == 'y'):

            # Get name
            print("Please enter your name: ")
            name = input()
            valid_name = True
            if name == '' or name == ' ':
                valid_name = False
            elif not re.match('^[A-Za-z0-9_]*$', name):
                valid_name = False
            while not valid_name:
                print("You must enter a valid name.")
                print("Please enter your name: ")
                name = input()
                if name == '' or name == ' ':
                    valid_name = False
                elif not re.match('^[A-Za-z0-9_]*$', name):
                    valid_name = False
                else:
                    valid_name = True
            
            # Get phone number and validate it
            print("Please enter your phone number: ")
            phone = input()
            valid_phone = True
            if phone == '' or phone == ' ':
                    valid_phone = False
            elif not re.match("^[\d0-9]{3}-[\d0-9]{3}-[\d0-9]{4}$", phone):
                valid_phone = False

            while not valid_phone:
                print("You must enter a valid phone number of the format XXX-XXX-XXXX.")
                print("Please enter your phone number: ")
                phone = input()
                if phone == '' or phone == ' ':
                    valid_phone = False
                elif not re.match("^[\d0-9]{3}-[\d0-9]{3}-[\d0-9]{4}$", phone):
                    valid_phone = False
                else:
                    valid_phone = True
                
            # Create a password
            print("Create your password: ")
            pwd = input()
            valid_pwd = True
            if valid_pwd == '' or valid_pwd == ' ':
                valid_pwd = False
            elif (len(pwd) > 6):
                valid_pwd = False
            elif not re.match('^[A-Za-z0-9_]*$', pwd):
                valid_name = False
            while not valid_pwd:
                print("You must enter a valid password.")
                print("Please enter your password: ")
                pwd = input()
                if valid_pwd == '' or valid_pwd == ' ':
                    valid_pwd = False
                elif (len(pwd) > 6):
                    valid_pwd = False
                elif not re.match('^[A-Za-z0-9_]*$', pwd):
                    valid_name = False
                else:
                    valid_pwd = True

            # Add the new entry to the table
            c.execute("INSERT INTO members (email, name, phone, pwd) VALUES (:u_email, :u_name, :u_phone, :u_pwd);", {"u_email":username, "u_name":name, "u_phone":phone, "u_pwd":pwd})
            conn.commit()
            print("You are now logged in as: ", username)
        else:
            quit()


    c.execute("SELECT * FROM inbox WHERE email = :u_name;", {"u_name": username})
    rows = c.fetchall()

    unread_count = 0

    # Display new messages if they exist
    for message in rows:
        if message[5] == 'n':
            unread_count += 1

    if unread_count > 0:
        print("You have ", unread_count, " unread messages: ")
        for message in rows:
            if message[0] == username:
                if message[5] == 'n':
                    print(message)
                    c.execute("UPDATE inbox SET seen = 'y' WHERE content = :content AND email = :u_name;", {"content":message[3], "u_name":username})
                    conn.commit()
    else:
        print("You have no unread messages.")

    conn.close()

    return username
