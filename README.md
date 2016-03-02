# swift-event-notification
Sending out notifications should happen when an object got modified. That means every successful object change (PUT, POST, DELETE) should trigger an action and send out an event notification. This middlware uses Zaqar which is a multi-tenant cloud messaging and notification service for web and mobile developers.Installation instructions for zaqar can be found at below link  http://docs.openstack.org/developer/zaqar/devref/development.environment.html


1) Install Swift-event-notification with sudo python setup.py install or sudo python setup.py develop or via whatever packaging system you may be using.
 
2) Alter your proxy-server.conf pipeline to have swift-event-notification:

   a) Add 'event-notifier' to pipeline</br>
   b) Add filter 
      [filter:event-notifier]
      use = egg:event-notifier#event-notifier

