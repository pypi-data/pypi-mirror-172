from microkit_python_server_sdk.conf import Conf
from microkit_python_server_sdk.network_controller import NetworkController
from microkit_python_server_sdk.group import Group
from microkit_python_server_sdk.aes import AES
import base64
import json

class Microkit:
    
    instance = None

    def __init__(self, key,  user , options):
        if Microkit.instance:
            return Microkit.instance
        options['api_key'] = key
        self.config = Conf(options=options, user=user)
        self.network_controller = NetworkController(self.config)
        Microkit.instance = self
   

    @staticmethod
    def initialize_kit (key, user = {}, options = {}):
        if not Microkit.instance:

            key_size = len(key)
            secret_size = 24
            sdk_key = key[:key_size-secret_size-1]
            secret = key[-secret_size:]
            Microkit(sdk_key, user, options)
            res = Microkit.instance.network_controller.get_latest_data('init')
            res = json.loads(res.decode('utf-8'))
            
            Microkit.instance.config.set("key_vars_values", res["key_vars_values"])
            Microkit.instance.config_kit = Group('config', Microkit.decrypt(res['config'], secret) if 'config' in res and res['config'] != '' else {})
            Microkit.instance.features_kit = Group('features', res["features"] if 'features' in res and type(res["features"]) == dict  else {})
            if Microkit.instance.config.get('polling_on'):
                Microkit.instance.network_controller.start_update_interval()
                def callback (current_val, prev_val):
                    current_val = json.loads(current_val.decode('utf-8'))
                    Microkit.instance.config_kit.update(Microkit.decrypt(current_val['config'], secret) if 'config' in current_val and current_val['config'] != '' else {})
                    Microkit.instance.features_kit.update(current_val["features"] if 'features' in current_val and type(current_val["features"]) == dict  else {})
                    Microkit.instance.config.set("key_vars_values", res["key_vars_values"])
                Microkit.instance.network_controller.change.subscribe(callback)

        return Microkit.instance

    def decrypt(raw_text, secret):
        key = base64.b64decode(secret)
        iv = base64.b64decode(raw_text)[:16]
        text = base64.b64decode(raw_text)[16:]
    
        decrypt_value = AES(key).decrypt_cbc(text, iv)
        return json.loads(decrypt_value.decode('utf-8'))

    def close (self):
        self.network_controller.stop_update_interval()

    def kit_ready():
        if Microkit.instance.features_kit and Microkit.instance.config_kit:
            return Microkit.instance
        else:
            return False