from jobs import q, update_status
from hotqueue import HotQueue
import sys
import os
import json
import redis
import numpy as np
import matplotlib.pyplot as plt

try:
	REDIS_IP = os.environ['REDIS_IP']
except KeyError:
	print("REDIS_IP is required.")
	sys.exit(1)

redis_ip = os.environ.get('REDIS_IP')
rd = redis.Redis(host=redis_ip, port=6437, db=0)

@q.worker
def execute_job(jid):
	update_status(jid,'working')
	key_list = json.loads(rd.get("keys_sol"))["keys_sol"]
	all_substance_composition = {}
	job_dict = json.loads(rd.get(jid))
	substance = str(job_dict['substance'])
	c = 0
	for x in key_list:
		c = c + 1
		all_substance_composition.update({c: json.loads(rd.get(x))})
	rd.set('subs', json.dumps(all_substance_composition))
	percentage_list = []
	for j in range(1, c):
		percentage = all_substance_composition[j][substance]
		percentage_list.append(percentage)
	max_percentage = float(max(percentage_list))
	percentage_list = [float(item) for item in percentage_list]
	hi = np.asarray(percentage_list)
	rd.set('plist', json.dumps({'plist': percentage_list}))
	plt.hist(hi, bins=19)
	plt.xlabel("Composition Percentage")
	plt.ylabel("Number of Samples")
	plt.title(f'{substance} Composition Percentages Frequencies')
	plt.savefig('concentration.png')
	with open('concentration.png', 'rb') as f:
		img = f.read()
	rd.hset(f'{jid}_plot', 'image', img)
	update_status(jid, 'complete')	


execute_job()
