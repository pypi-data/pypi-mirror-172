import os

import boto3
import celery


def get_bucket_name():
    bucket = celery.current_app.conf.get('CUBICWEB_CELERYTASK_S3_BUCKET')
    if not bucket:
        bucket = os.getenv('AWS_S3_BUCKET_NAME')
    return bucket


def get_key_name(task_id):
    key_pattern = celery.current_app.conf.get(
        'CUBICWEB_CELERYTASK_S3_KEY_PATTERN', 'celerytask-%s')
    return key_pattern % task_id


def get_s3_client():
    s3_endpoint_url = os.getenv(
        'AWS_S3_ENDPOINT_URL', 'https://s3.amazonaws.com')
    return boto3.client('s3', endpoint_url=s3_endpoint_url)


def get_task_logs(task_id):
    bucket = get_bucket_name()
    if not bucket:
        return None
    key = get_key_name(task_id)
    client = get_s3_client()
    try:
        result = client.get_object(Bucket=bucket, Key=key)
        return result['Body'].read()
    except client.exceptions.NoSuchKey:
        return None


def flush_task_logs(task_id):
    bucket = get_bucket_name()
    if not bucket:
        return
    key = get_key_name(task_id)
    client = get_s3_client()
    try:
        client.delete_object(Bucket=bucket, Key=key)
    except client.exceptions.NoSuchKey:
        pass
