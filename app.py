from flask import Flask
from flask import request
import requests
import redis
import json

app = Flask(__name__)

def get_redis_client():
	"""
	Returns redis client object for use in flask app. Hard coded for TACC isp02 port 6379 and lew2547's unique host
	Args:
		none
	Returns:
		redis client object
	"""
	return redis.StrictRedis(host='10.108.182.250',port=6379)

@app.route('/',methods=['GET'])
def hello_world():
	return 'Hello World\n'

@app.route('/data',methods=['GET','POST'])
def data_route():
	"""
	The route has two functions. 
	For a POST request. The function updates the redis database thorugh a python redis server object. 
	For a GET request. The function returns the meteorite landind data loaded from the POST request.
	Args:
		none
	Returns
		if POST: confirmations string
		if GET: json of meteorite landing data 
	"""
	if request.method == 'POST':
		rd = get_redis_client()
		sl = requests.get("https://raw.githubusercontent.com/lukewilson37/coe332-MarsSoilSampleAnalysis/main/initial_sol_list.txt")
		sl_list = list(sl.content.decode('utf-8').split("\n"))
		sl_list.remove("")
		for sol in sl_list:
			sol_info_dict = {}
			sol_info = requests.get("https://"+sol)
			sol_info_list = list(sol_info.content.decode('utf-8').split("\r\n"))
			for i in range(1,len(sol_info_list)):
				sol_info_list_i = sol_info_list[i].replace(" ","").split(",")
				sol_info_dict[sol_info_list_i[0]] = sol_info_list[1]
			rd.set(sol[69:77],sol_info_dict)
		return 'stored'
	else:
		rd = get_redis_client()
		sol_test = rd.get('sol00047')
		return sol_test

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')


