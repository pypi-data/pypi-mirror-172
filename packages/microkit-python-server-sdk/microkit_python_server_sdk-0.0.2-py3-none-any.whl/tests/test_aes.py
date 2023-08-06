import unittest
from http_client import HttpClient
from conf import Conf
from unittest.mock import patch, MagicMock
from aes import AES
import base64
import time

data = {"key1": "value1"}

class AesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
       
        self.chiper = 'NqAun3kjEOZXwrdBQSD2emC/PV+QltZVcqdpTgOHthe3DE52FpA5fc3Nw10eavkgNXiaHTlHujvnUHawKKdoiadxNagQtgGuEbY7BMKa0eWk1xNYlJWbjnvVi5CIiZtRLOLV9SOpexd2N3lvU/kitCIMYfCU9PxxApRXzTeA746T3GTfD/GpHa70pu0ygk6suI1489xUa0S5wnaHsHDM09yuCKUg+uHGgsJcEiJohAwUF8uH5CaKkLlE13cELVszqSBj+arhdBL5+Ad1P/gJsLONnUDZDmWcmEohst+rbJ3eBUhhpJYPCxxjFc24WYSriZsiPxEsJWTcErhDCviNQsOIBej05sPAwuNg9BV7PHXx41IPrX3mfp3rlgAoEmiOcuXHxCz010Nt4HOuuUyp8QXGDhroVwghHffIihcJ4Ym3Jruba5WcWX80C77BadF8VHCRs1UnoeyH0YOAYj++p0JKrodfFvybxwlburMdmjvbTOZBXTh3k+q8tWkOMMWI62m7uife0Fs3hDfTCUzwYr7s/isSPxUldAat3GIg3YeBkUOulSSyvt/UqS6eEf+tYRzJz7k0U8B0JbsKyZAHoUU6gYQQEabj5Hjoy/RmNm5HiUTkoBjzEHtxZJ6r8Tr7sGBncCDeKE+4xT1fJEDTcZ48N1xsGfBX2utM7G+NHV5lx1o7R6dI88uieeHNVv/yGa3+u3BXzvCvo3qUcB5MqhskyCl70Xg34X4ZcC4l2ssveVCnb032ME7aFRFxEyDj7Se/xmFMoXZeOqMsrAbLPvRJIQkZDSezDYtGlz1vyL1AujITSQgjovzBcxIX29e+OxYFUcdySZNYANYtJFFFJwh/2w1wuAzTPJTz0EylRf9k2xhS/hmbZ6hM6nSDTT+J60sDFEpHOdR2x4SzSwy7ewr1kAFT9TV9NCEg24RWgx4iRYhe7LGASq3wuCmwlWcIQ6qeD5LogeJeVNTjcrh/T03bLbAjdxvaf2yF3rmi7s479yZXf0aYVSqf9IVUjIRLZ4kAwjw4/YU3iIyy9wf3k95L6os5BxFe2vOD6jDemhwsATKvcgByw9fv8tTMMSVsL4Suy2gZU5MWpu0HOJ1Nqb+FCaKSD/VL9cwdc7gqHMpeDIir+4IR9gmvDuU3fnNjo/XJpbKj4IjlSDWpBPqIT7Td6Xhxb0SOOJ4geFEwT7MPGMVsmESfP49W1kjmeNMaEH/kC55MEjUdqBhVIzHyzRqPIB3+mJgczbLBRwPbgW0='
    
    def test_aes(self):
        key = base64.b64decode('qPYBtP5lgv4f/TDOV17BZA==')
        iv = base64.b64decode(self.chiper)[:16]
        text = base64.b64decode(self.chiper)[16:]
        start = time.time()
        print(AES(key).decrypt_cbc(text, iv))
        
        end = time.time()
        print(end - start)
    
    

if __name__ == '__main__':
    unittest.main()