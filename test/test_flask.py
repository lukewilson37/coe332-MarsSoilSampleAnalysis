import pytest, requests
import redis

REDIS_IP = '10.108.182.250'
REDIS_PORT = 6437
FLASK_ADDRESS = '10.108.203.190:5037'

def test_flask_running():
	responce = requests.get('http://' + FLASK_ADDRESS + '/')
	assert responce.status_code == 200

def test_redis_database_running():
	rd = redis.StrictRedis(host=REDIS_IP,port=REDIS_PORT)
	assert len(rd.keys()) > 0

def test_create_operation():
	rd = redis.StrictRedis(host=REDIS_IP,port=REDIS_PORT)
	requests.post('http://' + FLASK_ADDRESS + '/create/sol00069 ')
	responce = requests.get('http://' + FLASK_ADDRESS + '/read/sol00069 ')
	assert responce.content != b'key does not exist.\n'

def test_worker_received_queue():
	rd = redis.StrictRedis(host=REDIS_IP,port=REDIS_PORT)
	responce = requests.post('http://' + FLASK_ADDRESS + '/jobs/request/Cl ')
	responce = requests.get('http://' + FLASK_ADDRESS + '/jobs/status/' + json.loads(responce.content.decode('utf-8'))['id'] + ' ')
	assert responce.content != b'submitted\n'




