from jobs import q, update_status


@q.worker
def execute_job(jid):
    update_status(jid, 'working')



    update_status(jid, 'complete')