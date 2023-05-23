import mysql.connector
import streamlit as st
import pandas as pd

def add_menu_item(mname, price):
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    csr = mydb.cursor()
    query1 = "select mname from menu"
    csr.execute(query1)
    result = csr.fetchall()
    df = pd.DataFrame(result)
    l = []
    for i in range(len(df)):
        l.append(df.iloc[i][0])
    if mname not in l:
        query = "insert into menu(mname,price) values(%s,%s)"
        val = (mname, price)
        csr.execute(query, val)
        mydb.commit()
        st.success("Menu Added Successfully")
        csr.close()
        mydb.close()
    else:
        st.error("Menu already exists")

def update_menu(id, mname, price):
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    csr = mydb.cursor()
    query = "select mid from menu"
    csr.execute(query)
    result = csr.fetchall()
    df = pd.DataFrame(result)
    l = []
    for i in range(len(df)):
        res = df.loc[i][0]
        l.append(res)
    if id in l:
        sql = "update menu set mname=%s , price=%s where mid=%s"
        val = (mname, price, id)
        csr.execute(sql, val)
        mydb.commit()
        st.success("Menu Updated Successfully")
    else:
        st.error("Menu Id does not exist")
    csr.close()
    mydb.close()


def delete_menu(mid):
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    csr = mydb.cursor()
    flag = False

    csr.execute("select mid from menu")
    result = csr.fetchall()
    for i in result:
        for j in i:
            if mid == j:
                flag = True
    if flag:
        query = "DELETE FROM menu WHERE mid=%s"
        val = (mid,)
        csr.execute(query, val)
        mydb.commit()

        st.success("Menu Deleted Successfully")

    else:
        st.error("Menu Id does not exist")
    csr.close()
    mydb.close()


def display_menu():
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    csr = mydb.cursor()
    csr.execute("SELECT * FROM menu")
    result = csr.fetchall()
    st.write(pd.DataFrame(result, columns=["Menu_Id", "Menu Name", "Price"]).set_index("Menu_Id"))
    mydb.commit()
    csr.close()
    mydb.close()


def order(userid):
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    mycursor = mydb.cursor()
    cid = userid
    q = 'select id from customer'
    mycursor.execute(q)
    res = mycursor.fetchall()
    df=pd.DataFrame(res)
    li = []
    for i in range(len(df)):
        result = df.loc[i][0]
        li.append(result)
    if cid in li:
        mi = st.number_input("Enter the Menu ID of the Dish from Menu", min_value=0)
        if st.button("Order Confirm"):
            query = "select mid from menu"
            mycursor.execute(query)
            result = mycursor.fetchall()
            df = pd.DataFrame(result)
            l = []
            for i in range(len(df)):
                res = df.loc[i][0]
                l.append(res)
            if mi in l:
                query = "insert into orders(cid,mname,price) values(%s,(select mname from menu where mid=%s),(select price from menu where mid=%s))"
                val = (cid, mi, mi)
                mycursor.execute(query, val)
                mydb.commit()
                st.success("Confirm Order")
            else:
                st.error("Menu Id does not exist")
    else:
        st.error('Please Reserve a Table first')
    mycursor.close()
    mydb.close()


def bill(userid):
    cid = userid
    sum = 0
    if st.button("Generate Bill"):
        mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
        mycursor = mydb.cursor()
        val = (cid,)
        query = "select mname,count(mname) as item_count,(count(mname)*price) as total from orders where cid=%s group by mname,price"
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        df = pd.DataFrame(result, columns=["Menu Name", "Quantity", "Total"]).set_index("Menu Name")
        st.write(df)
        mycursor.execute("select price from orders where cid=%s", val)
        total = mycursor.fetchall()
        for i in total:
            for j in i:
                sum += j
        st.write("Total Payable Amount: ", format(float(sum), ".2f"), '\u20B9')

        query1 = 'delete from cust where cid = %s'
        val1 = (cid,)
        mycursor.execute(query1, val1)
        mydb.commit()

        query1 = 'delete from orders where cid = %s'
        val1 = (cid,)
        mycursor.execute(query1, val1)
        mydb.commit()

        query2 = 'delete from customer where id = %s'
        val2 = (cid,)
        mycursor.execute(query2, val2)
        mydb.commit()



def recommendation():
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    mycursor = mydb.cursor()
    # option = st.sidebar.selectbox('Choose option', ['Get Recommendations'])

    if True:
        recommendation = st.selectbox("Have no idea What to order\nWhat's your Hunger Mood ? ",
                                      ['-------- select -------- ', 'Chinese', 'Pasta', 'Frankie', 'Sandwich',
                                       'Burger'])
        if recommendation == 'Chinese':
            sql = "select menu from recommendation where cuisine = %s"
            value = (recommendation,)
            mycursor.execute(sql, value)
            result = mycursor.fetchall()
            df = pd.DataFrame(result)
            for i in range(len(df)):
                st.write(df.loc[i][0])

        if recommendation == 'Pasta':
            sql = "select menu from recommendation where cuisine = %s"
            value = (recommendation,)
            mycursor.execute(sql, value)
            result = mycursor.fetchall()
            df = pd.DataFrame(result)
            for i in range(len(df)):
                st.write(df.loc[i][0])

        if recommendation == 'Frankie':
            sql = "select menu from recommendation where cuisine = %s"
            value = (recommendation,)
            mycursor.execute(sql, value)
            result = mycursor.fetchall()
            df = pd.DataFrame(result)
            for i in range(len(df)):
                st.write(df.loc[i][0])

        if recommendation == 'Sandwich':
            sql = "select menu from recommendation where cuisine = %s"
            value = (recommendation,)
            mycursor.execute(sql, value)
            result = mycursor.fetchall()
            df = pd.DataFrame(result)
            for i in range(len(df)):
                st.write(df.loc[i][0])

        if recommendation == 'Burger':
            sql = "select menu from recommendation where cuisine = %s"
            value = (recommendation,)
            mycursor.execute(sql, value)
            result = mycursor.fetchall()
            df = pd.DataFrame(result)
            for i in range(len(df)):
                st.write(df.loc[i][0])

