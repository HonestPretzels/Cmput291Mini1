import sqlite3
import datetime

def manage_bookings(controller, username):

	cursor = controller.cursor()

	quit = False



	while not quit:
		print("Manage bookings:")
		print("To view your bookings, please enter 'view bookings'")
		print("To view all of your rides, please enter 'view rides'") 
		print("To book a member on a ride, please enter the ride number") #TODO
		print("To return to the menu, please enter 'menu'")
		rides = cursor.execute("SELECT * FROM rides r WHERE r.driver LIMIT 5 = :u_username", {"u_username":username})

		print("\nPosted Rides (up to 5)")
		for ride in rides:
			print("Rno: %d, Price per Seat: %d, Date: %s, Seats: %d, Luggage Description: %s, Source Lcode: %d: Destination Lcode: %d",(ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6]))
		
		response = input().lower()

		if response == "menu":
			quit = True


#----------------------------------------------------------------------------------------------------------------------------#
#handle view bookings/ cancel bookings
		elif response == "view bookings":
			bookings = cursor.execute("SELECT b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff FROM bookings b, rides r WHERE r.rno = b.rno and r.driver = :u_username ORDER BY r.rno", {"u_username":username})



			for booking in bookings:
				print("Booking No.: %d, Member: %s, Ride No.: %d, Cost Per Seat: %d, No. Of Seats: %d, Pickup Location Code: %d, Dropoff Location Code: %d", (booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], booking[6]))



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

						for booking in bookings:
							if booking[0] == bno:
								match = True

					except ValueError:
						continue

					if match == True:
						booking = cursor.execute("SELECT * FROM bookings WHERE bno = :bno;", {"bno":bno})

						cursor.execute("DELETE FROM bookings WHERE bno = :bno;", {"bno":bno})
						message_string = "Your booking" + str(bno) + "for ride" + booking[1] + "has been cancelled"
						cursor.execute("INSERT INTO inbox VALUES (:email, :msgTimestamp, :sender, :content, :rno, :seen)",{"email":member_data[0], "msgTimestamp":datetime.now(), "sender":username, "content":message_string, "rno":member_data[1], "seen":'n'})
						controller.commit()
						print("booking cancelled")

					else:
						print("Invalid Response, please try again")


#----------------------------------------------------------------------------------------------------------------------------#
#handle view rides
		elif response == 'view rides':
			total_rides = cursor.execute("SELECT * FROM rides r WHERE r.driver = :u_username", {"u_username":username})

			print("Posted rides:")
			for ride in total_rides:
				print("Rno: %d, Price per Seat: %d, Date: %s, Seats: %d, Luggage Description: %s, Source Lcode: %d: Destination Lcode: %d",(ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6]))

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
		 		input("Invalid Response, press any key to continue")

			if valid_rno:

		 		#get member name
				valid_response = False
				while not valid_response:
					email = input("Please enter a member's email: ")

					member_name = cursor.execute("SELECT email FROM members WHERE email = :_email;", {"_email": email})
					#not a good way to do this but tbh, don't know how else to check the values inside a query
					for name in member_name:
						if name[0] == email:
							valid_response = True

				#get cost per seat
				valid_response = False
				while not valid_response:
					cost_per_seat = input("Please enter a cost per seat")

					try:
						cost = int(cost_per_seat)
						valid_response = True

					except ValueError:
						print("Invalid input, please try again")

				#get number of seats
				valid_response = False
				while not valid_response:
					seats = input("Please enter the number of seats: ")

					try:
						int(seats)

						num_seats = tracked_ride[3]
						num_seats -= seats
						bookings = cursor.execute("SELECT seats FROM bookings WHERE rno = :_rno;",{"_rno":tracked_ride[0]})

						for booking in bookings:
							num_seats -= booking[4]

						if num_seats < 0:
							get_response = input("You have overbooked your ride, if you're sure you want to do this enter 'yes' otherwise, enter anything to try again: ").lower()
							if get_response == "yes":
								valid_response = True
						else:
							valid_response = True

					except ValueError:
						print("Invalid input, please try again")

				#get picikup
				locations = cursor.execute("SELECT lcode FROM locations;")
				valid_response = False
				while not valid_response:
					pickup = input("Please enter a pickup location lcode: ")
					try:
						pickup_lcode = int(pickup)

						for lcode in locations:
							if pickup_lcode == lcode[0]:
								valid_response = True
								break
					except ValueError:
						print("Invalid input, please try again")

				#get dropoff
				valid_response = False
				while not valid_response:
					dropoff = input("Please enter a dropoff location lcode: ")
					try:
						dropoff_lcode = int(dropoff)

						for lcode in locations:
							if dropoff_lcode == lcode[0]:
								valid_response = True
								break
					except ValueError:
						print("Invalid input, please try again")

				#generate bno
				bno = 0
				bookings = cursor.execute("SELECT bno FROM bookings;")
				for booking in bookings:
					if booking[0] > bno:
						bno = booking[0]
				bno += 1
				cursor.execute("INSERT INTO bookings VALUES :_bno, :_email, :_rno, :_cost, :_seats, :_pickup, :_dropoff;",{"_bno":bno, "_email":email, "_rno":rno, "_cost":cost, "_seats":seats, "_pickup":pickup_lcode, "_dropoff":dropoff_lcode})
				controller.commit()
				input("Booking added, press enter to return")

#----------------------------------------------------------------------------------------------------------------------------#
			#No valid response
			else:
				input("Invalid response, press enter to continue")














conn = sqlite3.connect('./proj.db')
manage_bookings(conn, "test_user")