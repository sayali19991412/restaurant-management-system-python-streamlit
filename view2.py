import streamlit as st
import pandas as pd
import mysql.connector
import restman as rm
from streamlit_lottie import st_lottie
import requests

headerSection = st.container()
customerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
newUserSection = st.container()

# connect to the database
mydb = mysql.connector.connect(user='sayali', password='sayali', host='localhost', database='project')
csr = mydb.cursor()
print("Connection Established")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_login_page_admin():
    with loginSection:
        st.subheader("Admin Login")
        if st.session_state['loggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="Enter your user id")
            password = st.text_input(label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_Clicked, args=(userName, password))


def show_login_page_cust():
    with loginSection:
        st.subheader("Customer Login")
        if st.session_state['cusloggedIn'] == False:
            userName = st.text_input(label="", value="", placeholder="Enter your Username")
            password = st.text_input(label="", value="", placeholder="Enter password", type="password")
            st.button("Login", on_click=LoggedIn_ClickedCust, args=(userName, password))


def show_role():
    option = st.sidebar.selectbox(
        'Choose your role', ['----select----', 'Admin', 'Customer', 'New User'])
    if option == 'Admin':
        show_login_page_admin()
        lottie_url = "https://assets1.lottiefiles.com/packages/lf20_SPA6bgo7nO.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json, width=200)
    elif option == 'Customer':

        show_login_page_cust()
        lottie_url = "https://assets10.lottiefiles.com/packages/lf20_bo8vqwyw.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json, width=200)
    elif option == 'New User':

        newUser()
        lottie_url = "https://assets9.lottiefiles.com/packages/lf20_bqnjxnmy.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json, width=200)
    else:
        pass


def LoggedIn_Clicked(userName, password):
    if authenticate(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")


def LoggedIn_ClickedCust(userName, password):
    if custauthenticate(userName, password):
        st.session_state['cusloggedIn'] = True
        st.session_state['username'] = userName
    else:
        st.session_state['cusloggedIn'] = False
        st.error("Invalid user name or password")


def authenticate(userName, password):
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    csr = mydb.cursor()
    sql = "select password from admin where aid = %s"
    val = (userName,)
    csr.execute(sql, val)
    passw = csr.fetchall()
    if passw[0][0] == password:
        return True
    else:
        return False


def custauthenticate(userName, password):
    mydb = mysql.connector.connect(host="localhost", user="sayali", password="sayali", database="project")
    csr = mydb.cursor()
    sql = "select password from cust where cid = %s"
    val = (userName,)
    csr.execute(sql, val)
    passw = csr.fetchall()
    if passw[0][0] == password:
        return True
    else:
        return False


def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['cusloggedIn'] = False


def show_main_page():
    with mainSection:
        tab1, tab2, tab3, tab4 = st.tabs(['Add menu ➕', 'Update Menu 📝', 'Delete Menu ❌', 'Display Menu 💻'])
        with tab1:
            lottie_url = "https://assets6.lottiefiles.com/packages/lf20_xuy0dq4j.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=150)
            mname = st.text_input("Enter menu iTem").title()
            price = st.text_input("Price")
            menu_button = st.button("Add menu")
            if menu_button:
                rm.add_menu_item(mname, price)
        with tab2:
            lottie_url = "https://assets6.lottiefiles.com/private_files/lf30_rzhdjuoe.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=150)
            id = st.number_input("Enter MenuId to Update", min_value=1)
            name = st.text_input("Enter New Menu Name").title()
            price = st.text_input("Enter New Price")
            if st.button("Update Menu"):
                rm.update_menu(id, name, price)
        with tab3:
            lottie_url = "https://assets2.lottiefiles.com/packages/lf20_VmD8Sl.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=200)
            id = st.number_input("Enter Menu Id to delete ", min_value=1)
            if st.button("Delete"):
                rm.delete_menu(id)
        with tab4:
            lottie_url = "https://assets7.lottiefiles.com/packages/lf20_3GIrwN3h0z.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=200)
            rm.display_menu()


def cust_page():
    with customerSection:
        option = st.sidebar.selectbox('Select an option',['Reserve a Table', 'Order', 'Bill','Get Recommendations','Feedback'])
        if option == 'Reserve a Table':
            st.subheader("Reserve a table for Customer")
            lottie_url = "https://assets5.lottiefiles.com/packages/lf20_29xm3xgf.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=200)
            csid = st.session_state['username']
            name1 = st.text_input("Enter Name")
            phone = st.text_input("Enter contact details")
            tablepref = st.selectbox("Select AC/NON-AC Table", ['AC', 'NONAC'])
            if st.button("Book A Table"):
                query = "insert into customer(id,name,phone,tablepref) values(%s,%s,%s,%s)"
                val = (csid, name1, phone, tablepref)
                csr.execute(query, val)
                mydb.commit()
                st.success("Your Table Has been Booked")
        if option == 'Order':
            lottie_url = "https://assets4.lottiefiles.com/packages/lf20_jmd7aruv.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=200)
            rm.display_menu()
            rm.order(st.session_state['username'])
        if option == 'Bill':
            lottie_url = "https://assets10.lottiefiles.com/packages/lf20_2K2lEIcWwq.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=200)
            rm.bill(st.session_state['username'])
        if option == 'Get Recommendations':
            lottie_url = "https://assets4.lottiefiles.com/packages/lf20_9ti102vm.json"
            lottie_json = load_lottieurl(lottie_url)
            st_lottie(lottie_json, width=200)
            rm.recommendation()

        if option == 'Feedback':
            st.write(
                "Our Restaurant pays excellent care and consideration towards providing with the best food and table service."
                " We would appreciate your time in our Customer Satisfaction Survey . I appreciate your Support !!")

            st.subheader("Food Quality")

            fq = st.slider('Food Freshness', 1, 5, 1)
            md = st.slider('Menu Diversity', 1, 5, 1)

            st.subheader('Service Quality')

            rt = st.slider('Response Time of the Staff', 1, 5, 1)
            ps = st.slider('Politeness of the Staff', 1, 5, 1)

            submit = st.button('Submit Feedback')
            if submit:
                st.success('Thank You For Your Feedback !!! ')

def newUser():
    with newUserSection:
        st.subheader("New User Registration")
        name = st.text_input("Enter Your Name")
        cid = st.text_input("Enter your Customer ID")
        phone = st.number_input("Enter Your Phone NUmber", min_value=0)
        password = st.text_input("Enter Your Password")
        if st.button("Register"):
            csr.execute("insert into cust(cid,phone,cname,password) values(%s,%s,%s,%s)", (cid, phone, name, password))
            mydb.commit()
            st.success("User Created")


with headerSection:
    st.title("Restaurant Management System")
    if 'loggedIn' not in st.session_state and 'cusloggedIn' not in st.session_state and 'newuserId' not in st.session_state:
        st.session_state['loggedIn'] = False
        st.session_state['cusloggedIn'] = False
        st.session_state['newuserId'] = False
        lottie_url = "https://assets6.lottiefiles.com/packages/lf20_Eh4ZBX.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json)
        show_role()
    else:
        if st.session_state['loggedIn']:  # admin , cust .. log in --> cust
            show_logout_page()
            show_main_page()
        elif st.session_state['cusloggedIn']:
            show_logout_page()
            cust_page()

        else:
            show_role()




