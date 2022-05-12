import matplotlib.pyplot as plt
import json
from jobs import q, update_status
import redis
import numpy as np

rd = redis.Redis(host="172.17.0.4", port=6379, db=0)


@q.worker
def execute_job(jid):
    update_status(jid, 'working')
    key_list = json.loads(rd.get("sol_key"))["sol_key"]
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
    plt.savefig('concentration.png')
    with open('concentration.png', 'rb') as f:
        img = f.read()
    rd.hset(f'{jid}_plot', 'image', img)
    update_status(jid, 'complete')


execute_job()
