import requests
import configparser

class Client(object):
    def __init__(self, server_ip, server_port, sensor_id, key):
        self._server_ip = server_ip
        self._server_port = server_port
        self._sensor_id = sensor_id
        self._key = key

    def ping(self):
        r = requests.put('http://'+self._server_ip+":"+self._server_port+'/api/ping', json={"sensor_id": self._sensor_id, "key": self._key})

        return self._getServerAnswer(r)

    def new_value(self, value):

        dict_to_send = {'key': self._key, 'id': self._sensor_id, 'value' : value.get_dict()}

        r = requests.put('http://' + self._server_ip + ":" + self._server_port + '/api/new_value', json=dict_to_send)

        return self._getServerAnswer(r)

    @staticmethod
    def create_client(filename = "./config-example.ini"):

        try:
            config = configparser.ConfigParser()
            config.read(filename)

            _server_ip = config.get("server", 'ip')
            _server_port = config.get("server", 'port')
            _sensor_id = config.get("user", 'sensor_id')
            _key = config.get("user", 'key')

            return Client(_server_ip, _server_port, _sensor_id, _key)

        except FileExistsError:
            print("Error with file")
        except FileNotFoundError:
            print("File does not exist")
        except configparser.NoOptionError:
            print("Option does not exist")

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
