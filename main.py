import sqlite3
from login import login
from offer import offer

def main():
    conn = sqlite3.connect('./proj.db')
    c = conn.cursor()
    c.execute('Select * from members')
    print(c.fetchone())

    login()
    action_choice = input('What action would you like to perform?').lower()
    while(action_choice!='exit'):
        if(action_choice == 'help'):
            help()

        elif (action_choice == 'offer'):
            offer()
        
        else:
            print('That is not a possible action. For information on possible actions type \'help\'')
        action_choice = input('What action would you like to perform?').lower()
        
    conn.close()
def help():
    print('INSERT HELP HERE')

main()
