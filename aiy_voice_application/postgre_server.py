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
		command_conn = 'dbname=aiy user=postgres password=\'%s\'' % self.pwd
		#print(command_conn)
		self.conn = psycopg2.connect(command_conn)
		
	def close(self):
		if self.conn is not None:
			self.conn.close()
			self.conn = None
		else:
			print('Database close already')
	
	"""Test use, for execute sql command"""	
	def execute(self,command,isSelect=False):
		result = []
		with self.conn:
			with self.conn.cursor() as curs:
				try:
					curs.execute(command)
					if isSelect:
						result = curs.fetchall()
						if len(result) == 0 :
    							return ('None',result)
					return ('Ok',result)
				except psycopg2.Error as e:
					error = e.pgerror
					print(error)
					result.append(['Error',error])
					return ('Error',result)
		return ('Error',result)
		
	#return the whole music list in database
	#return: ('Ok',[(1,'name','mp3','music')])
	def read_music_list(self):
		command_read_music_list = 'SELECT * FROM list_music;'
		return self.execute(command_read_music_list,isSelect=True)
	
	#save the action of button with action time and commands
	#action_time=datetime.datetime.now()
	#return:('Ok',[])
	def save_action_button(self, action_time, success_read, success_answer, question='NULL', answer='NULL'):
		command_save_action_button = 'INSERT INTO action_button VALUES (DEFAULT,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (action_time, question, answer, success_read, success_answer)
		return self.execute(command_save_action_button)
		
	#return the total number of actions button
	#return:return:('Ok',[(1,)])
	def read_total_button(self):
		command_read_total_button = 'SELECT count(*) FROM action_button;'
		return self.execute(command_read_total_button,isSelect=True)
	
	#use with a human detector
	#return:('Ok',[])
	def save_detect_human(self,detect_time,is_detected,error=False):
		command_save_detect_human = 'INSERT INTO detect_human VALUES (DEFAULT,\'%s\',\'%s\',\'%s\');' % (detect_time, is_detected, error)
		return self.execute(command_save_detect_human)
	
	#save a demand from app
	#return:('Ok',[])
	def save_demand_app(self,demand_time,demand,user_id,response='NULL'):
		command_save_demand_app = 'INSERT INTO demand_app VALUES (DEFAULT,\'%s\',\'%s\',\'%s\',\'%s\');' % (user_id, demand_time, demand, response)
		return self.execute(command_save_demand_app)
	
	#add an other user
	#return:('Ok',[])
	def add_auth_user(self,role_id,user_fname,user_lname,pwd,e_mail,active=True,user_description='NULL'):
		command_add_auth_user = 'INSERT INTO auth_user VALUES (DEFAULT,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (user_fname, user_lname, pwd,active,e_mail,user_description)
		result = self.execute(command_add_auth_user)
		#check already exist 
		if result[0] == 'Ok':
			command_get_user_id = 'SELECT user_id FROM auth_user WHERE e_mail = \'%s\';' % e_mail
			user_id = self.execute(command_get_user_id,isSelect=True)
			#print(user_id[1])
			if user_id[0] == 'Ok':
				user_id = user_id[1][0][0]
				creation_time = datetime.datetime.now()
				expiration_time = creation_time + datetime.timedelta(days=30)
				command_add_user_role = 'INSERT INTO auth_user_role VALUES (%s,\'%s\',\'%s\',\'%s\');' % (user_id,role_id,creation_time,expiration_time)
				return self.execute(command_add_user_role)
			else: #('Error',reason)
				return ('Error',user_id[0])
		else: #('Error',reason)
			print('E_mail has already been used')
			command_delect_user = 'DELECT FROM auth_user WHERE e_mail = \'%s\';' % e_mail
			self.execute(command_delect_user)
			return ('Error',result[0])
		
	'''
	Check the authentification to enter
	'''	
	'''password need to be more secure'''
	#return ('Ok',user_id)
	def check_auth_enter(self,e_mail,user_pwd,user_ip):
		command_check_auth_enter = 'SELECT user_id FROM auth_user WHERE e_mail = \'%s\' AND pwd = \'%s\';' % (e_mail,user_pwd)
		user_id = self.execute(command_check_auth_enter,isSelect=True)
		if user_id[0] == 'Ok':
			user_id = user_id[1][0][0]
			print('user_id: %s' % user_id)
			command_check_expiration = 'SELECT * FROM auth_user_role WHERE user_id = \'%s\' AND expiration_time > \'%s\';' % (user_id,datetime.datetime.now())
			result = self.execute(command_check_auth_enter,isSelect=True)[0]
			print(result)
			if result == 'Ok':
				command_connection_status = 'INSERT INTO connection_status VALUES (DEFAULT,\'%s\',\'%s\',\'ACTIVE\');' % (user_id,user_ip)
				result = self.execute(command_connection_status)
				if result[0] == 'Ok':
					print('%s can enter' % user_id)
					return ('Ok',user_id)
				else:#'Error'
					error = result[0]
					if error == 'Error':#need to be found
						print('%s has already logged in, please not log in twice' % user_id)
					else:
						print('Error in execution')
					return ('Error',error)
			else:
				print('Time expired')
				return('Error',user_id)
		else:
			print('%s not exist or password wrong' % e_mail)
			return ('Error',user_id[0])
			
	'''Delete connection when log out'''
	#return ('Ok',user_id)
	def delete_connection(self,user_id):
		command_delect_connection = 'DELETE FROM connection_status WHERE user_id = \'%s\';' % user_id
		result = self.execute(command_delect_connection)
		if result[0] == 'Ok':
			print('%s log out with success' % user_id)
			return ('Ok',user_id)
		else:#'Error'
			return ('Error',result[0])
	
	'''
	Check the role so as to access functions
	'''	
	#return ('Ok','visitor') #admin,collab,visitor
	def check_auth_role(self,user_id):
		command_check_auth_role = 'SELECT r.role_name FROM auth_role AS r, auth_user_role AS ur WHERE r.role_id = ur.role_id AND ur.user_id = \'%s\';' % user_id
		role_name = self.execute(command_check_auth_role,isSelect=True)
		if role_name[0] == 'Ok':
			role_name = role_name[1][0][0]
			print('%s : %s' % (user_id, role_name))
			return ('Ok',role_name)
		elif role_name[0] == 'None':
			print('Unknown error : user_id not in auth_user_role')
			return ('Error',role_name[0])
		else:
			print('Error in execution')
			return ('Error',role_name[0])
			
#do some test in shell