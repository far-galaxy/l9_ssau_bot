from mysql.connector import connect
import random

class Database():
	def __init__(self, host, user, password):
		self.database = connect( host = host,
							user = user,
							password = password)
		
		self.cursor = self.database.cursor()
		self.cursor.execute("CREATE DATABASE IF NOT EXISTS l9_lk")
		self.cursor.execute("USE l9_lk")
		
		users_table = """CREATE TABLE IF NOT EXISTS l9_users (
		    l9Id INTEGER PRIMARY KEY,
			vkId INTEGER,
			userName TEXT,
			userSurname TEXT,
			userPhotoUrl TEXT
			);"""
		
		self.cursor.execute(users_table)		
		
	def newID(self):
		l9ID = random.randint(100000000,999999999)
		
		check_id = """SELECT l9Id FROM l9_users
		WHERE l9Id = %s"""
		
		self.cursor.execute(check_id, tuple([l9ID]))
		exist = self.cursor.fetchall() != []
		if not exist:
			return l9ID
		else:
			self.newID()
			
if __name__ == "__main__":
	from vkbot import VKBot
	sql_pass = VKBot.check_file("settings/sql_pass")
	db = Database("localhost","root",sql_pass)
	
	user_query = """
            INSERT IGNORE INTO l9_users
            (l9Id, userName, userSurname)
            VALUES (%s, 'test', 'test')
            """

	db.cursor.execute(user_query, [db.newID()])
	db.database.commit()