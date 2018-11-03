import sqlite3
import datetime

def manage_bookings(controller, username):

	cursor = controller.cursor()

	quit = False

	print("Manage bookings:")
	print("To view your bookings, please enter 'view bookings'")
	print("To view your rides, please enter 'view rides'") #the description could be interpreted as print 5 rides on startup #TODO list # of seats available for each ride
	print("To cancel a booking, please enter 'cancel booking'") #TODO
	print("To book a member on a ride, please enter 'book member'") #TODO
	print("To return to the menu, please enter 'menu'") #TODO

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

		elif response == "cancel booking":
			sbno = input("please enter the bno of the booking you want to cancel: ")

			valid_bno = False
			while not valid_bno:
				try: 
					bno = int(sbno)
					
					bookings = cursor.execute("SELECT b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff FROM bookings b, rides r WHERE r.rno = b.rno and r.driver = :u_username ORDER BY r.rno", {"u_username":username})

					for booking in bookings:
						if booking[0] == bno:
							valid_bno = True
						else:
							print("Invalid bno")
				except TypeError:
					print("Invalid bno")

				valid_bno = True #test line until database established

			member_data = cursor.execute("SELECT email, rno FROM bookings WHERE bno = :u_bno", {"u_bno":bno})

			message_string = "Your booking" + str(bno) + "for ride" + str(member_data[1]) + "has been cancelled"
			cursor.execute("INSERT INTO inbox VALUES (:email, :msgTimestamp, :sender, :content, :rno, :seen)",{"email":member_data[0], "msgTimestamp":datetime.now(), "sender":username, "content":message_string, "rno":member_data[1], "seen":'n'})
			controller.commit()
			print("booking cancelled")
















conn = sqlite3.connect('./proj.db')
manage_bookings(conn, "test_user")