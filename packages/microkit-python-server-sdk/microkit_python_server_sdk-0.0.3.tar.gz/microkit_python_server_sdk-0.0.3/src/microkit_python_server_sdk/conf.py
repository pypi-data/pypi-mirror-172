
class Conf:
    conf = {"version": "v1"}
    def __init__(self, options, user):
        self.conf['base_url'] = options['base_url'] if 'base_url' in options else 'sdk.microkit.app'
        self.conf['api_key'] = self.validate_require(options, 'api_key')
        self.conf['port'] = options['port'] if 'port' in options else 443
        self.conf['http'] = options['http'] if 'http' in options else False
        self.conf['polling_interval'] = options['polling_interval'] if 'polling_interval' in options else 30
        self.conf['service'] = options['service'] if 'service' in options else ''
        self.conf['polling_on'] = options['polling_on'] if 'polling_on' in options else True
        self.conf['user'] = user

    def get (self, conf_name):
        if conf_name in self.conf:
            return self.conf[conf_name]
        else:
            return None

    def set (self, key, value):
        self.conf[key] = value
        
    def validate_require(self, options, value_name):
        if value_name in options:
            return options[value_name]
        else:
            raise Exception("{} is required.".format(value_name))
    

    