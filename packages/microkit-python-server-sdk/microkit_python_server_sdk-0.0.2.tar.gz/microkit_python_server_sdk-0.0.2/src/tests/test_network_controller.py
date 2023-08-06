import unittest
from http_client import HttpClient
from conf import Conf
from unittest.mock import patch, MagicMock
from network_controller import NetworkController

data = {"key1": "value1"}

class NetworkControllerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        config = Conf(api_key = 'key')
        # self.client = HttpClient(config)
        self.controller = NetworkController(config)
    
    def test_config(self):
        self.assertEqual(self.controller.config.get('api_key'), 'key')
    
    def test_client(self):
        self.assertTrue(isinstance(self.controller.client, HttpClient))
    
    @patch('urllib.request.urlopen')
    def test_get_latest_data(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = data
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
       
        res = self.controller.get_latest_data()
        self.assertEqual(res, data)

    # test get 
    # test port
    # test http/https
    # test start with http
    # test valid json

if __name__ == '__main__':
    unittest.main()