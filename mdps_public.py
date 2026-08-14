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

elif choice == "SignUp":
       st.subheader("Create an Account")
	new_user = st.text_input('Username')
	new_passwd = st.text_input('Password',type='password')
	if st.button('SignUp'):
		create_usertable()
		add_userdata(new_user,make_hashes(new_passwd))
		st.success("You have successfully created an account.Go to the Login Menu to login")
		
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# You can also use the verify functions of the various libraries for the same purpose
elif choice == "Login":
		user = st.sidebar.text_input('Username')
		passwd = st.sidebar.text_input('Password',type='password')
		if st.sidebar.checkbox('Login') :
			create_usertable()
			hashed_pswd = make_hashes(passwd)
			result = login_user(user,check_hashes(passwd,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(user))

				# Tasks For Only Logged In Users
				task = st.selectbox('Select Task',['Add Posts','Manage Blog','Profile'])
				if task == "Add Posts":
					st.subheader("Add Articles")
					....
