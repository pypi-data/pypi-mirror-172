import unittest
from microkit import Microkit
from network_controller import NetworkController
from conf import Conf
from unittest.mock import patch, MagicMock

data = {"config": "dc5+idVVGi00GpKlmkp5PyMHZ0AzpZuyl+0sfTVzYcFHCc\/8bMGvamSA3jfYEfJZJ6i6eMu4vHIvpqBF+\/LH4m9tO6Armcm4vSk9cM1rlrtypLA\/q+Ms1EUgXBWdoeJbZOz\/k8QvRu7VGz\/s9RtFPL3ouzMdKaFAj78hIMscQG5uv1ClZoLNXbLrAzO9sJPmyFS4GfUulgZ2\/sih3G7qNVaMclHcIVX6vtvz09pEF7CRH1SMZCXd\/ceh\/e1ifpeZk1g762TNF37NBIDFMf0f50dvpM0OAo+U8+WZtJASPriD4zPVvp5mGR+LdOrPYFFHpby+cyAqutWMo16a1qTIkPcQkt0XRcIGlANrCXjiCwZ8c+Vu2z3feLPurq1E1HTiTwPVB5zRuaVYstLqDmEkV3AZZI0IMAL\/nHKJFLGkFeWfVQNBlCwgeqrbSqLDh5Pn3m6\/N3MEiypSivKGjRsUSMsyIV2nrmPVUMvE3BMkXsTA0u0RYSMGCIQhqf1RbtypCfrnPIsJVA7+JSHfkMx3ZIA+1BPL9n+Hbvb4RQxPwXp+3XXkhCzKfdc2loWxMFCV\/NSi9XcGrFATLAYb9tz4\/aNhzXU+WWOLa3+RflLLSDHFKvz18pTOCNdmK4fujLv5mgH0KmNpWnndFRWY\/mJjuetBxov8NolSFrIXUcE\/MzqEc2IeB68Fv9AXMw1Uz62+Cq3rQVeTnTlattRNrtamWBluUMqA\/bZKIUP1LV\/gF8kSVSVzLWZ\/iHg1mr1YxYswkoVoKIpp3qBmkN6CyKtyHNmyRSxL\/d5fUfi5tUHmbZ\/1lMMtA0v3KC2up+uC245uup1V9H++6YHe392FaYyZe41C5A3V3vFMJiTC2VnSd\/ZbmjNLfwhPvUqcfwLApYwyXWjwPd2gNNM2lL+VVhsjTuCFNGZ+YccSKQXW4EJzUjg2YB2R\/MqFEYePL\/OyAv4K=="}
key = '3c20444b-6865-4dfb-bfee-0a0b7279572b-qPYBtP5lgv4f/TDOV17BZA=='
base_url = 'test'

class MicrokitTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass
    
    
    
    
    @patch('urllib.request.urlopen')
    def test_initializeKit_return_Microkit_instanc (self,mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = data
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        microkit = Microkit.initialize_kit(key)
        self.assertIsInstance(microkit, Microkit)

    @patch('urllib.request.urlopen')
    def test_network_controller_instanc (self,mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = data
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        microkit = Microkit.initialize_kit(key)
        self.assertIsInstance(microkit.network_controller, NetworkController)
    
    @patch('urllib.request.urlopen')
    def test_config_base_url_return_Microkit_instanc (self,mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = data
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
        
        microkit = Microkit.initialize_kit(key, {}, {"base_url": "test"})
        self.assertEqual(microkit.config.get('base_url'), 'test')
    
    @patch('urllib.request.urlopen')
    def test_config_kit_item_value (self,mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = data
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm
        
        microkit = Microkit.initialize_kit(key, {}, {"base_url": "test"})
        self.assertEqual(microkit.config_kit.ports.configurations.value, '8020')
    
    # @patch('urllib.request.urlopen')
    # def test_initializeKit_call_post (self,mock_urlopen):
    #     cm = MagicMock()
    #     cm.getcode.return_value = 200
    #     cm.read.return_value = data
    #     cm.__enter__.return_value = cm
    #     mock_urlopen.return_value = cm
        
    #     microkit = Microkit.initialize_kit(key, {}, {"base_url": "test"})
    #     self.assertTrue(mock_urlopen.called)
    
    # @patch('urllib.request.urlopen')
    # def test_initializeKit_call_post (self,mock_urlopen):
    #     cm = MagicMock()
    #     cm.getcode.return_value = 200
    #     cm.read.return_value = data
    #     cm.__enter__.return_value = cm
    #     mock_urlopen.return_value = cm
        
       
    #     res = self.client.post()
    #     self.assertEqual(res, data)

    

if __name__ == '__main__':
    unittest.main()