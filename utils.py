import os
from hashlib import md5

def checkFile(file):
	"""Checking and loading information from file.
	Useful for keeping tokens and other properties

	Args:
		file: path of file

	Returns:
		str: A content of file
	"""   

	if len(file.split("/")) > 1:
		f = file.split("/")[-1]
		path = os.path.abspath(file.split("/")[-2])+f"/{f}.txt"
	else:
		path = f"{file}.txt"

	if os.path.exists(f"{path}"):
		with open(f"{path}", "r", encoding="utf-8") as f:
			info = f.read()

	else:
		info = input(f"{file} file not found. Please type {file} now:")
		file = open(f"{path}", "w")
		file.write(info)
		file.close()
	return info

def hashMD5(string):
	return md5(string.encode('utf-8')).hexdigest()