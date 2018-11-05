import sqlite3
import re

def manage_bookings(controller, username):

	cursor = controller.cursor()

	quit = False

# re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$',date)


	while not quit:
		print("Manage bookings:")
		print("To view your bookings, please enter 'view bookings'")
		print("To view your rides, please enter 'view rides'") 
		print("To book a member on a ride, please enter the ride number")
		print("To return to the menu, please enter 'menu'")


		response = input().lower()

		# scrub_check = re.match('[A-Za-z0-9_]$', response)

		# if not scrub_check:
		# 	print("Invalid characters used, returning to menu")
		# 	break

		if response == "menu":
			quit = True


#----------------------------------------------------------------------------------------------------------------------------#
#handle view bookings/ cancel bookings
		elif response == "view bookings":
			bookings = cursor.execute("SELECT b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff FROM bookings b, rides r WHERE r.rno = b.rno and r.driver = :u_username ORDER BY r.rno", {"u_username":username})


			print("Bookings:")
			for booking in bookings:
				#print("Booking No.: %d, Member: %s, Ride No.: %d, Cost Per Seat: %d, No. Of Seats: %d, Pickup Location Code: %d, Dropoff Location Code: %d", (booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], booking[6]))
				print(booking)


			do_return = False
			while not do_return:
				print("To cancel a booking, please enter the booking number")
				print("Otherwise, enter 'return'")
				get_response = input().lower()

				if get_response == "return":
					do_return = True
					print("returning")

				else:

					match = False
					try:
						bno = int(get_response)
						bookings = cursor.execute("SELECT b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff FROM bookings b, rides r WHERE r.rno = b.rno and r.driver = :u_username ORDER BY r.rno", {"u_username":username})
						for booking in bookings:
							#print(booking[0])
							if int(booking[0]) == bno:
								match = True

					except ValueError:
						#print("NAN")
						continue

					if match == True:
						booking = cursor.execute("SELECT * FROM bookings WHERE bno = :_bno;", {"_bno":bno}).fetchone()
						# booking = value.fetchone()[0]

						date = cursor.execute("SELECT datetime('now')")
						datetime = cursor.fetchone()[0]
						#member_data = cursor.execute("SELECT * FROM members WHERE email = :_email",{"_email":booking[7]}).fetchone()[0]
						cursor.execute("DELETE FROM bookings WHERE bno = :_bno;", {"_bno":bno})
						message_string = "Your booking " + str(bno) + " for ride " + str(booking[2]) + " has been cancelled"
						cursor.execute("INSERT INTO inbox VALUES (:_email, :_msgTimestamp, :_sender, :_content, :_rno, :_seen)",{"_email":booking[1], "_msgTimestamp":datetime, "_sender":username, "_content":message_string, "_rno":booking[2], "_seen":'n'})
						controller.commit()
						print("booking cancelled")

					else:
						print("Invalid Response, please try again")


#----------------------------------------------------------------------------------------------------------------------------#
#handle view rides
		elif response == 'view rides':
			rides = cursor.execute("SELECT r.rno, r.price, r.rdate, r.seats, r.lugdesc, r.src, r.dst, r.seats - SUM(b.seats) FROM rides r, bookings b WHERE r.rno = b.rno and r.driver = :_username GROUP BY r.rno UNION SELECT r.rno, r.price, r.rdate, r.seats, r.lugdesc, r.src, r.dst, r.seats FROM rides r WHERE r.driver = :_username EXCEPT SELECT r.rno, r.price, r.rdate, r.seats, r.lugdesc, r.src, r.dst, r.seats FROM rides r, bookings b WHERE r.rno = b.rno;",{"_username":username})

			

			not_return = False
			loop = 1
			
			#Print list of rides
			while  not not_return:
				print("Posted rides:")
				ride_list = rides.fetchmany(5)
				for ride in ride_list:
					print(ride)
				if len(ride_list) < 5:
					print("End of list")
					not_return = True
				
				if not not_return:
					more_rides = input("To view more rides, press enter. Otherwise enter 'quit'").lower()
					if more_rides == "quit":
						not_return = True

			input("Press enter to return to menu")


#----------------------------------------------------------------------------------------------------------------------------#
#handle book member
#as a note, I think it's stupid to be able to book anyone on your rides but w/e... HOP ON MR. BONES' WILD RIDE!
		else:
			valid_rno = False


			try: 
		 		rno = int(response)
	 			total_rides = cursor.execute("SELECT * FROM rides r WHERE r.driver = :u_username;", {"u_username":username})
	 			for ride in total_rides:
	 				if rno == ride[0]:
	 					tracked_ride = ride
	 					valid_rno = True
	 					break

			except ValueError:
		 		input("Invalid Response, press enter to continue")

			if valid_rno:

		 		#get member name
				valid_response = False
				while not valid_response:
					email = input("Please enter a member's email: ")
					valid_email = True if re.match("[^@]+@[^@]+\.[^@]+", username) else False
					while not valid_email:
						username = input("Please enter a valid email of the format 'example@123.ca': ")
						valid_email = True if re.match("[^@]+@[^@]+\.[^@]+", username) else False

					member_name = cursor.execute("SELECT email FROM members WHERE email = :_email;", {"_email": email}).fetchone()

					if member_name is not None:
						valid_response = True

				#get cost per seat
				valid_response = False
				while not valid_response:
					cost_per_seat = input("Please enter a cost per seat: ")

					try:
						cost = int(cost_per_seat)
						if cost >= 0:
							valid_response = True

					except ValueError:
						print("Invalid input, please try again")

				#get number of seats
				valid_response = False
				while not valid_response:
					seats = input("Please enter the number of seats: ")

					try:
						seats = int(seats)

						num_seats = int(tracked_ride[3])
						#print(num_seats)
						num_seats -= seats
						bookings = cursor.execute("SELECT seats FROM bookings WHERE rno = :_rno;",{"_rno":tracked_ride[0]})

						for booking in bookings:
							#print(booking)
							num_seats -= booking[0]

						if num_seats < 0:
							get_response = input("You have overbooked your ride, if you're sure you want to do this enter 'yes' otherwise, enter anything to try again: ").lower()
							if get_response == "yes":
								valid_response = True
						else:
							valid_response = True

					except ValueError:
						print("Invalid input, please try again")

				#need to alter slightly: lcodes can be characters should be a quick fix
				#get picikup
				locations = cursor.execute("SELECT lcode FROM locations;")
				valid_response = False
				while not valid_response:
					pickup = input("Please enter a pickup location lcode: ")

					
					lcode_match = False
					for lcode in locations:
						if pickup.lower() == lcode[0].lower():
							valid_response = True
							lcode_match = True
							break

					if not lcode_match:
						print("Not a valid location, please try again")

				#get dropoff
				locations = cursor.execute("SELECT lcode FROM locations;")
				valid_response = False
				while not valid_response:
					dropoff = input("Please enter a dropoff location lcode: ")

					lcode_match = False
					for lcode in locations:
						if dropoff.lower() == lcode[0].lower():
							valid_response = True
							lcode_match = True
							break

					if not lcode_match:
						print("Not a valid location, please try again")

				#generate bno
				bno = 0
				bookings = cursor.execute("SELECT bno FROM bookings;")
				for booking in bookings:
					if booking[0] > bno:
						bno = booking[0]
				bno += 1
				date = cursor.execute("SELECT datetime('now')")
				datetime = cursor.fetchone()[0]


				cursor.execute("INSERT INTO bookings VALUES (:_bno, :_email, :_rno, :_cost, :_seats, :_pickup, :_dropoff);",{"_bno":bno, "_email":email, "_rno":rno, "_cost":cost, "_seats":seats, "_pickup":pickup, "_dropoff":dropoff})
				message_string = "You have been booked on ride " + str(rno) + " from " + pickup + " to " + dropoff
				cursor.execute("INSERT INTO inbox values (:_email, :_time, :_sender, :_content, :_rno, :_seen);",{"_email":email, "_time":datetime,"_sender":username,"_content":message_string, "_rno":rno, "_seen":'n'})
				controller.commit()
				input("Booking added, press enter to return")

#----------------------------------------------------------------------------------------------------------------------------#
#testing function

# conn = sqlite3.connect('./proj.db')
# manage_bookings(conn, "tom.maurer@yahoo.com")

# conn.close()