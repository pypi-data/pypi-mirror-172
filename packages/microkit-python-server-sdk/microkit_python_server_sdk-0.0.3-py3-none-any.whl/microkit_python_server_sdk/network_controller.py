
from microkit_python_server_sdk.http_client import HttpClient
from microkit_python_server_sdk.publisher import Publisher
import threading
import time

class NetworkController:
    
    def __init__(self, config):
        self.config = config
        self.client = HttpClient(config)
        self.change = Publisher()

    def get_latest_data (self, action):
        return self.client.post(action, None, {"user": self.config.get("user")})

    
    def start_update_interval (self):
        self.thread = StoppableThread(target=self.update)
        self.thread.start()

    def stop_update_interval (self):
        self.thread.stop()

    def update(self):
        count = 0
        while True:
            count = count + 1
            if self.thread.stopped():
                break
            if count == self.config.get('polling_interval'):
                count = 0
                res = self.get_latest_data('update')
                self.change.publish(res, {})
            time.sleep(1)



class StoppableThread(threading.Thread):

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()