#Library management system
import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',passwd='123456')
mycursor=mydb.cursor()
print("""*******************************************************************
            Welcome to the LIBRARY MANAGEMENT SYSTEM
*******************************************************************""")
#Creating database
mycursor.execute('Create database if not exists LMS')#if not exists?
mycursor.execute('use lms')
mycursor.execute('create table if not exists av_books(id int,name varchar(35), subject varchar(25), qty int)')
mycursor.execute('create table if not exists issued(id int,name varchar(35), subject varchar(25), sid int)')
mycursor.execute('create table if not exists login(user varchar(25),password int)')
mydb.commit()#permanently executed in mysql

#FOR SINGLE DATABASE ADMINISTRATOR
userstored=0
mycursor.execute('select * from login')
for i in mycursor:
    userstored=1
if userstored==0:
    mycursor.execute("insert into login values ('user',123456)")
    mydb.commit()
while True:
    print("""
1. Login
2. Exit
""")
    ch=int(input('Enter your choice:'))
    if ch==1:
        u=input('Enter Username:')
        p=int(input('Enter Password:'))
        mycursor.execute('select * from login')
        rows=mycursor.fetchall()
        user=''
        pas=0
        logged=False
        for row in rows: #var1,var2=(x,y)
            user,pas=row#user,password
            #pas=int(pas)#unpacking obtains password as a string
            if p==pas and u==user:
                print('Login Complete...')
                logged=True
        if logged:  
            while True:
                print("""*******************************************************************
1)Add New Books
2)Remove Any Book
3)Issue Book to Student
4)Return Book
5)View Available Books
6)View Issued Books
7)Logout
******************************************************************""")
                choice=int(input('Enter Choice:'))
                if choice==1:
                    while True:
                        print('All the information asked below is mandatory')
                        bid=int(input('Enter the book\'s id'))
                        name=input('Enter the name of the book')
                        subject=input('Enter the name of the subject:')
                        qty=input('Enter quantity:')
                        mycursor.execute("insert into av_books values ({},'{}','{}',{})".format(bid,name,subject,qty))
                        mydb.commit()
                        print('Successfully added book to DB.')
                        c=input('Do you want to add more books? y/n')
                        if c.lower()=='n':
                            break
                        
                elif choice==2:
                    bid=int(input('Enter the book\'s id'))
                    mycursor.execute('select * from av_books')
                    d=mycursor.fetchall()
                    bexists=False#flag
                    for row in d:
                        bookid,name,sub,qty=row#unpacking
                        print(type(bookid))
                        if bookid==bid:
                            bexists=True
                    if bexists:
                        
                        mycursor.execute('delete from av_books where id={}'.format(bid))
                        mydb.commit()
                        print('Book successfully removed!')
                    else:
                        print(f'No book with book id {bid} exists in the database')
                elif choice==3:
                    while True:
                        bid=int(input('Enter the id of the book:'))
                        sid=input('Enter the id of student:')
                        mycursor.execute('Select * from av_books where id={}'.format(bid))
                        foundbook=False    
                        name=''
                        sub=''
                        qty=0
                        for record in mycursor:
                            idd,name,sub,qty=record #unpacking
                            foundbook= True
                        if foundbook:
                            if qty>0:
                                mycursor.execute("Insert into issued values ({},'{}','{}',{})".format(bid,name,sub,sid))
                                mydb.commit()
                                qty=qty-1
                                mycursor.execute("Update av_books set qty={} where id={}".format(qty,bid))
                                mydb.commit()
                                print('Successfully issued...')
                            else:
                                print(f'Sorry all the books with book id={bid} have been issued')
                        else:
                            print(f'Book with book id {bid} not found!')
                        c=input('Do you want to issue more books? y/n')
                        if c.lower()=='n':
                            break
                elif choice==4:
                    while True:
                        
                        bid=int(input('Enter book id:'))
                        sid=int(input('Enter student id:'))
                        mycursor.execute('select * from av_books where id={}'.format(bid))
                        qty=0
                        bookexists=False
                        for record in mycursor:
                            idd,name,sub,qty=record
                            bookexists=True
                        if bookexists:
                            issue=False
                            mycursor.execute('select * from issued where id={} and sid={}'.format(bid,sid))
                            for record in mycursor:
                                issue=True
                            if issue:
                                mycursor.execute('delete from issued where id={} and sid={}'.format(bid,sid))
                                mydb.commit()
                                qty+=1
                                mycursor.execute("Update av_books set qty={} where id={}".format(qty,bid))
                                mydb.commit()
                                print('Successfully returned...')
                            else:
                                print(f'No issuing of book with book id ={bid} by student with student id={sid} has taken place')
                        
                        else:
                            print(f'No book with book id = {bid} exists in this library!')
                        c=input('Do you want to return more books?')
                        if c.lower()=='n':
                            break
                
                elif choice==5:
                    mycursor.execute('Select * from av_books')
                    records=mycursor.fetchall()
                    print('ID | NAME | SUBJECT | QTY')
                    for record in records:
                        idd,n,s,q=record
                        print(idd,n,s,q,sep=' | ')
                elif choice==6:
                    mycursor.execute('Select * from issued')
                    records=mycursor.fetchall()
                    print('BOOKID | NAME | SUBJECT | SID')
                    for record in records:
                        idd,n,s,sid=record
                        print(idd,n,s,sid,sep=' | ')
                    
                elif choice==7:
                    break
        if logged==False:
            print('Either the username or password is incorrect...')
            
    elif ch==2:
        break
    
    
        
    
    




