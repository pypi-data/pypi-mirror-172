import celery
import redis
from redis.client import Redis

LOG_KEY_PREFIX = "cw:celerytask:log"


def get_log_key(task_id):
    return "{0}:{1}".format(LOG_KEY_PREFIX, task_id)


def get_redis_client():
    conf = celery.current_app.conf
    url = conf.get('CUBICWEB_CELERYTASK_REDIS_URL')
    BROKER_TRANSPORT_OPTIONS = conf.get('broker_transport_options')
    if (url and url.startswith('redis-sentinel://')
            and 'sentinels' in BROKER_TRANSPORT_OPTIONS):
        from redis.sentinel import Sentinel
        service_name = BROKER_TRANSPORT_OPTIONS.get('service_name', 'master')
        socket_timeout = BROKER_TRANSPORT_OPTIONS.get('socket_timeout', 3)
        return Sentinel(BROKER_TRANSPORT_OPTIONS['sentinels'],
                        socket_timeout=socket_timeout).master_for(
                            service_name, redis_class=Redis,
                            socket_timeout=socket_timeout)
    elif url:
        return redis.Redis.from_url(url)


def get_task_logs(task_id):
    """
    Get task logs by id
    """
    redis_client = get_redis_client()
    return redis_client.get(get_log_key(task_id))


def flush_task_logs(task_id):
    """Delete task logs"""
    redis_client = get_redis_client()
    return redis_client.delete(get_log_key(task_id))
