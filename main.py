import sqlite3
import sys
from login import login
from deleteRequest import delete_request
from searchRequests import search_requests
from rides import offer_ride, search_rides

def main():
    if len(sys.argv)!=2:
        print('ERROR: No database specified')
        return
    database = sys.argv[1]
    conn = sqlite3.connect('./'+database)
    c = conn.cursor()

    current_user_email = login(database)
    action_choice = input('What action would you like to perform? ').lower()
    while(action_choice!='exit'):
        if(action_choice == 'help'):
            help()

        elif (action_choice == 'offer'):
            offer_ride(current_user_email)
        
        elif (action_choice == 'search_rides'):
            search_rides(current_user_email)

        elif (action_choice == 'search_requests'):
            search_requests(current_user_email, database)

        elif (action_choice == 'delete_request'):
            delete_request(current_user_email, database)
        
        else:
            print('That is not a possible action. For information on possible actions type \'help\'')
            
        action_choice = input('What action would you like to perform? ').lower()
        
    conn.close()
def help():
    print('INSERT HELP HERE')

main()
