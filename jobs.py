from hotqueue import HotQueue
import redis
import uuid
import json
import os

redis_ip = os.environ.get('REDIS_IP')


q = HotQueue("plot_queue", serializer=None, host=redis_ip, port=6379, db=1)

rd = redis.Redis(host=redis_ip, port=6379, db=0)


def generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())



def save_job(jid, jobd):
    """Save a job in the Redis database."""
    rd.set(jid, json.dumps(jobd))


def queue_job(jid):
    """
    add job to queue
    """
    q.put(jid)


def instantiate_job(jid, substance, status):
    """
    Create the job object description as a python dictionary.

    :param: jid - unique id for job
    :param: substance - substance user wants data about
    :param: status - the status of the job
    """
    return {'id': jid,
            'substance': substance,
            'status': status
            }


def add_job(substance, status="submitted"):
    jid = generate_jid()
    jobd = instantiate_job(jid, str(substance), status)
    save_job(jid, jobd)
    queue_job(jid)
    return jobd


def update_status(jid, status):
    jobd = json.loads(rd.get(jid))
    if jobd:
        jobd['status'] = status
        save_job(jid, jobd)
    else:
        raise Exception()


def check_status(jid):
    job_dict = json.loads(rd.get(jid))
    return job_dict['status']


