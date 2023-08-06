import unittest
from http_client import HttpClient
from conf import Conf
from unittest.mock import patch, MagicMock

data = {"key1": "value1"}

class HttpClientTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        config = Conf({"api_key":'key'})
        self.client = HttpClient(config)
    
    def test_url(self):
        self.assertEqual(self.client.config.get('api_key'), 'key')
    
    @patch('urllib.request.urlopen')
    def test_get (self,mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = data
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
        
       
        res = self.client.post()
        self.assertEqual(res, data)

    # test get 
    # test port
    # test http/https
    # test start with http
    # test valid json

if __name__ == '__main__':
    unittest.main()