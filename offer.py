import sqlite3
import re
conn = sqlite3.connect('./proj.db')
c = conn.cursor()

def offer(current_user_email):
    

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
    add_car = input('Would you like to add a car to this ride y/n? ').lower()
    while(add_car != 'n' and add_car != 'y'):
        add_car = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to add a car to this ride? ')
    car, car_found = choose_car(add_car,current_user_email)

    #CREATE RNO AND INSERT
    c.execute('SELECT rno FROM rides ORDER BY rno desc LIMIT 1')
    rno = c.fetchone()[0] + 1
    if (car_found):
        c.execute('INSERT INTO rides VALUES (:rno, :price, :rdate, :seats, :lugDesc, :src, :dst, :driver, :cno);', {"rno":rno, "price":seat_price, "rdate":date, "seats":num_seats, "lugDesc":luggage_description, "src":source, "dst":destination, "driver":current_user_email, "cno":car})
        print('Added a ride: %s, %s, %s, %s, %s, %s, %s, %s, %s'%(rno,seat_price,date,num_seats,luggage_description,source,destination,current_user_email,car))
    else:
        c.execute('INSERT INTO rides VALUES (:rno, :price, :rdate, :seats, :lugDesc, :src, :dst, :driver, :cno);', {"rno":rno, "price":seat_price, "rdate":date, "seats":num_seats, "lugDesc":luggage_description, "src":source, "dst":destination, "driver":current_user_email, "cno":None})
        print('Added a ride: %s, %s, %s, %s, %s, %s, %s, %s'%(rno,seat_price,date,num_seats,luggage_description,source,destination,current_user_email))

    #ENROUTE
    add_enroute = input('Would you like to add an enroute destination to this ride y/n? ').lower()
    while(add_enroute != 'n'):
        if(add_enroute != 'y'):
            add_enroute = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to add an enroute destination to this ride? ')
        else:
            enroute_keyword = input('Please enter a location keyword: ')
            enroute_valid = re.match('^[A-Za-z0-9_]*$',enroute_keyword)
            while(not enroute_valid):
                enroute_keyword = input('Location keyword not valid. Please enter another location: ')
                enroute_valid = re.match('^[A-Za-z0-9_]*$',enroute_keyword)
            enroute, enroute_found = choose_location(enroute_keyword)
            if(enroute_found):
                c.execute("INSERT INTO enroute VALUES (:rno, :lcode)", {"rno":rno, ":lcode":enroute})
                print('Enroute location: %s added to ride: %s'%(enroute,rno))
            add_enroute = input("Would you like to add another enroute location y/n? ")
    return


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

def choose_car(add_car,current_user_email):
    # Helper function to allow the user to choose a car

    if(add_car == 'y'):
        car = input('Please enter the car number: ')
        car_valid = re.match('^[0-9]*$', car)
        while (not car_valid):
            car = input('Car number invalid. Please enter the car number: ')
            car_valid = re.match('^[0-9]*$', car)  
        c.execute('SELECT cno FROM cars WHERE owner == ?', current_user_email)
        owned_cars = c.fetchall()
        if(not car in owned_cars):
            add_car = input('You do not own that car. Would you like to add a different car to the ride y/n? ').lower()
            while(add_car != 'n' and add_car != 'y'):
                add_car = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to add a different car to this ride? ')
            if(add_car == 'n'):
                return '', False
            else:
                return choose_car(add_car, current_user_email)
        else:
            return car, True
    else:
        return '', False