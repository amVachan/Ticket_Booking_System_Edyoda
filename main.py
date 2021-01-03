from IPython.display import clear_output
from cinema import Seat,Cinema
from user import User
import mysql.connector



rows=int(input('Enter the number of rows: '))
columns=int(input('Enter the number of columns: '))
cinema=Cinema(rows,columns)

def start_screen():
    print('''Enter your option
    1. Show the seats
    2. Buy a ticket
    3. Statistics
    4. Show booked Tickets User Info
    0. Exit
    ''')
    option = int(input())
    return option

def create_user():
    infos=['name','gender','age','phoneNo']
    inpt=[]
    for info in infos:
        inpt.append(input(f'Enter your {info}: '))
    user=User(inpt[0],inpt[1],int(inpt[2]),int(inpt[3]))
    return user
def go_back():
    Input=int(input('Enter 0 to go back: '))
    if Input==0:
              return True
flag = True

while flag:
    option=start_screen()
    if option == 1:
        cinema.show_seats()
    elif option == 2:
        row=int(input('Enter the row number: '))
        column=int(input('Enter the column number: '))
        status=cinema.check_status(row,column)
        if status=='S':
            price=cinema.calculate_price(row,column)
            book=input(f'Enter yes if you want to book the seat with the price ${price}: ')
            if book.lower()=='yes':
                user=create_user()
                cinema.book_seat(row,column,user)
                if go_back():
                    clear_output()
                    continue
            else:
                continue
        else:
            print("Sorry, this seat has already been booked")
            cinema.user_info(row,column)
            if go_back():
                    clear_output()
                    continue
    elif option == 3:
        cinema.statistics()
        if go_back():
                    clear_output()
                    continue
    elif option == 4:
        row=int(input('Enter the row number: '))
        column=int(input('Enter the column number: '))
        status=cinema.check_status(row,column)
        if status=='S':
            print('This seat has not been booked')
            if go_back():
                    clear_output()
                    continue
        else:
            cinema.user_info(row,column)
            if go_back():
                    clear_output()
                    continue
    elif option == 0:
        flag=False