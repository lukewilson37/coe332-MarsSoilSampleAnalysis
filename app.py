from flask import Flask
from flask import request, send_file
import requests
import redis
import json
from jobs import add_job, check_status


app = Flask(__name__)


def get_redis_client():
    """
	Returns redis client object for use in flask app. Hard coded for TACC isp02 port 6379 and lew2547's unique host
	Args:
	none
	Returns:
	redis client object
	"""
    return redis.Redis('172.17.0.5', port=6379, db=0)


@app.route('/', methods=['GET'])
def hello_world():
    return '\n Welcome to the Mars Soil Sample Analysis Application\n'


@app.route('/data', methods=['GET', 'POST'])
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
    keylist = []
    if request.method == 'POST':
        rd = get_redis_client()
        sl = requests.get(
            "https://raw.githubusercontent.com/lukewilson37/coe332-MarsSoilSampleAnalysis/main/initial_sol_list.txt")
        sl_list = list(sl.content.decode('utf-8').split("\n"))
        sl_list.remove("")
        for sol in sl_list:
            sol_info_dict = {}
            sol_info = requests.get("https://" + sol)
            sol_info_list = list(sol_info.content.decode('utf-8').split("\r\n"))
            sol_info_list.remove("")
            for i in range(1, len(sol_info_list)):
                sol_info_list_i = sol_info_list[i].replace(" ", "").split(",")
                sol_info_dict[sol_info_list_i[0]] = sol_info_list_i[1]
            rd.set(sol[69:77], json.dumps(sol_info_dict))
            keylist.append(sol[69:77])
            rd.set('sol_key', json.dumps({'sol_key': keylist}))
        return 'stored'
    else:
        rd = get_redis_client()
        sol_test = rd.get('sol00047')
        return sol_test


@app.route('/abundancies/<solname>', methods=['GET'])
def return_sol_data(solname):
    rd = get_redis_client()
    sol_data_raw = rd.get(solname)
    sol_data_json = json.loads(sol_data_raw)
    return sol_data_raw


@app.route('/jobs/<substance>', methods=['POST'])
def job_creator(substance):
    """
    application route to create new job. This route accepts a substance input by the user in the URL
    :param: substance
    """
    add_job(substance)
    return add_job(substance)


@app.route('/jobs/results/<id>', methods=['GET'])
def job_results(id):
    """
    application route to return the results of a completed job.
    :param id:
    :return: histogram image produced by the worker
    """
    rd = get_redis_client()
    path = f'/app/{id}.png'
    with open(path, 'wb') as f:
        f.write(rd.hget(str(id), 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
