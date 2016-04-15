from .save_application_event_test import SaveApplicationEventTestCase
from .save_connectivity_event_test import SaveConnectivityEventTestCase
from .save_events_tests import SaveEventsTestCase
from .save_events_with_device_and_sim_test import SaveEventsWithDeviceAndSimTestCase
from .save_mobile_event_test import SaveMobileEventTestCase
from .save_wifi_event_test import SaveWifiEventTestCase


def send_json_for_test(test, json, token):
    request = test.app.post('/api/events', data=dict(
            events=json
    ), headers={'Authorization': 'token ' + token})

    return request
