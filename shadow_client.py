"""
Copyright (c) 2023 embd-io
latyr.fall@embd-io.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from time import sleep
from awscrt import mqtt, http
from awsiot import iotshadow, mqtt_connection_builder
from concurrent.futures import Future
import sys
import threading
import traceback
from uuid import uuid4

class ShadowClient:
    """"""
    
    def __init__(self):
        """"""
        self.client_id = ""
        
        self.mqtt_connection: mqtt.Connection = None
        self.shadow_client: iotshadow.IotShadowClient = None
        self.device_name: str = ""

        self.has_disconnected = threading.Event()
        self.critical_error = threading.Event()

        self.document: iotshadow.ShadowStateWithDelta = None

    def connect(self, endpoint: str, client: str, device: str, port: int, cert: str, key: str, ca: str):
        """"""
        self.device_name = device
        self.client_id = client
        try:
            self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=endpoint,
                port=port,
                cert_filepath=cert,
                pri_key_filepath=key,
                ca_filepath=ca,
                client_id=client,
                clean_session=False,
                keep_alive_secs=30,
                http_proxy_options=None)

            connected_future = self.mqtt_connection.connect()
            self.shadow_client = iotshadow.IotShadowClient(self.mqtt_connection)
            connected_future.result()
            print("Connected!")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def _on_disconnected(self, disconnect_future):
        """"""
        print("Disconnected.")
        self.has_disconnected.set()

    def disconnect(self, code):
        """"""
        try:
            print(f"Disconnecting, error code = {code}")
            future = self.mqtt_connection.disconnect()
            future.add_done_callback(self._on_disconnected)
        except Exception as e:
            print(f"Failed to disconnect: {e}")

    def wait_for_disconnection(self):
        """"""
        self.has_disconnected.wait()

    def _subscribe_to_update_topics(self):
        """"""
        try:
            update_accepted_subscribed_future, _ = self.shadow_client.subscribe_to_update_shadow_accepted(
                request=iotshadow.UpdateShadowSubscriptionRequest(thing_name=self.device_name),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_update_shadow_accepted)

            update_rejected_subscribed_future, _ = self.shadow_client.subscribe_to_update_shadow_rejected(
                request=iotshadow.UpdateShadowSubscriptionRequest(thing_name=self.device_name),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_update_shadow_rejected)

            # Wait for subscriptions to succeed
            update_accepted_subscribed_future.result()
            update_rejected_subscribed_future.result()

            print("Subscribed to update topics.")
        except Exception as e:
            print(f"Failed to subscribe to update topics: {e}")

    def _subscribe_to_get_topics(self):
        """"""
        try:
            get_accepted_subscribed_future, _ = self.shadow_client.subscribe_to_get_shadow_accepted(
                request=iotshadow.GetShadowSubscriptionRequest(thing_name=self.device_name),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_get_shadow_accepted)

            get_rejected_subscribed_future, _ = self.shadow_client.subscribe_to_get_shadow_rejected(
                request=iotshadow.GetShadowSubscriptionRequest(thing_name=self.device_name),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_get_shadow_rejected)

            # Wait for subscriptions to succeed
            get_accepted_subscribed_future.result()
            get_rejected_subscribed_future.result()

            print("Subscribed to get topics.")
        except Exception as e:
            print(f"Failed to subscribe to get topics: {e}")

    def publish_update_shadow(self, update_value):
        """"""
        try:
            request = iotshadow.UpdateShadowRequest(
                thing_name=self.device_name,
                state=iotshadow.ShadowState(
                    desired=update_value
                )
            )
            future = self.shadow_client.publish_update_shadow(request, mqtt.QoS.AT_LEAST_ONCE)
            future.add_done_callback(self.on_publish_update_shadow)
        except Exception as e:
            print(f"Failed to publish update request: {e}")

    def fetch_shadow_document(self):
        """"""
        try:
            request = iotshadow.GetShadowRequest(thing_name=self.device_name)
            future = self.shadow_client.publish_get_shadow(request, mqtt.QoS.AT_LEAST_ONCE)
            # future.add_done_callback(self.on_get_shadow_accepted)
            future.result()
            print("Get request published.")
        except Exception as e:
            print(f"Failed to publish get request: {e}")

    def get_shadow_document(self) -> iotshadow.ShadowStateWithDelta:
        """"""
        return self.document

    def loop(self):
        """"""
        while not self.has_disconnected.is_set() or not self.critical_error.is_set():
            sleep(5)
        self.has_disconnected.wait()

    def subscribe(self):
        """"""
        self._subscribe_to_update_topics()
        self._subscribe_to_get_topics()

    def from_state(self, state):
        # type: (iotshadow.ShadowStateWithDelta) -> None
        """"""
        self.document = state

    def on_get_shadow_accepted(self, response):
        # type: (iotshadow.GetShadowResponse) -> None
        """"""
        print(f"Received get response, state:{response.state}")
        self.from_state(response.state)

    def on_get_shadow_rejected(self, error):
        """"""
        print(f"Get request was rejected. code:{error.code} message:'{error.message}'")

    def on_shadow_delta_updated(self, delta):
        """"""
        print("Received shadow delta.")

    def on_publish_update_shadow(self, future):
        """"""
        try:
            future.result()
            print("Update request published.")
        except Exception as e:
            print("Failed to publish update request.")
            self.disconnect(e)

    def on_update_shadow_accepted(self, response):
        # type: (iotshadow.UpdateShadowResponse) -> None
        """"""
        print(f"Update request accepted, state:{response.state}")

    def on_update_shadow_rejected(self, error):
        """"""
        print(f"Update request was rejected. code:{error.code} message:'{error.message}'")
