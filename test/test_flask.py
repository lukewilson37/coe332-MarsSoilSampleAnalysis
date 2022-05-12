import pytest, requests
import redis

REDIS_IP = '10.108.182.250'
REDIS_PORT = 6437
FLASK_ADDRESS = '10.108.203.190:5037'

def test_flask_running():
	responce = requests.get('http://' + FLASK_ADDRESS + '/')
	assert responce.status_code == 200

def test_redis_database():
	rd = redis.StrictRedis(host=REDIS_IP,port=REDIS_PORT)
	assert len(rd.keys()) > 0

#def test_worker
