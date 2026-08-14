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
		
