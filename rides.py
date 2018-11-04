import sqlite3
import re


def offer_ride(current_user_email,database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()    

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
    source, source_valid = choose_location(source,database)
    if (not source_valid):
        print('Failed to find a source location. Ride offer aborted')
        return

    #DESTINATION LOCATION
    destination = input('Please enter the destination location: ')
    destination_valid = re.match('^[A-Za-z0-9_]*$',destination)
    while(not destination_valid):
        destination = input('Destination not valid. Please enter the destination location: ')
        destination_valid = re.match('^[A-Za-z0-9_]*$',destination)
    destination, destination_valid = choose_location(destination,database)
    if (not destination):
        print('Failed to find a source location. Ride offer aborted')
        return

    #CAR
    add_car = input('Would you like to add a car to this ride y/n? ').lower()
    while(add_car != 'n' and add_car != 'y'):
        add_car = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to add a car to this ride? ')
    car, car_found = choose_car(add_car,current_user_email,database)

    #CREATE RNO AND INSERT
    c.execute('SELECT rno FROM rides ORDER BY rno desc LIMIT 1')
    rno = c.fetchone()[0] + 1
    if (car_found):
        c.execute('INSERT INTO rides VALUES (:rno, :price, :rdate, :seats, :lugDesc, :src, :dst, :driver, :cno);', {"rno":rno, "price":seat_price, "rdate":date, "seats":num_seats, "lugDesc":luggage_description, "src":source, "dst":destination, "driver":current_user_email, "cno":car})
        print('Added a ride: %s, %s, %s, %s, %s, %s, %s, %s, %s'%(rno,seat_price,date,num_seats,luggage_description,source,destination,current_user_email,car))
    else:
        c.execute('INSERT INTO rides VALUES (:rno, :price, :rdate, :seats, :lugDesc, :src, :dst, :driver, :cno);', {"rno":rno, "price":seat_price, "rdate":date, "seats":num_seats, "lugDesc":luggage_description, "src":source, "dst":destination, "driver":current_user_email, "cno":''})
        print('Added a ride: %s, %s, %s, %s, %s, %s, %s, %s'%(rno,seat_price,date,num_seats,luggage_description,source,destination,current_user_email))
    conn.commit()

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
            enroute, enroute_found = choose_location(enroute_keyword,database)
            if(enroute_found):
                c.execute("INSERT INTO enroute VALUES (:rno, :lcode);", {"rno":rno, "lcode":enroute})
                print('Enroute location: %s added to ride: %s'%(enroute,rno))
            add_enroute = input("Would you like to add another enroute location y/n? ")
    return

def search_rides(current_user_email,database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()  

    # First keyword
    keyword1 = input('Please enter a location keyword to search: ')
    keyword1_valid = re.match('^[A-Za-z0-9_]*$',keyword1)
    while(not keyword1_valid):
        keyword1 = input('Keyword not valid. Please enter a location keyword: ')
        keyword1_valid = re.match('^[A-Za-z0-9_]*$',keyword1)
    keyword_count = 1
    # Second keyword
    add_keyword = input('Would you like to add a second keyword y/n? ').lower()
    while(add_keyword != 'n'):
        if(add_keyword != 'y'):
            add_keyword = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to add a second keyword? ')
        else:
            keyword2 = input('Please enter a location keyword to search: ')
            keyword2_valid = re.match('^[A-Za-z0-9_]*$',keyword2)
            while(not keyword2_valid):
                keyword2 = input('Keyword not valid. Please enter a second location keyword: ')
                keyword2_valid = re.match('^[A-Za-z0-9_]*$',keyword2)
            add_keyword = 'n'
            keyword_count = 2
        # Third keyword
        add_keyword = input('Would you like to add a third keyword y/n? ').lower()
        while(add_keyword != 'n'):
            if(add_keyword != 'y'):
                add_keyword = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to add a third keyword? ')
            else:
                keyword3 = input('Please enter a location keyword to search: ')
                keyword3_valid = re.match('^[A-Za-z0-9_]*$',keyword3)
                while(not keyword3_valid):
                    keyword3 = input('Keyword not valid. Please enter a second location keyword: ')
                add_keyword = 'n'
                keyword_count = 3
                
    if(keyword_count == 1):
        rno = multi_parameter_ride_search(database,keyword1)
    elif(keyword_count == 2):
        rno = multi_parameter_ride_search(database,keyword1,keyword2)
    elif(keyword_count == 3):
        rno = multi_parameter_ride_search(database,keyword1,keyword2,keyword3)

    if (rno == None):
        print("No ride found")
        return

    message_request = input('Would you like to message the poster of this ride requesting a booking y/n? ').lower()
    message_sent = False
    while(message_request != 'n' and not message_sent):
        if (message_request != 'y'):
            message_request = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to message the poster of this ride requesting a booking? ')
        else:
            message(rno,current_user_email,database)
            message_sent = True




def choose_location(location_keyword,database):
    # Takes a keyword argument and allows the user to choose a location which matches that keyword

    conn = sqlite3.connect('./'+database)
    c = conn.cursor()  

    choices_found = False
    choice = None
    if (len(location_keyword)<=5):      # Lcode case
        c.execute('SELECT lcode FROM locations WHERE lcode LIKE ?', (location_keyword,))
        choice = c.fetchone()
    if (choice != None):
        choices_found = True
        return choice[0], choices_found
    
    else:                               # Keyword case
        c.execute("SELECT lcode, address, city, prov FROM locations WHERE address LIKE ? OR prov LIKE ? or city LIKE ?", ('%'+location_keyword+'%','%'+location_keyword+'%','%'+location_keyword+'%'))
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

def choose_car(add_car,current_user_email,database):
    # Helper function to allow the user to choose a car

    conn = sqlite3.connect('./'+database)
    c = conn.cursor()  

    if(add_car == 'y'):
        car = input('Please enter the car number: ')
        car_valid = re.match('^[0-9]*$', car)
        while (not car_valid):
            car = input('Car number invalid. Please enter the car number: ')
            car_valid = re.match('^[0-9]*$', car)  
        c.execute('SELECT cno FROM cars WHERE owner == ?', (current_user_email,))
        car_responses = c.fetchall()
        owned_cars = []
        for row in car_responses:
            owned_cars.append(str(row[0]))
        if(not car in owned_cars):
            add_car = input('You do not own that car. Would you like to add a different car to the ride y/n? ').lower()
            while(add_car != 'n' and add_car != 'y'):
                add_car = input('Input invalid. Please respond with either \'y\' or \'n\'. Would you like to add a different car to this ride? ')
            if(add_car == 'n'):
                return '', False
            else:
                return choose_car(add_car, current_user_email,database)
        else:
            return car, True
    else:
        return '', False

def multi_parameter_ride_search(database,keyword1, keyword2=None, keyword3 = None):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()  

    keywords, lcodes = [keyword1], []
    if(keyword2 != None):
        keywords.append(keyword2)
        if(keyword3 != None):   
            keywords.append(keyword3)

    keyword_count = len(keywords)

    # Get viable lcodes
    location_returns = {}
    for keyword in keywords:
        location_returns[keyword] = []
        c.execute("SELECT DISTINCT lcode FROM locations WHERE address LIKE ? OR prov LIKE ? or city LIKE ? or lcode LIKE ?", ('%'+keyword+'%','%'+keyword+'%','%'+keyword+'%','%'+keyword+'%'))
        current_lcodes = c.fetchall()
        for lcode in current_lcodes:
            location_returns[keyword].append(lcode[0])
    
    # Make sure all keywords match
    if (keyword_count != 1):
        if (keyword_count == 2):
            for lcode in location_returns[keyword1]:
                if (lcode in location_returns[keyword2]):
                    lcodes.append(lcode)
        else:
            for lcode in location_returns[keyword1]:
                if ((lcode in location_returns[keyword2]) and (lcode in location_returns[keyword3])):
                    lcodes.append(lcode)
    else:
        lcodes = location_returns[keyword1]

    rides = []
    # Get and show rides 
    chosen_rno = None
    c.execute("SELECT * FROM enroute")
    all_enroutes = c.fetchall()
    enroutes = []
    for lcode in lcodes:
        c.execute('SELECT * FROM rides WHERE src LIKE ? OR dst LIKE ? COLLATE NOCASE', (lcode, lcode))
        fetched_rows = c.fetchall()
        for row in fetched_rows:
            if row not in rides:
                rides.append(row)
        
        for row in all_enroutes:
            if row[1] == lcode:
                enroutes.append(row[0])

        for rno in enroutes:
            c.execute('SELECT * FROM rides WHERE rno == ?', (rno,))
            fetched_rows = c.fetchall()
            for row in fetched_rows:
                if row not in rides:
                    rides.append(row)
    
    idx = 0
    while(idx < len(rides)):
        if(idx ==0 or idx % 5 != 0):
            cno = rides[idx][8]
            c.execute('SELECT * FROM cars WHERE cno == ?',(cno,))
            car_info = c.fetchone()
            if car_info != None:
                print(rides[idx]+car_info)
            else:
                print(rides[idx])
            idx += 1
        else:
            response = input('If any of these rides are what you are looking for enter the rno of that ride. Else press enter to see more results. ')
            if (re.match('^[0-9]*$',response)):
                chosen_rno = response
                break
            else:
                c.execute('SELECT * FROM cars WHERE cno == ?', rides[idx][8])
                car_info = c.fetchone()
                if car_info != None:
                    print(rides[idx]+car_info)
                else:
                    print(rides[idx])
                idx += 1
    if (chosen_rno == None):
        response = input('If any of these rides are what you are looking for enter the rno of that ride. Else press enter to abandon search. ')
        if (re.match('^[0-9]+$',response)):
            chosen_rno = response
        else:
            chosen_rno = None

    if (chosen_rno != None):
        for i in range(len(rides)):
            if int(chosen_rno) == int(rides[i][0]):
                return chosen_rno
        print('Not a valid rno')
    return None

def message(rno, current_user_email,database):
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()  

    c.execute('SELECT driver FROM rides WHERE rno == ?', rno)
    driver = c.fetchone()
    c.execute("SELECT datetime('now')")
    datetime = c.fetchone()
    message = input("What would you like the message to the rider to say? ")
    message_valid = re.match('^[A-Za-z0-9_ ]*$',message)
    while (not message_valid):
        message = input("Message invalid. What would you like the message to the rider to say? ")
        message_valid = re.match('^[0-9]*$',message)
    c.execute("INSERT INTO inbox VALUES (:email, :msgTimestamp, :sender, :content, :rno, :seen);", {"email":driver[0], "msgTimestamp":datetime[0], "sender":current_user_email, "content":message, "rno":rno, "seen":'n'})
    conn.commit()
    print("Message Sent")
