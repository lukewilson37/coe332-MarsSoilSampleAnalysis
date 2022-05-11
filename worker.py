import matplotlib.pyplot as plt
import json
from jobs import q, update_status
import redis


rd = redis.Redis(host="172.17.0.5", port=6379, db=0)


@q.worker
def execute_job(jid):
    update_status(jid, 'working')
    key_list = json.loads(rd.get("sol_key"))["sol_key"]
    substance_composition = {}
    job_dict = json.loads(rd.get(jid))
    substance = job_dict['substance']
    for sol in key_list:
        substance_composition.update(json.loads(rd.get(sol)))
    update_status(jid, 'complete')


execute_job()
