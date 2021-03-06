from flask import Flask
from flask import request, send_file
import requests
import redis
import json
from jobs import add_job,check_status


app = Flask(__name__)

def get_redis_client():
	"""
	Returns redis client object for use in flask app. Hard coded for TACC isp02 port 6379 and lew2547's unique host
	Args:
		none
	Returns:
		redis client object
	"""
	return redis.StrictRedis(host='10.108.182.250',port=6437)

# TEST ROUTE
@app.route('/',methods=['GET'])
def hello_world():
	return 'Welcome to Mars Soil Sample Analysis Application\n'

# INITIALIZE DATABASE
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
		sl = requests.get("https://raw.githubusercontent.com/lukewilson37/coe332-MarsSoilSampleAnalysis/main/source/initial_sol_list.txt")
		sl_list = list(sl.content.decode('utf-8').split("\n"))
		sl_list.remove("")
		for sol in sl_list:
			sol_info_dict = {}
			sol_info = requests.get("https://"+sol)
			sol_info_list = list(sol_info.content.decode('utf-8').split("\r\n"))
			sol_info_list.remove("")
			for i in range(1,len(sol_info_list)):
				sol_info_list_i = sol_info_list[i].replace(" ","").split(",")
				sol_info_dict[sol_info_list_i[0]] = sol_info_list_i[1]
			rd.set(sol[69:77],json.dumps(sol_info_dict))
		template_sol = json.loads(rd.get(rd.keys(pattern="sol*")[0]))
		for key in template_sol.keys():
			template_sol[key] = 0
		rd.set('template_sol',json.dumps(template_sol))
		return 'stored'
	else:
		rd = get_redis_client()
		sol_test = rd.get('sol00047')
		return sol_test

# INITIALIZE/UPDATE LIST OF SOL_KEYS
@app.route('/set_sol_list',methods=['GET'])
def get_sol_list():
	"""
	This route generates and updates the list of sol values, such that they are iterable for future use.
	"""
	rd = get_redis_client()
	keys_sol = []
	for sol_key in rd.keys(pattern="sol*"):
		keys_sol.append(sol_key.decode('utf-8'))
	rd.set('keys_sol',json.dumps({'keys_sol':keys_sol}))
	return "sol list updated\n"

### CRUD OPERATIONS ---------------------------------------------------------------------

# CREATE EMPTY SOL
@app.route('/create/<sol_key>',methods=['POST'])
def create_empty_sol_route(sol_key):
	"""
	This route creates an empty sol data sample. Dictionary Template is provided and percentages are preset to zero
	"""
	rd = get_redis_client()
	if rd.get(sol_key):
		return 'sol already exists.\n'
	rd.set(sol_key,rd.get('template_sol'))
	return str(sol_key) + ' created!\n'

# READ SOL DATA
@app.route('/read/<sol_key>',methods=['GET'])
def return_sol_data(sol_key):
	""" 
	This route prints the data from the requested sol sample.
	Args: sol_key (string)
	Returns: associates sol data (json dictionary)
	"""
	rd = get_redis_client()
	if not rd.get(sol_key):
		return 'key does not exist.\n'
	sol_data_raw = rd.get(sol_key)
	sol_data_json = json.loads(sol_data_raw)
	return sol_data_json

# UPDATE SOL DATA
@app.route('/update/<sol_key>/<element>/<value>',methods=['POST'])
def update_sol_data_route(sol_key,element,value):
	"""
	This route updated a value in a sol sample's data.
	Args:
		sol_key (str)
		element (str)
		value (float)
	Returns
		confirmation message
	"""
	rd = get_redis_client()
	if not rd.get(sol_key):
		return 'key does not exist.\n'
	sol_dict = json.loads(rd.get(sol_key))
	sol_dict[element] = float(value)
	rd.set(sol_key,json.dumps(sol_dict))
	return sol_key + ' updated!\n'
	

# DELETE SOL FROM DATABASE
@app.route('/delete/<sol>',methods=['POST'])
def delete_sol_route(sol):
	"""
	application route to delete a key.
	arguments: key value (str)
	return: success or failure (str)
	"""
	rd = get_redis_client()
	if not rd.get(sol):
		return "key does not exist\n"
	rd.delete(sol)
	return "key successfully removed\n"

### JOB ROUTES -------------------------------------------------------------

# RETURN RESULTS ROUTE
@app.route('/jobs/results/<jid>', methods=['GET'])
def job_results(jid):
    """
    application route to return the results of a completed job.
    :param id:
    :return: histogram image produced by the worker
    """
    rd = get_redis_client()
    path = f'/app/' + str(jid) + '.png'
    with open(path, 'wb') as f:
        f.write(rd.hget(str(jid)+'_plot', 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)

# REQUEST JOB ROUTE
@app.route('/jobs/request/<substance>', methods=['POST'])
def job_creator(substance):
    """
    application route to create new job. This route accepts a substance input by the user in the URL
    :param: substance
    """
    #add_job(substance)
    return add_job(substance)

# RETURN JOB STATUS
@app.route('/jobs/status/<job_id>',methods=['GET'])
def check_status_route(job_id):
	"""
	application route to check job status
	arguments: job id (string)
	returns: status (string)
	"""
	return check_status(job_id)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
	

