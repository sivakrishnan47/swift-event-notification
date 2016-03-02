from setuptools import setup, find_packages

name = "event-notifier"

setup(
    name=name,
    author="Sivasathurappan Radhakrishnan",
    author_email="siva.radhakrishnan@intel.com",
    description="Notifies of any changes to server configured",
    keywords="openstack swift middleware",
    packages=find_packages(),
    entry_points={
        'paste.filter_factory': [
            'event-notifier=event.event_notification:filter_factory',
            ],
        },
    )
