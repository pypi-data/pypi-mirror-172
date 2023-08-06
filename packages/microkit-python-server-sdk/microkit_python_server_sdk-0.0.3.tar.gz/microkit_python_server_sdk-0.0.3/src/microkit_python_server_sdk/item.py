
from microkit_python_server_sdk.publisher import Publisher
class Item:
    
    def __init__(self, value, name):
        self._value = value['value']
        self.type = value['type']
        self.name = name
        self.change = Publisher()

    @property
    def value (self):
        if self.type == 'string':
            return str(self._value)
        elif self.type == 'number':
            return float(self._value)
        elif self.type == 'boolean':
            return  True if self._value == 'true' or self._value == True else False
       



    @value.setter
    def value(self, value):
        prev_value = self._value
        if isinstance(value, dict):
            have_been_changed = self._value != value["value"] or self.type != value["type"]
            self._value = value["value"]
            self.type = value["type"]

        else:
            have_been_changed = self._value != value
            self._value = value
        if (have_been_changed):
            self.change.publish(self._value, prev_value)

    def update(self, value):    
        self.value = value
    
    

    