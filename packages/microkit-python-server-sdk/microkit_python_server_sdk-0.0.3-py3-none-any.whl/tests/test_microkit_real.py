import unittest
from microkit_python_server_sdk.microkit import Microkit




class MicrokitTestCase(unittest.TestCase):
   
    def test_initializeKit (self):
        microkit = Microkit.initialize_kit("83578f1b-e460-43ce-a481-a1efd5382496-B+XtrA4P/2nDYHmrh+Ts/g==", {}, {"base_url": "localhost", "port": "8030", "http": True, 'polling_on': False})
        print(microkit.features_kit.value)
        def callback(current, prev):
            print(current)
            print(prev)
            
        microkit.config_kit.ports.change.subscribe(callback)

    

if __name__ == '__main__':
    unittest.main()