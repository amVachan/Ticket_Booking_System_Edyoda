from user import User
import mysql.connector
from password import password

User='root'
Password =password
Host='localhost'
Database='cinema'

class Seat():
    
    def __init__(self,seatNo,status,price):
        self.seatNo=seatNo
        self.status=status
        self.price=price
        self.insert_to_db()
        
    def insert_to_db(self):
        conn=mysql.connector.connect(user=User,password=Password,host=Host,database=Database)
        crsr=conn.cursor()
        crsr.execute("INSERT INTO Seats(seatNo,status,price) VALUES (%s,%s,%s)",(self.seatNo,self.status,self.price))
        conn.commit()
        crsr.close()
        conn.close()


class Cinema():
    
    def __init__(self,rows,columns):
        self.rows=rows
        self.columns=columns
        self.clear_db()
        self.create_seats()
    
    def create_seats(self):
        for row in range(1,self.rows+1):
            for column in range(1,self.columns+1):
                seatNo=str(row)+'-'+str(column)
                price=self.calculate_price(row,column)
                Seat(seatNo,'S',price)
        
    
    def show_seats(self):
        conn=mysql.connector.connect(user=User,password=Password,host=Host,database=Database)
        crsr=conn.cursor()
        crsr.execute("SELECT status from Seats")
        result=crsr.fetchall()
        x=0
        print('Cinema: ')
        print('   '+'  '.join([str(x) for x in range(1,self.columns+1)]))

        for r in range(self.rows):
            print(str(r+1),end='  ')
            for c in range(self.columns):
                print(result[c+x][0],end='  ')
            print('\n')
            x+=self.columns
        
    def book_seat(self,row,column,user):
        conn=mysql.connector.connect(user=User,password=Password,host=Host,database=Database)
        crsr=conn.cursor()
        seatNo=str(row)+'-'+str(column)     
        crsr.execute("INSERT INTO Users(seatNo,name,gender,phoneNo,age) VALUES (%s,%s,%s,%s,%s)",(seatNo,user.name,
                   user.gender,user.phoneNo,user.age))
        crsr.execute("UPDATE Seats SET status='B' WHERE seatNo=%s",(seatNo,))
        conn.commit()
        crsr.close()
        conn.close()
        print("Your Ticket has been booked successfully!")
            
    
    def statistics(self):
        stats=['No of purchased tickets','Percentage of tickets booked','Current Income','Total Income']
        
        conn=mysql.connector.connect(user=User,password=Password,host=Host,database=Database)
        crsr=conn.cursor()
        crsr.execute("SELECT COUNT(seatNo),SUM(price) FROM Seats WHERE status='B'")
        result=crsr.fetchall()
        crsr.execute("SELECT COUNT(*),SUM(price) FROM Seats")
        result+=crsr.fetchall()
        crsr.close()
        conn.close()
        if result[0][0]:
            print(stats[0]+' : '+str(result[0][0]))
            print(stats[1]+' : '+str(round(((result[0][1]/result[1][1])*100),2))+'%')
            print(stats[2]+' : $'+str(result[0][1]))
            print(stats[3]+' : $'+str(result[1][1]))
        else:
            print('No seats have been booked yet.')


    def user_info(self,row,column):
        info=["Name","Gender","Age","Ticket Price in $","Phone No"]
        seatNo=str(row)+'-'+str(column)
        conn=mysql.connector.connect(user=User,password=Password,host=Host,database=Database)
        crsr=conn.cursor()
        crsr.execute("SELECT U.name,U.gender,U.age,C.price,U.phoneNo FROM Users U INNER JOIN Seats C ON U.seatNo=C.seatNo WHERE C.seatNo=%s",(seatNo,))
        result=crsr.fetchall()
        conn.commit()
        crsr.close()
        conn.close()
        for i,inf in enumerate(info):
            print(inf+' : '+str(result[0][i]))
    
    def check_status(self,row,column):
        seatNo=str(row)+'-'+str(column)
        conn=mysql.connector.connect(user=User,password=Password,host=Host,database=Database)
        crsr=conn.cursor()
        crsr.execute("SELECT status from  Seats  WHERE seatNo=%s",(seatNo,))
        result=crsr.fetchone()
        crsr.close()
        conn.close()
        return result[0]
    
    def calculate_price(self,row,column):
        if self.rows*self.columns <= 60:
            price = 10
        elif self.rows*self.columns > 60:
            if row <= self.rows//2:
                price = 10
            else:
                price = 8
        return price
        
    def clear_db(self):
        conn=mysql.connector.connect(user=User,password=Password,host=Host,database=Database)
        crsr=conn.cursor()
        crsr.execute("DELETE FROM Users")
        crsr.execute("DELETE FROM Seats")
        conn.commit()
        crsr.close()
        conn.close()