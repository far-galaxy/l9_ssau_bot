import requests
from utils import checkFile
from ast import literal_eval

auth_params = {
	'client_id' : checkFile("settings/client_id"),
	'client_secret' : checkFile("settings/client_secret"),
	'redirect_uri' : checkFile("settings/redirect_uri")
}

user_params = {
	'v' : '5.81',
	'fields' :'photo_big'
}


def getAcessToken(code):
	auth_params['code'] = code
	data = requests.get("https://oauth.vk.com/access_token", params = auth_params)	
	if data.status_code == 200:
		return True, data.json()
	else:    
		return False, data.json()["error_description"]	
	
def getUserInformation(data):
	user_params['uids'] = data['user_id']
	user_params['access_token'] = data['access_token']
	data = requests.get("https://api.vk.com/method/users.get", params = user_params)
	if data.status_code == 200:
		d = data.content.decode()
		user_data = literal_eval(d)['response'][0]
		return True, user_data
	
	else:
		return False, user_data