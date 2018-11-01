import sqlite3

conn = sqlite3.connect('./proj.db')
c = conn.cursor()


print("Enter your email to login or create a new account: ")
username = input()

c.execute("SELECT * FROM members;")
rows = c.fetchall()

for entry in rows:
    if entry["email"].upper() == username.upper():
        print("Please enter your password: ")
        password = input()
        if entry["pwd"] == password:
            print("Login successful")
        break

# create new account info goes in here

conn.close()