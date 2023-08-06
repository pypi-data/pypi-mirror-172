from unittest import TestCase
from unittest.mock import patch

from redislite import Redis

from cw_celerytask_helpers.redisutils import (flush_task_logs,
                                              get_log_key,
                                              get_task_logs,
                                              LOG_KEY_PREFIX)


class RedisUtilsTC(TestCase):

    def setUp(self):
        self.redis = Redis()
        self.redis.set(f"{LOG_KEY_PREFIX}:key", "42")

    def test_get_log_key(self):
        self.assertEqual(get_log_key("42"), f"{LOG_KEY_PREFIX}:42")

    def test_get_task_logs_with_redis(self):
        with patch("cw_celerytask_helpers.redisutils.get_redis_client",
                   return_value=self.redis) as mocked_redis:
            self.assertIsNone(get_task_logs("unknown_key"))
            self.assertEqual(get_task_logs("key"), b"42")

    def test_flush_task_logs_with_redis(self):
        with patch("cw_celerytask_helpers.redisutils.get_redis_client",
                   return_value=self.redis) as mocked_redis:
            self.assertIsNotNone(self.redis.get(f"{LOG_KEY_PREFIX}:key"))

            flush_task_logs("key")
            self.assertIsNone(self.redis.get(f"{LOG_KEY_PREFIX}:key"))
