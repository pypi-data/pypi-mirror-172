
from tokenize import group
from turtle import update
from microkit_python_server_sdk.publisher import Publisher
from microkit_python_server_sdk.config_item import ConfigItem
from microkit_python_server_sdk.features_item import FeaturesItem
class Group:
    types = ['config', 'features']
    def __init__(self, type, values, ):
        if type not in Group.types:
            raise Exception('Group type is not valid')
        self.group = {}
        self.type = type
        self.change = Publisher()
        self.updated = False
        self.initialized = False
        self.update(values)
   
    def update (self, values):
        prev_value = self.value
        for key, item in values.items():
            if key in self.group:
                self.group[key].update(item)
            else:
                if self.initialized:
                    self.updated = True
                if "value" in item and not type(item['value']) is dict:
                    self.group[key] =  ConfigItem(item, key) if self.type is 'config' else FeaturesItem(item, key)
                    def published(current_value, prev_value):
                        self.updated = True
                    self.group[key].change.subscribe(published)
                else:
                    self.group[key] =  Group(self.type, item)
            setattr(self, key, self.group[key])

        if not self.initialized:
            self.initialized = True 
        if self.updated:
            self.change.publish(self.value ,prev_value)
            self.updated = False 

    @property
    def value (self):
        val = {}
        for key, item in self.group.items():
            val[key] = item.value
        return val

    