import os
import sys
import json
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shadow_client import ShadowClient
from awsiot import iotshadow
from time import sleep

class TestShadowClient:

    def setup_method(self):
        self.test_config = json.load(open(os.path.join(os.path.dirname(__file__), 'test_config.json'), "r"))
        self.shadow_client = ShadowClient()

    def teardown_method(self):
        try:
            self._disconnect()
            assert self.shadow_client.has_disconnected.is_set()
        except Exception as e:
            print(f"Failed to disconnect: {e}")
    
    def _disconnect(self):
        self.shadow_client.disconnect(0)
        self.shadow_client.wait_for_disconnection()

    def _on_error(self, msg:str, fn=None):
        print(f"Error: {msg}")
        traceback.print_exc()
        if callable(fn):
            fn()
        sys.exit(1)

    def test_shadow_client_connect(self):
        try:
            self.shadow_client.connect(self.test_config['endpoint'], self.test_config['port'], self.test_config['cert'], self.test_config['key'], self.test_config['ca'], self.test_config['clientId'])
            sleep(1)
            self.shadow_client.disconnect(0)
            self.shadow_client.wait_for_disconnection()
            assert self.shadow_client.has_disconnected.is_set()
        except Exception as e:
            self._on_error(e)

    def test_shadow_client_subscribe(self):
        try:
            self.shadow_client.connect(self.test_config['endpoint'], self.test_config['port'], self.test_config['cert'], self.test_config['key'], self.test_config['ca'], self.test_config['clientId'])
            self.shadow_client.subscribe()
            sleep(1)
        except Exception as e:
            self._on_error(e, self._disconnect)

    def test_shadow_client_get(self):
        try:
            self.shadow_client.connect(self.test_config['endpoint'], self.test_config['port'], self.test_config['cert'], self.test_config['key'], self.test_config['ca'], self.test_config['clientId'])
            self.shadow_client.subscribe()
            self.shadow_client.fetch_shadow_document()
            sleep(1)
        except Exception as e:
            self._on_error(e, self._disconnect)

    def test_shadow_client_update(self):
        try:
            self.shadow_client.connect(self.test_config['endpoint'], self.test_config['port'], self.test_config['cert'], self.test_config['key'], self.test_config['ca'], self.test_config['clientId'])
            self.shadow_client.subscribe()
            self.shadow_client.fetch_shadow_document()
            sleep(1)
            state: iotshadow.ShadowStateWithDelta = self.shadow_client.get_shadow_document()
            for key, value in state.desired.items():
                state.desired[key] = value + '_updated'
            sleep(1)
            self.shadow_client.publish_update_shadow(state.desired)
            sleep(1)
            self.shadow_client.fetch_shadow_document()
            new_state: iotshadow.ShadowStateWithDelta = self.shadow_client.get_shadow_document()
            for key, value in new_state.desired.items():
                assert value == new_state.desired[key]
                new_state.desired[key] = value.replace('_updated', '')
            sleep(1)
            self.shadow_client.publish_update_shadow(new_state.desired)
            sleep(1)
        except Exception as e:
            self._on_error(e, self._disconnect)

if __name__ == '__main__':
    test = TestShadowClient()
    test.test_shadow_client_connect()
    test.test_shadow_client_subscribe()
    test.test_shadow_client_get()
    test.test_shadow_client_update()