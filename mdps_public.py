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

hide_style = """
    <style>
    #GithubIcon {visibility: hidden;}
    #MainMenu {visibility: hidden;}
	Header {visibility: hidden;}
	</style>
"""

tz_thai = pytz.timezone('Asia/Bangkok')
now_thai = datetime.now(tz_thai)
current_time_str = now_thai.strftime("%d/%m/%y time %H:%M minute.")

loaded_model = pickle.load(open('EAtrained_model.sav', 'rb'))

#loaded_model = pickle.load(open('alphabetatrained_model.sav', 'rb'))

# giving a title  
	# st.title('Web for prediction Alpha Thalassemia carrier')   
def main():
#	"""Simple Login App"""
	st.markdown(hide_style, unsafe_allow_html=True)
#st.title("Simple Login App")
	
	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)
	
	if choice == "Home":
		st.subheader("This is Web app for prediction alpha thalassemia carrier")
		st.write('In 2024, From Phrae Adaboost model on Dataset3 demonstrated acc 97% sen 100% spec 95% AUC 0.974. In 2026, A performance evaluation of the adaboost model in the Khon Kaen population showed acc 63% Sen 93.4% Spec 57.4% PPV 30.9% NPV 97.7% AUC 0.754.')
        	
	elif choice == "Login":
		st.subheader("Alpha thalassemia carrier prediction using ML")
		
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
		#if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
		
			if result:
				
				st.success("Logged In as {}".format(username))

				# getting the input data from the user
				col1, col2, col3, col4 = st.columns(4)
				with col1:
			   		AGE = st.text_input('AGE (years)')
				with col2:
			   		HCT = st.text_input('Hematocrit (%)')
				with col3:
		   			HGB = st.text_input('Hemaglobin (g/dl)')
				with col4:
		   			RBC = st.text_input('RBC count(10^6 cells/cumm')
				with col1:
		   			MCV = st.text_input('MCV (fl)')
				with col2:
		   			MCH = st.text_input('MCH (pg)')
				with col3:
		   			MCHC = st.text_input('MCHC (g/dl)')
				with col4:
		   			RDW = st.text_input('RDW (fl)')
				#with col1:
				#	HbA2 = st.text_input('HbA2 (%)')				
				
				# code for Prediction
				diagnosis = ''
    
				# creating a button for Prediction 
        
				if st.button('Prediction result Pls. Click'):        
		   		    
					diagnosis = EA_Alpha_thal_prediction([AGE, HCT, HGB, RBC, MCV, MCH, MCHC, RDW])               
				
				st.success(diagnosis)
				
				#if st.button('Prediction Beta thal. Click'):        
		   		    
				#	diagnosis = EA_Alpha_thal_prediction([AGE, HCT, HGB, RBC, MCV, MCH, MCHC, RDW, HbA2])  
				
				#st.success(diagnosis)
       
				# getting the input data from the user
				
				col1, col2, col3, = st.columns(3)
				with col1:
	  				st.write('Predicted by ..Phrae ADA ML.. ') 
				with col2:
	   				st.write('Reported by ............................ ')   
				with col3:
		   			st.write('Approved by ............................ ')
		   	
				st.write(f"**Date Prediction:** {current_time_str}")	

				#st.title("รายงานผลการทำนาย")
				# สร้างปุ่มพิมพ์หน้าเว็บ
				components.html("""
    			<button onclick="window.parent.print()" style="
	        		background-color: #4CAF50;
    	    		color: white;
        			padding: 10px 24px;
        			border: none;
        			border-radius: 4px;
        			cursor: pointer;
        			font-size: 16px;">
        			🖨️ พิมพ์รายงาน (Print / Save as PDF)
    			</button>
				""", height=60)
		
			else:
 	 			
				st.sidebar.warning("Incorrect Username/Password")

		
	
	elif choice == "SignUp":
		st.subheader("Create an Account")

		new_user = st.text_input('Username')
		new_passwd = st.text_input('Password',type='password')

		if st.button('SignUp'):
		   create_usertable()
		   add_userdata(new_user,make_hashes(new_passwd))
		   st.success("You have successfully created an account.Go to the Login Menu to login")

def EA_Alpha_thal_prediction(input_data):

	# changing the input_data to numpy array
	input_data_as_numpy_array = np.asarray(input_data)

	# reshape the array as we are predicting for one instance
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

	prediction = loaded_model.predict(input_data_reshaped)
	print(input_data_as_numpy_array)
	print(prediction)

	if (prediction[0] == 0):
   	 return 'This person is alpha thalassemia carrier'
	else:
   	   return 'This person is not alpha thalassemia carrier'

# giving a title  
#	st.title('Web for prediction Alpha Thalassemia carrier')   
    
       

				#task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				#if task == "Add Post":
				#	st.subheader("Add Your Post")

				#elif task == "Analytics":
				#	st.subheader("Analytics")
				#elif task == "Profiles":
				#	st.subheader("User Profiles")
				#	user_result = view_all_users()
				#	clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
				#	st.dataframe(clean_db)


if __name__ == '__main__':
	main()


