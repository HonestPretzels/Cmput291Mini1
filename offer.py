import sqlite3
import re
conn = sqlite3.connect('./proj.db')
c = conn.cursor()

def offer():
    

    # DATE
    date = input('Please enter the date of the ride in YYYY-MM-DD format: ')
    date_valid = re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$',date)
    while (not date_valid):
        date = input('Date invalid. Please enter the date of the ride in YYYY-MM-DD format: ')
        date_valid = re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$',date)

    #NUMBER OF SEATS
    num_seats = input('Please enter the number of seats: ')
    seats_valid = re.match('^[0-9]*$',num_seats)
    while (not seats_valid):
        num_seats = input('Number of seats not valid. Please enter the number of seats: ')
        seats_valid = re.match('^[0-9]*$',num_seats)

    #PRICE
    seat_price = input('Please enter the price per seat: ')
    price_valid = re.match('^[0-9]*$',seat_price)
    while (not price_valid):
        seat_price = input('Price per seat not valid. Please enter the price per seat: ')
        price_valid = re.match('^[0-9]*$',seat_price)

    #LUGGAGE DESCRPITION
    luggage_description = input('Please enter the luggage description: ')
    luggage_valid = (re.match('^[A-Za-z0-9_]*$',luggage_description) and len(luggage_description)<=10)
    while (not luggage_valid):
        luggage_description = input('Luggage description not valid. Please enter the luggage description: ')
        luggage_valid = (re.match('^[A-Za-z0-9_]*$',luggage_description) and len(luggage_description)<=10)

    #SOURCE LOCATION
    source = input('Please enter the source location: ')
    source_valid = re.match('^[A-Za-z0-9_]*$',source)
    while(not source_valid):
        source = input('Source not valid. Please enter the source location: ')
        source_valid = re.match('^[A-Za-z0-9_]*$',source)
    source, source_valid = choose_location(source)
    if (not source_valid):
        print('Failed to find a source location. Ride offer aborted')
        return

    #DESTINATION LOCATION
    destination = input('Please enter the destination location: ')
    destination_valid = re.match('^[A-Za-z0-9_]*$',destination)
    while(not destination_valid):
        destination = input('Destination not valid. Please enter the destination location: ')
        destination_valid = re.match('^[A-Za-z0-9_]*$',destination)
    destination, destination_valid = choose_location(destination)
    if (not destination):
        print('Failed to find a source location. Ride offer aborted')
        return

    #CAR
    ################ ADD CAR FUNCTIONALITY #################

    #ENROUTE
    ################ ADD EN ROUTE FUNCTIONALITY ############

    #INSERT
    ################ INSERT INTO RIDES TABLE ###############




def choose_location(location_keyword):
    # Takes a keyword argument and allows the user to choose a location which matches that keyword

    choices_found = False
    if (len(location_keyword)==5):      # Lcode case
        c.execute('SELECT lcode FROM locations WHERE lcode = ?', (location_keyword))
        choice = c.fetchone()
    if (choice != None):
        choices_found = True
        return choice[0], choices_found
    
    else:                               # Keyword case
        c.execute("SELECT lcode, address, city, prov FROM locations WHERE address LIKE '%?%' OR prov LIKE '%?' or city LIKE '%?%'", (location_keyword,location_keyword,location_keyword))
        options = c.fetchmany(5)
        while (len(options)>0): # All through the options
            for option in options:
                print(option)
            response = input('If any of these locations are what you are looking for enter the lcode of that location. Else press enter to see more results. ')
            if (re.match('^[A-Za-z0-9_]{5}$',response)):
                return response, True
            else:
                options = c.fetchmany(5)  
        print('No more locations left')
        choices_found = False
        return '', choices_found