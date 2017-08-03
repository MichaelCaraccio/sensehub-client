from datetime import datetime

class Value(object):

    def __init__(self, value, type, meta=None):
        self._value = value
        self._type = type
        self._meta = meta
        self._timestamp = datetime.utcnow()

    def get_dict(self):
        '''
        Convert class properties to json
        :return: json object
        '''
        return {"value": str(self._value),
               "type": str(self._type),
               "meta" : str(self._meta),
               "timestamp": str(self._timestamp)}

