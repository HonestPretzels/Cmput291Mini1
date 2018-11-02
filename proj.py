import sqlite3
import getpass

conn = sqlite3.connect('./proj.db')
c = conn.cursor()


print("Enter your email to login or create a new account: ")
username = input()

c.execute("SELECT * FROM members;")
rows = c.fetchall()
found = False

for entry in rows:
    if entry[0] == username:
        found = True
        print("Please enter your password: ")
        # password = input()
        password = getpass.getpass('')
        if entry[3] == password:
            print("You are now logged in as: ", username)
        break

if not found:
    print("To make a new account with the address entered, type \'y\', to quit type \'n\'")
    make_new = input()
    print(make_new)
    # while not make_new != "y" or make_new != "n":
    #     print("Please type \'y\' or \'n\'")
    #     make_new = input()
    if (make_new == 'y'):
        print("Please enter your name: ")
        name = input()
        while (name == ''):
            print("You must enter a valid name.")
            print("Please enter your name: ")
            name = input()
        print("Please enter your phone number: ")
        phone = input()
        while (phone == ''):
            print("You must enter a valid phone number.")
            print("Please enter your phon number: ")
            phone = input()
        print("Create your password: ")
        pwd = input()
        while (pwd == ''):
            print("You must enter a valid password.")
            print("Please enter your password: ")
            pwd = input()

        c.execute("INSERT INTO members (email, name, phone, pwd) VALUES (:u_email, :u_name, :u_phone, :u_pwd);", {"u_email":username, "u_name":name, "u_phone":phone, "u_pwd":pwd})
        conn.commit()
        print("You are now logged in as: ", username)
    else:
        quit()


c.execute("SELECT * FROM inbox WHERE email = :u_name;", {"u_name": username})
rows = c.fetchall()

unread_count = 0

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
else:
    print("You have no unread messages.")


print("Menu: \n")
print("Please type one of the following words to perform an action: \n")
print("To offer a ride, type \'offer\'")
print("To search for a ride, type \'search\'")
print("To book members or cancel a booking, type \'bookings\'")
print("To post a ride request, type \'post\'")
print("To search or delete your requests, type \'requests\'")

# typing any of the words above will route to the appropriate function


conn.close()