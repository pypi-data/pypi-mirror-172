import json
import urllib.error
import urllib.parse
import urllib.request
import ssl




class HttpClient:

    instance = None

    def __init__(self, config):
        # To do raise error if url is not http
        if HttpClient.instance:
            return HttpClient.instance
        self.config = config
        HttpClient.instance = self

    def get_instance():
        return HttpClient.instance

    def post(self, action, uri = None, post_data = None):

        data = {"options": {"service": self.config.get('service'), "action": action, "lang": "python"}}
        if post_data:
            data = merge_two_dicts(data, post_data)
        
        if self.config.get("key_vars_values"):
            data = merge_two_dicts(data, {"key_vars_values": self.config.get("key_vars_values")})

        # Dict to Json
        data = json.dumps(data)

        # Convert to String
        data = str(data)

        # Convert string to byte
        data = data.encode('utf-8')

        headers = {
             'Content-Type': 'application/json',
             'Authorization': "Bearer {}".format(self.config.get('api_key'))
        }
        http = 'http' if self.config.get('http') else 'https'
        base_url = self.config.get('base_url')
        port = self.config.get('port')
        version = self.config.get('version')
        url = '%s://%s:%s/%s/%s'%(http, base_url, port, version, uri if uri else '')
        
        ssl_context = ssl.SSLContext() if not self.config.get('http') else None
        req = urllib.request.Request(url, headers=headers, data=data)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            return response.read()

def merge_two_dicts(x, y):
    z = x.copy()   
    z.update(y)    
    return z