from mysql.connector import connect
import random

class Database():
	def __init__(self, host, user, password):
		self.database = connect(host = host,
								user = user,
								password = password)
		self.cursor = self.database.cursor()
	
	def exec(self, query, commit = False):
		self.cursor.execute(query)
		if commit:
			self.database.commit()
		return self.cursor
		
	def initDatabase(self, name):
		self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name}")
		self.cursor.execute(f"USE {name}")		
		
	def initTable(self, name, head):
		query = f"CREATE TABLE IF NOT EXISTS {name} ("
		query += ", ".join([" ".join(i) for i in head])
		query += ");"
		self.exec(query)
		
	def insert(self, name, values):
		query = f"INSERT IGNORE INTO {name} ("
		query += ", ".join(values) + ") VALUES ("
		query += ", ".join(values.values()) + ");"
		self.exec(query, commit = True)
		
	def get(self, name, condition, columns = None):
		query = "SELECT " + (', '.join(columns) if columns != None else "*")
		query += f" FROM {name} WHERE {condition};"
		return self.exec(query)
		
	def newID(self, name, id_name):
		someID = random.randint(100000000,999999999)
		
		result = self.get(name, f"{id_name} = {someID}")
		
		exist = result.fetchall() != []
		if not exist:
			return str(someID)
		else:
			self.newID()	
		
if __name__ == "__main__":
	from vkbot import VKBot
	sql_pass = VKBot.check_file("settings/sql_pass")
	db = Database("localhost","root",sql_pass)
	db.initDatabase("l9_lk")
	db.initTable("l9_users", [
		["l9Id", "INTEGER", "PRIMARY KEY"],
		["vkId", "INTEGER"]
	])
	
	db.insert("l9_users", {
		"l9Id":db.newID("l9_users", "l9Id"), 
		"vkId":"5678"
	})
	
	db.get("l9_users", 
		   "l9Id = 1", 
		   ["l9Id, vkId"]
		   )