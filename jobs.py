from hotqueue import HotQueue
import redis
import uuid
import os


redis_ip = os.environ.get('REDIS_IP', '127.17.0.3')
q = HotQueue("plot_queue", host=redis_ip, port=6379, db=1)
rd = redis.StrictRedis(host=redis_ip, port=6379, db=0)


def generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())


def save_job(jid, jobd):
    """Save a job in the Redis database."""
    rd.hset(jid, jobd)


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
    if type(jid) == str:
        return {'id': jid,
                'substance': substance,
                'status': status
                }
    return {'id': jid.decode('utf-8'),
            'substance': substance.decode('utf-8'),
            'status': status.decode('utf-8')
            }


def add_job(substance, status="submitted"):
    jid = generate_jid()
    jobd = instantiate_job(jid, status, substance)
    save_job(jid, jobd)
    queue_job(jid)
    return jobd


def update_status(jid, status):
    jobd = rd.hget(jid)
    if jobd:
        jobd['status'] = status
        save_job(jid, jobd)
    else:
        raise Exception()



