from login import login
from deleteRides import delete_ride
from searchRides import search_rides


username = login()

print("Menu: \n")
print("Please type one of the following words to perform an action: \n")
print("To offer a ride, type \'offer\'")
print("To search for a ride, type \'search\'")
print("To book members or cancel a booking, type \'bookings\'")
print("To post a ride request, type \'post\'")
print("To delete your requests, type \'delete\'")
print("To search for a request, type \'search\'")

# typing any of the words above will route to the appropriate function

search_rides(username)