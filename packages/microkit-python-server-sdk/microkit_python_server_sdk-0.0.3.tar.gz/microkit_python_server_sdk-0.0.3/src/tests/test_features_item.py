import unittest
from featrues_item import FeaturesItem
from publisher import Publisher
from unittest.mock import Mock


class FeaturesItemTestCase(unittest.TestCase):
    def test_value(self):
        value = {'value': 'value', 'type': 'type'}
        item = FeaturesItem(value)
        self.assertEqual(item.value, 'value')
    
    def test_change_prop(self):
        value = {'value': 'value', 'type': 'type'}
        item = FeaturesItem(value)
        self.assertTrue(isinstance(item.change, Publisher))
    
    def test_change_is_called_when_value_is_change(self):
        value = {'value': 'value', 'type': 'type'}
        item = FeaturesItem(value)
        test_dict = {}
        
        def func (currentVal, prevVal):
            test_dict['value'] = currentVal

        item.change.subscribe(func)
        item.value = 'change'
        self.assertEqual(test_dict['value'], item.value)

    def test_change_is_called_when_value_is_change_object(self):
        value = {'value': 'value', 'type': 'type'}
        item = FeaturesItem(value)
        test_dict = {}
        
        def func (currentVal, prevVal):
            test_dict['value'] = currentVal

        item.change.subscribe(func)
        item.value = {'value': 'change', 'type': 'type'}
        self.assertEqual(test_dict['value'], item.value)

    def test_change_is_called_when_type_is_change_object(self):
        value = {'value': 'value', 'type': 'type'}
        item = FeaturesItem(value)
        test_dict = {}
        
        def func (currentVal, prevVale):
            test_dict['value'] = currentVal

        item.change.subscribe(func)
        item.value = {'value': 'value', 'type': 'change'}
        self.assertEqual(test_dict['value'], item.value)

    def test_change_is_not_called_when_value_is_not_change(self):
        value = {'value': 'value', 'type': 'type'}
        item = FeaturesItem(value)
        f = Mock()

        item.change.subscribe(f)
        item.value = 'value'
        f.assert_not_called()
    
    

    

if __name__ == '__main__':
    unittest.main()