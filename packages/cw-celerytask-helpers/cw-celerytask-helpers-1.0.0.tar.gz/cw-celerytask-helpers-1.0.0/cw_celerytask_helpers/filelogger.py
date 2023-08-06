"""Helpers for managing logging to file in cubicweb-celerytask workers

Add this module 'cw_celerytask_helpers.filelogger' to CELERY_IMPORTS

You can control where logs are stored with the CUBICWEB_CELERYTASK_LOGDIR
config, the directory must exist and be writable.
"""
from __future__ import absolute_import

import logging
import gzip

from celery import signals

from .fileutils import get_log_filename

LOG_KEY_PREFIX = "cw:celerytask:log"


class UnknownTaskId(Exception):
    pass


def get_log_key(task_id):
    return "{0}:{1}".format(LOG_KEY_PREFIX, task_id)


@signals.celeryd_after_setup.connect
def setup_file_logging(conf=None, **kwargs):
    logger = logging.getLogger('celery.task')
    store_handler = FileStoreHandler(level=logging.DEBUG)
    store_handler.setFormatter(logging.Formatter(
        fmt="%(levelname)s %(asctime)s %(module)s %(process)d %(message)s\n"))
    logger.addHandler(store_handler)


class FileStoreHandler(logging.Handler):
    """
    Send logging messages to a file in
    """

    def emit(self, record):
        """
        Append logs to gzip log file in `self.logdir`
        """
        # See celery.app.log.TaskFormatter
        if record.task_id not in ('???', None):
            fname = get_log_filename(record.task_id)
            with gzip.open(fname, 'a') as f:
                formatted = self.format(record)
                if isinstance(formatted, str):
                    f.write(formatted.encode('utf-8'))
                else:
                    f.write(formatted)
