from time import sleep
import requests
from multiprocessing import Process


class Client(object):
    _INTERVAL_PING_MS = 5000
    def __init__(self, server_ip, server_port, sensor_id, key):
        self._server_ip = server_ip
        self._server_port = server_port
        self._sensor_id = sensor_id
        self._key = key
        self._process_ping = Process(target=self._ping_loop)
        self._process_ping.start()

    def ping(self):
        r = self._send_put('http://'+self._server_ip+":"+self._server_port+'/api/ping', json={"sensor_id": self._sensor_id, "key": self._key})

        if r is None:
            return False, None

        return self._getServerAnswer(r)

    def new_value(self, value):

        dict_to_send = {'key': self._key, 'id': self._sensor_id, 'value' : value.get_dict()}

        r = self._send_put('http://' + self._server_ip + ":" + self._server_port + '/api/new_value', json=dict_to_send)

        if r is None:
            return False, None

        return self._getServerAnswer(r)

    def _ping_loop(self):
        interval_s = Client._INTERVAL_PING_MS / 1000.0
        while True:
            sleep(interval_s)
            self.ping()

    def _send_get(self, address, **kwargs):
        try:
            return requests.get(address, **kwargs)
        except BaseException as e:
            print(e)
            return None

    def _send_put(self, address, **kwargs):
        try:
            return requests.put(address, **kwargs)
        except BaseException as e:
            print(e)
            return None

    def _getServerAnswer(self, r):

        if r.status_code != 200:
            print("Server error:")
            print(r.json())
            return False, r.json()
        else:
            msg = r.json()
            status = msg['status']

            if status == 'ok':
                return True, None
            else:
                return False, msg['error_value']
