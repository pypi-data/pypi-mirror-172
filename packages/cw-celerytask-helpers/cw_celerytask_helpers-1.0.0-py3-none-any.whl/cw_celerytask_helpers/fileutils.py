import errno
import gzip
import os

import celery


def get_log_filename(task_id):
    logdir = celery.current_app.conf.get('CUBICWEB_CELERYTASK_LOGDIR')
    if not logdir:
        raise RuntimeError(
            "You asked for file-based log storage of the task logs "
            "but CUBICWEB_CELERYTASK_LOGDIR is not configured. "
            "Please set CUBICWEB_CELERYTASK_LOGDIR in your "
            "celery configuration.")
    return os.path.join(logdir, 'celerytask-{}.log.gz'.format(task_id))


def get_task_logs(task_id):
    """
    Get task logs by id
    """
    try:
        with gzip.open(get_log_filename(task_id), 'rb') as f:
            return f.read()
    except IOError as exc:
        if exc.errno != errno.ENOENT:
            raise
        return None


def flush_task_logs(task_id):
    """Delete task logs"""
    try:
        os.unlink(get_log_filename(task_id))
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise
