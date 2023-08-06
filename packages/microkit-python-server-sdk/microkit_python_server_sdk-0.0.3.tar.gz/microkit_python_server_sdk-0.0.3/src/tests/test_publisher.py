import unittest
from publisher import Publisher
from unittest.mock import Mock

class PublisherTestCase(unittest.TestCase):
    def test_subscribers_array(self):
        pub = Publisher()
        self.assertEqual(pub.subscribers, {})
    
    def test_insert_func_into_subscribers_array(self):
        pub = Publisher()
        def func ():
            pass
        subscription = pub.subscribe(func)
        self.assertEqual(pub.subscribers[subscription.key], func)
    
    def test_unsubscribe(self):
        pub = Publisher()
        def func ():
            pass
        subscription = pub.subscribe(func)
        subscription.unsubscribe()
        self.assertEqual(pub.subscribers, {})
    
    
    def test_call_func_on_publish(self):
        pub = Publisher()
        f = Mock()
        subscription = pub.subscribe(f)
        pub.publish('current', 'prev')
        f.assert_called_with('current', 'prev')

    def test_call_func_on_first_subscription(self):
        pub = Publisher()
        f = Mock()
        subscription = pub.subscribe(f)
        subscription.call()
        f.assert_called_once()
    
    

    

if __name__ == '__main__':
    unittest.main()