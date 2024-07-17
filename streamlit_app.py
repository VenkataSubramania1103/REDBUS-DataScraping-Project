import streamlit as st
import mysql.connector
import pandas as pd

con=mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678')
cursor=con.cursor()
cursor.execute("use redbus")


df=pd.read_excel("output_redbus.xlsx")
st.header('REDBUS DataScraping Project :bus:')
route_name=['All']
for i in df['Bus Route Name'].drop_duplicates():
    route_name.append(i)
name=st.selectbox("Enter route name:",route_name)

bus_type=['All']
for i in df['Bus Type'].drop_duplicates():
    bus_type.append(i)
type=st.selectbox("Select bus type:",bus_type)

seats=['=All','<10','>10','>20','>30','>40','>50']
seats_ava=st.selectbox("Select the number of seats required:",seats)


cost=['=All','<1000','>1000','>2000','>3000']
price=st.selectbox("Select the bus Price:",cost)

query1=f"select * from bus_routes where route_name='{name}' and price{price} and seats_available{seats_ava} and bustype='{type}';"
if('=All' in query1):
    query1=query1.replace('=All',' is not null')
if('All' in query1):
    query1=query1.replace("='All'",' is not null')

cursor.execute(query1)
rows=cursor.fetchall()
df1=pd.DataFrame(rows,columns=['Id','Bus Route Name','Bus route link','Bus Name','Bus Type','Departing time','Duration','Reaching Time','Rating','Price','Seats available'])
st.header("Bus Details as per filter")
st.dataframe(df1,use_container_width=True, hide_index=True)