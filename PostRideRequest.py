import sqlite3
import re #regular expressions
import datetime #for checking valid dates



def PostRideRequest(controller, username):

	print("Posting Ride\n")

	cursor = controller.cursor()

	valid_date = False
	date_format = re.compile('\d\d\d\d-\d\d-\d\d')

	while not valid_date:
		date = input("Please provide a date (YYYY-MM-DD): ")

		if date_format.match(date) is not None:
			year,month,day = date.split('-')

			valid_date = True
			try:
				datetime.datetime(int(year), int(month), int(day))
			except ValueError:
				valid_date = False

		if not valid_date:
			print("Invalid date, please use format (YYYY-MM-DD)")		


	valid_location = False
	locations = c.execute("SELECT lcode FROM locations;")


	while not valid_location:
		pick_up_code = input("Please provide a pickup location code: ")

		#This section will be uncommented once we've established a database
		# for lcode in locations:
		# 	if lcode[0] == pick_up_code:
		# 		valid_location = True

		# if not valid_location:
		# 	print("Location does not exist, please enter a valid location")

		valid_location = True #remove when uncommenting above


	valid_location = False

	while not valid_location:
		drop_off_code = input("Please provide a dropoff location code: ")

		#This section will be uncommented once we've established a database
		# for lcode in locations:
		# 	if lcode[0] == drop_off_code:
		# 		valid_location = True

		# if not valid_location:
		# 	print("Location does not exist, please enter a valid location")

		valid_location = True #remove when uncommenting above

	valid_price = False

	while not valid_price:
		amount = input("Please provide the amount you are willing to pay per seat: ")

		valid_price = True
		try:
			price = int(amount)
			if price <= 0:
				valid_price = False
		except ValueError:
			valid_price = False

		if not valid_price:
			print("Invalid price, please enter an integer")

	print(date, int(pick_up_code), int(drop_off_code), price)

	valid_rid = False
	highest_rid = 0

	existing_rids = c.execute("SELECT rid FROM requests")

	for temp_rid in existing_rids:
		if temp_rid[0] > highest_rid:
			highest_rid = temp_rid[0]

	rid = highest_rid + 1

	cursor.execute("INSERT INTO requests (rid, email, rdate, pickup, dropoff, amount) VALUES (:r_rid, :u_email, :r_rdate, :r_pickup, :r_dropoff, :r_amount)", {"r_rid":rid, "u_email":username, "r_rdate":date, "r_pickup":int(pick_up_code), "r_dropoff":int(drop_off_code), "r_amount": price})
	controller.commit()

#for testing purposes only
conn = sqlite3.connect('./proj.db')
c = conn.cursor()

PostRideRequest(conn, "ltyue@ualberta.ca")

requests = c.execute("SELECT * FROM requests")
for request in requests:
	print(request)