import mysql.connector
from datetime import datetime
from getpass import getpass

mysql_password = getpass("Enter your MySQL password: ")

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password=mysql_password
)

mycursor=mydb.cursor()#cursor is an object used by python to send sql commands to mysql.
mycursor.execute("create database if not exists hotlman")
#print("created successfully")

mycursor.execute("use hotlman")
mycursor.execute("create table if not exists rooms(room_id int primary key,room_type varchar(25),price int,status varchar(35))")
mydb.commit()
mycursor.execute("create table if not exists customers(Customer_id int primary key,Customer_name varchar(25),Phone varchar(25),Email varchar(80),Address varchar(100))")
mydb.commit()
mycursor.execute("create table if not exists booking(Booking_id int primary key,Customer_id int,Room_id int,Check_in datetime,Check_out datetime)")
mydb.commit()
#mycursor.execute("alter table booking add constraint fk_room foreign key(Room_id)references rooms(room_id),add constraint fk_customer foreign key(Customer_id) references customers(Customer_id) ")
#mydb.commit()


#mycursor.execute("alter table rooms add primary key(room_id)")
#mydb.commit()
class room:
    def add_room(self):
        room_id=int(input("Enter the Room ID:"))
        room_typ=input("Enter room type(Standard/Deluxe/Premium/Suite):")
        room_price=int(input("Enter the room price:"))
        room_status=input("Enter status(available/occupied):")
        mycursor.execute("insert into rooms(room_id,room_type,price,status)values(%s,%s,%s,%s)",(room_id,room_typ,room_price,room_status))##here %s is a placeholder.it acts as a blankspace where python fill it later
        mydb.commit()
        print(f"Room {room_id} added successfully")
    def update_room(self):
        room_no=int(input("Enter the room number/Id:"))
        mycursor.execute("select * from rooms where room_id=%s",(room_no,))
        rm_ans=mycursor.fetchone()
        if rm_ans is None:
            print(f"Room {room_no} doesn't exist")
            return
        update_what=input("what you want to update:(room_type/price)")
        ans=update_what.lower()
        if ans=='room_type':
            new_type=input("Enter room type(Standard/Deluxe/Premium/Suite):")
            mycursor.execute("update rooms set room_type=%s where room_id=%s",(new_type,room_no))
            mydb.commit()
            print(f"Room {room_no} type updated successfully.")
        elif ans=='price':
            room_prce=int(input("Enter the new price:"))
            mycursor.execute("update rooms set price=%s where room_id=%s",(room_prce,room_no))
            mydb.commit()
            print(f"Room {room_no} price updated successfully.")
        else:
            print("invalid option")

    def delete_room(self):
        del_room=int(input("Enter the room_id for deletion:"))
        mycursor.execute("select * from rooms where room_id=%s",(del_room,))
        del_rm=mycursor.fetchone()
        if del_rm is None:
            print(f"Room {del_room} doesn't exists")
            return
        if del_rm[3]=='occupied':
            print(f"Room {del_room} is occupied")
            return
        mycursor.execute("delete from rooms where room_id=%s",(del_room,))
        mydb.commit()
        print(f"Room {del_room} deleted successfully")
    def search_room(self):
        srch=int(input("Enter the room_id:"))
        mycursor.execute("select * from rooms where room_id=%s",(srch,))
        rslt=mycursor.fetchone()#fetchone() returns one row at a time
        if rslt:#rslt contain some information
            print(f"Room {srch} found")
            print(rslt)
        else:#rslt=none
            print(f"Room {srch} not found")
    def available_room(self):
        print("------------------------------")
        print("        Available Rooms       ")
        print("------------------------------")
        mycursor.execute("select * from rooms where status='available' ")
        rslt=mycursor.fetchall()  # fetchall() returns a list of all matching rows
                                  # if no rows are found, it returns []
        if rslt:
            for row in rslt:
                print(f"Room:{row[0]}")
                print(f"Type:{row[1]}")
                print(f"Price:{row[2]}")
                print(f"Status:{row[3]}\n")
                
                
        else:#if rslt=[] else works
            print("Not available")
class customer:
    def add_customer(self):
        cstmr_id=int(input("Enter the customer id:"))
        mycursor.execute("select * from customers where Customer_id=%s",(cstmr_id,))
        rslt=mycursor.fetchone()
        if rslt:
            print(f"Customer {cstmr_id} already exists")
            return
        cstmr_name=input("Enter customer name:")
        cstmr_phn=input("Enter customer phone:")
        cstmr_email=input("Enter customer email:")
        cstmr_addrss=input("Enter customer address:")
        mycursor.execute("insert into customers(Customer_id,Customer_name,Phone,Email,Address)values(%s,%s,%s,%s,%s)",(cstmr_id,cstmr_name,cstmr_phn,cstmr_email,cstmr_addrss))
        mydb.commit()
        print(f"Customer {cstmr_id} added successfully")
    def update_customer(self):
        cstm_id=int(input("Enter customer id:"))
        mycursor.execute("select * from customers where Customer_id=%s",(cstm_id,))
        cst_updt=mycursor.fetchone()
        if cst_updt is None:
            print(f"Customer {cstm_id} not exists")
            return
        wht_updte=input("What you want to change(name/phone/email/address):")
        updt=wht_updte.lower()
        if updt=='name':
            nw_name=input("Enter new name:")
            mycursor.execute("update customers set Customer_name=%s where Customer_id=%s",(nw_name,cstm_id))
            mydb.commit()
            print(f"Customer {cstm_id} name updated successfully.")
        elif updt=='phone':
            nw_phn=input("Enter new phone number:")
            mycursor.execute("update customers set Phone=%s where Customer_id=%s",(nw_phn,cstm_id))
            mydb.commit()
            print(f"Customer {cstm_id} phone number updated successfully")
        elif updt=='email':
            nw_email=input("Enter new email:")
            mycursor.execute("update customers set Email=%s where Customer_id=%s",(nw_email,cstm_id))
            mydb.commit()
            print(f"Customer {cstm_id} email updated successfully.")
        elif updt=='address':
            nw_addrss=input("Enter new address:")
            mycursor.execute("update customers set Address=%s where Customer_id=%s",(nw_addrss,cstm_id))
            mydb.commit()
            print(f"Customer {cstm_id} address updated successfully.")
        else:
            print("Invalid option")
    def delete_customer(self):
        cst_id=int(input("Enter customer id:"))
        mycursor.execute("select * from customers where Customer_id=%s",(cst_id,))
        cst_rslt=mycursor.fetchone()
        if cst_rslt is None:
                    print(f"Customer {cst_id} doesn't exist")
                    return

        mycursor.execute("select * from booking where Customer_id=%s",(cst_id,))
        chck_rsl=mycursor.fetchone()
        if chck_rsl is not None:
            print(f"Customer {cst_id} has a booking")
            return
        
        mycursor.execute("delete from customers where Customer_id=%s",(cst_id,))
        mydb.commit()
        print(f"Customer {cst_id} deleted successfully")
    def search_customer(self):
        cst_id=int(input("Enter customer id:"))
        mycursor.execute("select * from customers where Customer_id=%s",(cst_id,))
        rslt=mycursor.fetchone()
        if rslt:

            print("Customer Details")
            print("------------------")
            print(rslt)
        else:
            print(f"Customer {cst_id} not found")
    def view_customers(self):
        mycursor.execute("select * from customers")
        out=mycursor.fetchall()
        if out:
            print("Customer details")
            print("--------------------")
            for row in out:
             
                print(f"Customer_id:{row[0]}")
                print(f"Customer_name:{row[1]}")
                print(f"Phone:{row[2]}")
                print(f"Email:{row[3]}")
                print(f"Address:{row[4]}\n")
                
        else:
            print("Nothing found")

class bookings:
    def add_booking(self):
        custm_id=int(input("Enter Customer ID:"))
        mycursor.execute("select * from customers where Customer_id=%s",(custm_id,))
        out=mycursor.fetchone()
        if out is None:
            print(f"Customer {custm_id} does not exist")
            return
        bkng_id=int(input("Enter Booking ID:"))
        mycursor.execute("select * from booking where Booking_id=%s",(bkng_id,))
        bk_rslt=mycursor.fetchone()
        if bk_rslt is not None:
            print(f"Booking_id {bkng_id} already exists")
            return
        rum_id=int(input("Enter Room ID:"))
        #check whether the room exists or not
        mycursor.execute("select status from rooms where room_id=%s",(rum_id,))
        room_rslt=mycursor.fetchone()
        if room_rslt is None:
            print(f"Room {rum_id} does not exist")
            return
        if room_rslt[0]!='available':
            print(f"Room {rum_id} is already occupied")
            return
        chck_in=input("Enter check-in(YYYY-MM-DD HH:MM:SS):")
        chck_out=input("Enter check-out(YYYY-MM-DD HH:MM:SS):")
        try:
            new_chk_in=datetime.strptime(chck_in,"%Y-%m-%d %H:%M:%S")
            new_chk_out=datetime.strptime(chck_out,"%Y-%m-%d %H:%M:%S")
            if new_chk_out<=new_chk_in:
                print("check-out must be after check_in")
                return
        except ValueError:
            print("Invalid date format")
            return
        #add booking
        mycursor.execute("insert into booking(Booking_id,Customer_id,Room_id,Check_in,Check_out)values(%s,%s,%s,%s,%s)",(bkng_id,custm_id,rum_id,new_chk_in,new_chk_out))
        mydb.commit()
        #change room status
        mycursor.execute("update rooms set status=%s where room_id=%s",('occupied',rum_id))
        mydb.commit()
        print(f"Booking ID {bkng_id} added successfully")
        print(f"Room {rum_id} is now occupied")

    def update_booking(self):
        bk_id=int(input("Enter booking id:"))
        #checking bk_id exists or not
        mycursor.execute("select * from booking where Booking_id=%s",(bk_id,))
        rslt=mycursor.fetchone()
        if rslt is None:
            print(f"Booking ID {bk_id} doesn't exists")
            return
        #if exists
        wht_updt=input("What you want to update(room id,customer id,check in,check out)")
        bk_updt=wht_updt.lower()
        if bk_updt=='room id':
            nwrm_id=int(input("Enter new room ID:"))
            mycursor.execute("select status from rooms where room_id=%s",(nwrm_id,))
            x=mycursor.fetchone()

            if x is None:
                print(f"Room {nwrm_id} does not exist")
                return

            if x[0]=='occupied':
                print(f"Room {nwrm_id} is occupied")
                return

            old_room_id=rslt[2]

            mycursor.execute("update rooms set status=%s where Room_id=%s",('available',old_room_id))
            mydb.commit()

            mycursor.execute("update booking set Room_id=%s where Booking_id=%s",(nwrm_id,bk_id))
            mydb.commit()

            mycursor.execute("update rooms set status=%s where Room_id=%s",('occupied',nwrm_id))
            mydb.commit()

            print("updated successfully")
        elif bk_updt=='customer id':
            nwcst_id=int(input("Enter new customer ID:"))
            mycursor.execute("select * from customers where Customer_id=%s",(nwcst_id,))
            cstd=mycursor.fetchone()
            if cstd is None:
                print(f"customer {nwcst_id} doesn't exists")
                return
            
            mycursor.execute("update booking set Customer_id=%s where Booking_id=%s",(nwcst_id,bk_id))
            mydb.commit()
            print("updated successfully")
        elif bk_updt=='check in':
            nwchk_in=input("Enter new check_in(YYYY-MM-DD HH:MM:SS):")
            old_check_out=rslt[4]
            try:
                new_check_in= datetime.strptime(nwchk_in,"%Y-%m-%d %H:%M:%S")
                if new_check_in < old_check_out:
                    mycursor.execute("update booking set Check_in=%s where Booking_id=%s",(nwchk_in,bk_id))
                    mydb.commit()
                    print("updated successfully")
                else:
                    print("Check-in must be before check-out")
            except ValueError:
                print("Invalid date format")
        elif bk_updt=='check out':
            nwchk_out=input("Enter new check_out(YYYY-MM-DD HH:MM:SS):")
            old_check_in=rslt[3]
            try:
                new_check_out= datetime.strptime(nwchk_out,"%Y-%m-%d %H:%M:%S")
                if new_check_out > old_check_in:
                    mycursor.execute("update booking set Check_out=%s where Booking_id=%s",(nwchk_out,bk_id))
                    mydb.commit()
                    print("updated successfully")
                else:
                    print("Check-out must be after check-in")
            except ValueError:
                print("Invalid date format")
        else:
            print("Invalid option")
    def delete_booking(self):
        bkng_id=int(input("Enter booking ID:"))
        mycursor.execute("select Room_id from booking where Booking_id=%s",(bkng_id,))
        rst=mycursor.fetchone()
        if rst is None:
            print(f"Booking {bkng_id} does not exist")
            return
        room_id=rst[0]
        mycursor.execute("delete from booking where Booking_id=%s",(bkng_id,))
        mydb.commit()
        print(f"Booking ID {bkng_id} removed successfully")
        mycursor.execute("update rooms set status=%s where Room_id=%s",('available',room_id))
        mydb.commit()

    def search_booking(self):
        bkng_id=int(input("Enter the Booking ID you want to search:"))
        mycursor.execute("select * from booking where Booking_id=%s",(bkng_id,))
        rslt=mycursor.fetchone()
        if rslt:
            print(f'Booking ID {bkng_id} details:')
            print(rslt)

        else:
            print("Not found")
    def view_booking(self):
        mycursor.execute("select * from booking")
        out=mycursor.fetchall()
        if out:
            print("Booking details")
            print("-----------------")
            for row in out:
                print(f"Booking ID :{row[0]}")
                print(f"Customer ID :{row[1]}")
                print(f"Room ID :{row[2]}")
                print(f"Check IN :{row[3]}")
                print(f"Check Out :{row[4]}\n")
                print("--------------------------")
        else:
            print("Not found")
    def checkout(self):
        bkng_id=int(input("Enter Booking ID:"))
        mycursor.execute("select * from booking where Booking_id=%s",(bkng_id,))
        rsl=mycursor.fetchone()
        if rsl is None:
            print(f"Booking {bkng_id} doesn't exists")
            return
        rm_id=rsl[2]
        mycursor.execute("update rooms set status =%s where room_id=%s",('available',rm_id))
        mydb.commit()
        mycursor.execute("delete from booking where Booking_id=%s",(bkng_id,))
        mydb.commit()
        print(f"Booking {bkng_id} checkout successfully")
        print(f"Room {rm_id} is now available")

rm=room()     
cst=customer()    
bk=bookings()

while True:
    print("========================")
    print(" HOTEL MANAGEMENT SYSTEM ")
    print("========================")
    print("1.Room Management")
    print("2.Customer Management")
    print("3.Booking Management")
    print("4.Exit")
    choice=int(input("Enter a choice:"))
    if choice==1:
        while True:
            print("------Room Management------")
            print("1.Add Room")
            print("2.Update Room")
            print("3.Delete room")
            print("4.Search Room")
            print("5.Available Room")
            print("6.Back")
            room_choice=int(input("Enter your choice:"))
            if room_choice==1:
                rm.add_room()
            elif room_choice==2:
                rm.update_room()
            elif room_choice==3:
                rm.delete_room()
            elif room_choice==4:
                rm.search_room()
            elif room_choice==5:
                rm.available_room()
            elif room_choice==6:
                break
            else:
                print("Invalid choice")

    elif choice==2:
           while True:
                    print("----Customer Management------")
                    print("1.Add Customer")
                    print("2.Update Customer")
                    print("3.Delete Customer")
                    print("4.Search Customer")
                    print("5.View Customer")
                    print("6.Back")
                    custm_choice=int(input("Enter your choice:"))
                    if custm_choice==1:
                        cst.add_customer()
                    elif custm_choice==2:
                        cst.update_customer()
                    elif custm_choice==3:
                        cst.delete_customer()
                    elif custm_choice==4:
                        cst.search_customer()
                    elif custm_choice==5:
                        cst.view_customers()
                    elif custm_choice==6:
                        break
                    else:
                        print("Invalid choice")
    elif choice==3:
        while True:
            print("----Booking Management------")
            print("1.Add Booking")
            print("2.Update Booking")
            print("3.Delete Booking")
            print("4.Search Booking")
            print("5.View Booking")
            print("6.Checkout")
            print("7.Back")
            Booking_choice=int(input("Enter your choice:"))
            if Booking_choice==1:
                bk.add_booking()
            elif Booking_choice==2:
                bk.update_booking()
            elif Booking_choice==3:
                bk.delete_booking()
            elif Booking_choice==4:
                bk.search_booking()
            elif Booking_choice==5:
                bk.view_booking()
            elif Booking_choice==6:
                bk.checkout()
            elif Booking_choice==7:
                break
            else:
                print("Invalid choice")
   
    elif choice==4:
        print("Thank you!")
        break
    else:
        print("Invalid choice")
