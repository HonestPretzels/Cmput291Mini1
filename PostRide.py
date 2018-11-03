import sqlite3
import re #regular expressions



def PostOffer(cursor, username):

	print("Posting Ride\n")

	valid_date = False
	date_format = re.compile('\d\d\d\d-\d\d-\d\d')
	while not valid_date:
		date = input("Please provide a date (YYYY-MM-DD): ")
		if r.match(date) is not None:
			valid_date = True

	pick_up_code = input("Please provide a pickup location code: ")
	drop_off_code = input("Please provide a dropoff location code: ")
	amount = input("Please provide the amount you are willing to pay per seat: ")

	print(date, pick_up_code, drop_off_code, amount)

	#c.execute("INSERT INTO requests (rid, email, rdate, pickup, dropoff, amount) values (:r_rid, :u_email, :r_rdate, :r_pickup, :r_dropoff, :r_amount)", {"r_rid":tbd, "u_email":username, "r_rdate":date, "r_pickup": pickUpCode, "r_dropoff":dropOffCode, "r_amount": amount})



conn = sqlite3.connect('./proj.db')
c = conn.cursor()

PostOffer(c, "ltyue@ualberta.ca")