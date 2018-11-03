import sqlite3

def manage_bookings(conn, username):

	cursor = conn.cursor()

	quit = False

	print("Manage bookings:")
	print("To view your bookings, please enter 'view bookings'")
	print("To view your rides, please enter 'view rides'") #the description could be interpreted as print 5 rides on startup
	print("To cancel a booking, please enter 'cancel booking'")
	print("To book a member on a ride, please enter 'book member'")
	print("To return to the menu, please enter 'menu'")

	while not quit:

		
		response = input().lower()

		if response == "menu":
			quit = True

		elif response == "view bookings":
			bookings = cursor.execute("SELECT b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff FROM bookings b, rides r WHERE r.rno = b.rno and r.driver = :u_username ORDER BY r.rno", {"u_username":username})

			for booking in bookings:
				print(booking)

		elif response == 'view rides':
			rides = cursor.execute("SELECT * FROM rides r WHERE r.driver LIMIT 5 = :u_username", {"u_username":username})
			total_rides = cursor.execute("SELECT * FROM rides r WHERE r.driver = :u_username", {"u_username":username})

			print("Posted rides:")

			for ride in rides:
				print(ride)

			#temporary ui until I can consult team members on whether or not rides should be posted at runtime
			more = input("To view more rides, please enter 'more'\nOtherwise, enter anything else\n").lower()

			if more == "more":
				for ride in total_rides:
					print(ride)














conn = sqlite3.connect('./proj.db')
manage_bookings(conn, "test_user")