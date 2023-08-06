from email.policy import HTTP
import unittest
from conf import Conf
from unittest.mock import patch, MagicMock


class ConfTestCase(unittest.TestCase):
    def test_init_options(self):
        options = {
            'base_url': 'test url',
            'api_key': 'key',
            'port': '443',
            'http': True,
            'polling_interval': 1000,
        }
        client = Conf(options)

        self.assertEqual(client.get('base_url'), options['base_url'])
        self.assertEqual(client.get('api_key'), options['api_key'])
        self.assertEqual(client.get('port'), options['port'])
        self.assertEqual(client.get('http'), options['http'])
        self.assertEqual(client.get('polling_interval'), options['polling_interval'])
   
    def test_init_options_default(self):
        options = {
            'base_url': 'test url',
            'api_key': 'key',
            'port': '443',
            'http': False,
            'polling_interval': 1000,
        }
        client = Conf( {"api_key": options['api_key']})

        self.assertEqual(client.get('base_url'), 'sdk.microkit.app')
        self.assertEqual(client.get('api_key'), options['api_key'])
        self.assertEqual(client.get('port'), 443)
        self.assertEqual(client.get('http'), False)
        self.assertEqual(client.get('polling_interval'), 30000)
    
    def test_raise_if_api_does_not_exist(self):
        self.assertRaises(Exception, Conf)
    
    

    

if __name__ == '__main__':
    unittest.main()