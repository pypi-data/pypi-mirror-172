from pyexpat import features
from re import S
from microkit_python_server_sdk.item import Item
from microkit_python_server_sdk.http_client import HttpClient
import json
class FeaturesItem(Item):
   def __init__(self, value, name):
        self.targeting_groups = value["targeting_groups"]
        self.client = HttpClient.get_instance()
        super(FeaturesItem, self).__init__(value, name)
        
   def getValue (self, user):
      if not user or len(self.targeting_groups) == 0:
         return self.value
      else:
         features = {}
         features[self.name] = {"value": self.value, "type": self.type, "targeting_groups": self.targeting_groups}
         res = self.client.post("get_user_data", "get_feature_by_user",{"user": user,  "features": features})
         res = json.loads(res.decode('utf-8'))
         return res["features"][self.name]["value"] if self.name in res["features"] else self.value
    
    

    