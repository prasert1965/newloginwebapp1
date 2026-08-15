# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
	 
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# You can also use the verify functions of the various libraries for the same purpose
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pytz
import datetime
import tempfile
from fpdf import FPDF
import streamlit.components.v1 as components
from datetime import datetime
tz_thai = pytz.timezone('Asia/Bangkok')
now_thai = datetime.now(tz_thai)
current_time_str = now_thai.strftime("%d/%m/%y time %H:%M minute.")
loaded_model = pickle.load(open('EAtrained_model.sav', 'rb'))

def main():
#	"""Simple Login App"""

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("This is Web app for prediction alpha thalassemia carriers")
		st.write('In 2024, From Phrae Adaboost model on Dataset3 demonstrated acc 97% sen 100% spec 95% AUC 0.974. In 2026, A performance evaluation of the adaboost model in the Khon Kaen population showed acc 63% Sen 93.4% Spec 57.4% PPV 30.9% NPV 97.7% AUC 0.754.')

	elif choice == "Login":
		st.subheader("Login Section")
		
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				if task == "Add Post":
					st.subheader("Add Your Post")

				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

	elif choice == "SignUp":
		st.subheader("Create an Account")

		new_user = st.sidebar.text_input('Username')
		new_passwd = st.sidebar.text_input('Password',type='password')

		if st.sidebar.button('SignUp'):
		   create_usertable()
		   add_userdata(new_user,make_hashes(new_passwd))
		   st.success("You have successfully created an account.Go to the Login Menu to login")

if __name__ == '__main__':
	main()
