import mysql.connector
import pandas as pd

con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678')
cursor=con.cursor()
#cursor.execute('drop database redbus')
#print("Database Dropped")
cursor.execute('create database redbus')

cursor.execute('use redbus')

print("Database created")



query="create table bus_routes (id INT AUTO_INCREMENT PRIMARY KEY, route_name text,route_link text,busname text,bustype text,departing_time datetime,duration text,reaching_time datetime,star_rating float, price DECIMAL,seats_available int)"
cursor.execute(query)


print("Table Created")

df = pd.read_excel('output_redbus.xlsx')
query1='''insert into bus_routes (route_name,route_link,busname,bustype,departing_time,duration,reaching_time,
star_rating,price,seats_available)
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
for i in df.values:
    values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])
    cursor.execute(query1, values)
cursor.execute("update bus_routes objects set star_rating=0.0 where star_rating=0")
con.commit()
print("Values inserted")
