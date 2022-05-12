from jobs import q, update_status
from hotqueue import HotQueue
import sys
import os
import json

try:
	REDIS_IP = os.environ['REDIS_IP']
except KeyError:
	print("REDIS_IP is required.")
	sys.exit(1)

#q = HotQueue('queue',host=REDIS_IP,port=6379,db=1)

@q.worker
def execute_job(jid):
	update_status(jid,'working')
	key_list = json.loads(rd.get("keys_sol"))["keys_sol"]
	all_substance_composition = {}
	job_dict = json.loads(rd.get(jid))
	substance = str(job_dict['substance'])
	i = 0
	for x in key_list:
		i = i + 1
		all_substance_composition.update({i: json.loads(rd.get(x))})
	rd.set('subs', json.dumps(all_substance_composition))
	percentage_list = []
	for i in range(1, len(key_list)):
		if all_substance_composition[i][substance]:
			percentage = all_substance_composition[i][substance]
			percentage_list.append(percentage)
	max_percentage = float(max(percentage_list))
	container1 = 0
	container2 = 0
	container3 = 0
	container4 = 0
	container5 = 0
	container6 = 0
	container7 = 0
	container8 = 0
	container9 = 0
	container10 = 0
	container11 = 0
	container12 = 0
	container13 = 0
	container14 = 0
	container15 = 0
	container16 = 0
	container17 = 0
	container18 = 0
	container19 = 0
	for i in percentage_list:
		i = float(i)
		if max_percentage*0.05 >= i >= 0:
			container1 = container1 + 1
		if max_percentage*0.1 >= i > max_percentage*0.05:
			container2 = container2 + 1
		if max_percentage*0.15 >= i > max_percentage*0.1:
			container3 = container3 + 1
		if max_percentage*0.2 >= i > max_percentage*0.15:
			container4 = container4 + 1
		if max_percentage*0.25 >= i > max_percentage*0.2:
			container5 = container5 + 1
		if max_percentage*0.3 >= i > max_percentage*0.25:
			container6 = container6 + 1
		if max_percentage*0.35 >= i > max_percentage*0.3:
			container7 = container7 + 1
		if max_percentage*0.4 >= i > max_percentage*0.35:
			container8 = container8 + 1
		if max_percentage*0.45 >= i > max_percentage*0.4:
			container9 = container9 + 1
		if max_percentage*0.5 >= i > max_percentage*0.45:
			container10 = container10 + 1
		if max_percentage*0.55 >= i > max_percentage*0.5:
			container11 = container11 + 1
		if max_percentage*0.6 >= i > max_percentage*0.55:
			container12 = container12 + 1
		if max_percentage*0.65 >= i > max_percentage*0.6:
			container13 = container13 + 1
		if max_percentage*0.7 >= i > max_percentage*0.65:
			container14 = container14 + 1
		if max_percentage*0.75 >= i > max_percentage*0.7:
			container15 = container15 + 1
		if max_percentage*0.8 >= i > max_percentage*0.75:
			container16 = container16 + 1
		if max_percentage*0.85 >= i > max_percentage*0.8:
			container16 = container16 + 1
		if max_percentage*0.9 >= i > max_percentage*0.85:
			container17 = container17 + 1
		if max_percentage*0.95 >= i > max_percentage*0.9:
			container18 = container18 + 1
		if max_percentage >= i > max_percentage*0.95:
			container19 = container19 + 1
		histogram_data = np.array([container1, container2, container3, container4, container5, container6,
								container7, container8, container9, container10, container11, container12,
								container13, container14, container15, container16, container17, container18,
								container19])
	plt.hist(histogram_data, 19)
	plt.show()
	plt.savefig(f'{substance}_concentration.png')
	with open(f'{substance}_concentration.png', 'rb') as f:
		img = f.read()
	rd.hset(str(jid), 'image', img)

	update_status(jid, 'complete')

execute_job()
