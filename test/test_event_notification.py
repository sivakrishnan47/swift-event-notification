import unittest

from swift.common.swob import Request
from event.event_notification import EventNotificationMiddleware

import requests


class FakeApp(object):
    def __call__(self, env, start_response):
        start_response('200 OK', [])
        return[]


class TestEventNotifications(unittest.TestCase):
    def test_object_post(self):
        environ = {'REQUEST_METHOD': 'PUT'}
        req = Request.blank('/v1/a/c/o', environ)
        notifier = EventNotificationMiddleware(FakeApp(), {'server': 'http://localhost:8888/v1/queues/samplequeue/messages'})
        req.get_response(notifier)
        # URL of Zaqar queue where object was posted
        url = notifier.server+'?echo=true'
        headers = {'Content-Type': 'application/json', 'Client-ID': notifier.client_id}
        # Get message from queue
        q_req = requests.get(url, headers=headers)
        self.assertEqual(200, q_req.status_code)

if __name__ == '__main__':
    unittest.main()
