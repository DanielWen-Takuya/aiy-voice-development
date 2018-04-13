#!/usr/bin/python
import psycopg2, datetime

"""
PostgreServer class can connect to the database and execute SQL command.
It has following functions : 
- Save and read the actions of button/audio
- Save and read the detection details
- Read the list of music
- Check the information for authentification
- Save and read the demand from app
"""
class PostgreServer(object):
	def __init__(self,pwd):
		self.pwd = pwd
		self.conn = None
	
	def connect(self):
		command_conn = 'dbname=aiy user=postgres password=%s' % self.pwd
		self.conn = psycopg2.connect(command_conn)
		
	def close(self):
		if self.conn is not None:
			self.conn.close()
			self.conn = None
		else
			print('Database close already')
	
	"""Test use"""
	def execute(self,command):
		with self.conn:
			with self.conn.cursor() as curs:
				curs.execute(command)
				result = curs.fetchone()
		
		return result
		
	def read_music_list(self):
		command_read_music_list = 'SELECT * FROM list_music'
		return self.execute(command_read_music_list)
		
	def save_action_button(self, action_time, question=None, answer=None, success_read, success_answer):
		command_save_action_button = 'INSERT INTO action_button VALUES (DEFAULT,%s,%s,%s,%s,%s)' % (action_time, question, answer, success_read, success_answer)
		self.execute(command_save_action_button)
		
	def read_total_button(self):
		command_read_total_button = 'SELECT count(*) FROM action_button'
		return self.execute(command_read_music_list)
		
	def save_detect_human(self,detect_time,is_detected,error=None):
		command_save_detect_human = 'INSERT INTO detect_human VALUES (DEFAULT,%s,%s,%s)' % (detect_time, is_detected, error)
		self.execute(command_save_detect_human)
		
	def save_demand_app(self,demand_time,demand,response=None,user_id):
		command_save_demand_app = 'INSERT INTO demand_app VALUES (DEFAULT,%s,%s,%s,%s)' % (user_id, demand_time, demand, response)
		self.execute(command_save_demand_app)
	
	def add_auth_user(self,role_id,user_fname,user_lname,pwd,active=True,e_mail,user_description=None):
		command_add_auth_user = 'INSERT INTO auth_user VALUES (DEFAULT,%s,%s,%s,%s,%s,%s)' % (user_fname, user_lname, pwd,active,e_mail,user_description)
		#todo : check already exist?
		self.execute(command_add_auth_user)
		command_get_user_id = 'SELECT user_id FROM auth_user WHERE e_mail = %s' % e_mail
		user_id = self.execute(command_get_user_id)

		creation_time = datetime.datetime.now()
		expiration_time = creation_time + datetime.datetime(0,1,1)
		command_add_user_role = 'INSERT INTO auth_user_role VALUES (%s,%s,%s,%s)' % (user_id,role_id,creation_time,expiration_time)
		self.execute(command_add_user_role)
		
	'''
	Check the authentification to enter
	Error 100 : E-mail not exist or password wrong
	Error 101 : Already log in, not for twice
	'''	
	'''password need to be more secure'''
	def check_auth_enter(self,e_mail,user_pwd):
		command_check_auth_enter = 'SELECT user_id FROM auth_user WHERE e_mail = %s AND pwd = %s' % (e_mail,user_pwd)
		user_id = self.execute(command_check_auth_enter)
		if user_id is not None:
			user_id = user_id[0]
			command_check_auth_enter = 'SELECT * FROM connection_status WHERE user_id = %s' % user_id
			result = self.execute(command_check_auth_enter)
			if result is None:
				print('%s can enter' % user_id)
				return (True,user_id)
			else
				print('%s has already logged in, please not log in twice' % user_id)
				return (False,101)
		else
			print('%s not exist or password wrong' % e_mail)
			return (False,100)
	
	'''
	Check the role so as to access functions
	Error 102 : given user id not exist in the auth_user_role table
	'''	
	def check_auth_role(self,user_id):
		command_check_auth_role = 'SELECT r.role_name FROM auth_role AS r, auth_user_role AS ur WHERE r.role_id = ur.role_id AND ur.user_id = %s' % user_id
		role_name = self.execute(command_check_auth_role)
		if role_name is not None:
			role_name = role_name[0]
			print('%s : %s' % (user_id, role_name))
			return (True,role_name)
		else
			print('Unknown error : user_id not in auth_user_role')
			return (False,102)
			
#do some test in shell