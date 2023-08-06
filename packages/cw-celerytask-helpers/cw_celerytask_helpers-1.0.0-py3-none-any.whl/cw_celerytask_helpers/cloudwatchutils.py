from time import time
from os import getenv

import boto3
import celery


def get_stream_name(task_id):
    stream_pattern = celery.current_app.conf.get(
        'CUBICWEB_CELERYTASK_STREAM_PATTERN', 'celerytask-%s')
    return stream_pattern % task_id


def get_logs_client():
    endpoint_url = getenv('AWS_CLOUDWATCH_ENDPOINT_URL')
    return boto3.client('logs', endpoint_url=endpoint_url)


def get_task_logs(task_id):
    log_group = celery.current_app.conf.get('CUBICWEB_CELERYTASK_LOG_GROUP')
    if not log_group:
        return None
    stream_name = get_stream_name(task_id)
    client = get_logs_client()
    try:
        logs = b''
        kwargs = {
            'logGroupName': log_group,
            'logStreamName': stream_name,
            'startFromHead': True,
            'endTime': int(time() * 1000),  # avoid getting newer logs
        }
        while True:
            result = client.get_log_events(**kwargs)
            for event in result['events']:
                message = event['message']
                if isinstance(message, str):
                    message = message.encode('utf-8')
                logs += message + b'\n'
            if 'nextForwardToken' not in result or (
                    'nextToken' in kwargs
                    and result['nextForwardToken'] == kwargs['nextToken']):
                return logs
            kwargs['nextToken'] = result['nextForwardToken']
    except client.exceptions.ResourceNotFoundException:
        return None


def flush_task_logs(task_id):
    log_group = celery.current_app.conf.get('CUBICWEB_CELERYTASK_LOG_GROUP')
    if not log_group:
        return
    stream_name = get_stream_name(task_id)
    client = get_logs_client()
    try:
        client.delete_log_stream(
            logGroupName=log_group,
            logStreamName=stream_name)
    except client.exceptions.ResourceNotFoundException:
        pass
