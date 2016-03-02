from eventlet.green import urllib2
from eventlet import Timeout
import json
import uuid

from swift.common.http import is_success
from swift.common.swob import wsgify
from swift.common.utils import get_logger
from swift.common.utils import split_path


class EventNotificationMiddleware(object):

    def __init__(self, app, conf):
        self.app = app
        self.logger = get_logger(conf, log_route='eventnotification')
        self.server = conf.get('server', 'http://localhost:8888/v1/'
                               'queues/samplequeue/messages')
        self.client_id = str(uuid.uuid4())

    @wsgify
    def __call__(self, req):
        if req.method not in ("POST", "PUT", "DELETE", "COPY"):
            return self.app
        self.logger.debug("entered notification middlware")
        obj = None
        try:
            (version, account, container, obj) = \
                split_path(req.path_info, 4, 4, True)
        except ValueError:
            # not an object request
            return self.app
        resp = req.get_response(self.app)
        if obj and is_success(resp.status_int) and \
           req.method in ("POST", "PUT", "DELETE", "COPY"):
            notification_server = self.server
            if notification_server:
                # create a POST request with obj name as body
                data = json.dumps([{"ttl": 800, "body": {"account": account,
                                    "container": container, "object": obj,
                                  "method": req.method}}])
                event_req = urllib2.Request(notification_server, data)
                event_req.add_header('Content-Type', 'application/json')
                event_req.add_header('Client-ID', self.client_id)
                with Timeout(20):
                    try:
                        response = urllib2.urlopen(event_req)
                    except (Exception, Timeout):
                        self.logger.exception(
                            'failed to POST object %s' % obj)
                    else:
                        self.logger.info(
                            'successfully posted object %s' % obj)
        return resp


def filter_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)

    def Event_filter(app):
        return EventNotificationMiddleware(app, conf)
    return Event_filter
