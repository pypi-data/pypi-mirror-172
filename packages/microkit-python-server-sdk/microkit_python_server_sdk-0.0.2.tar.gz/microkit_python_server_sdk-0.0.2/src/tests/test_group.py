from multiprocessing.sharedctypes import Value
import unittest
from group import Group
from publisher import Publisher
from unittest.mock import Mock
from config_item import ConfigItem

class GroupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.value = {
            'item_1': {
                'value': 'value_1',
                'type': 'type_1'
                },
            'item_2' : {
                'value': 'value_2',
                'type': 'type_2'
                }
        }
        

    def test_group_prop(self):
        group = Group('config', self.value)
        self.assertTrue(isinstance(group.group, type({})))
    
    def test_type_prop(self):
        group = Group('config', self.value)
        self.assertEqual(group.type, 'config')
    
    def test_exception_if_type_not_valid(self):
        self.assertRaises(Exception, Group ,'not_valid', self.value)
            
    def test_update_values(self):
        group = Group('config', self.value)
        self.assertTrue(isinstance(group.item_1, ConfigItem))

    def test_change_prop(self):
        group = Group('config', self.value)
        self.assertTrue(isinstance(group.change, Publisher)) 
    
    # def test_change_called_if_children_is_changed(self):
    #     group = Group('config', self.value)
    #     f = Mock()
    #     group.change.subscribe(f)
    #     new_value = self.value.copy()
    #     new_value['item_1']['value'] = 'other_value'
    #     group.update(new_value)
        
    #     f.assert_called_once()

    def test_change_called_with_all_children_values(self):
        group = Group('config', self.value)
        f = Mock()
        group.change.subscribe(f)
        new_value = self.value.copy()
        new_value['item_1']['value'] = 'other_value'
        group.update(new_value)
        f.assert_called_once_with({
                'item_1': 'other_value',
                'item_2' : 'value_2'
            },
            {
                'item_1': 'value_1',
                'item_2' : 'value_2'
            })
    
    # def test_value(self):
    #     value = {'value': 'value', 'type': 'type'}
    #     item = Group(value)
    #     self.assertEqual(item.value, 'value')
    
    # def test_change_prop(self):
    #     value = {'value': 'value', 'type': 'type'}
    #     item = Group(value)
    #     self.assertTrue(isinstance(item.change, Publisher))
    
    # def test_change_is_called_when_value_is_change(self):
    #     value = {'value': 'value', 'type': 'type'}
    #     item = Group(value)
    #     test_dict = {}
        
    #     def func (val):
    #         test_dict['value'] = val

    #     item.change.subscribe(func)
    #     item.value = 'change'
    #     self.assertEqual(test_dict['value'], item.value)

    # def test_change_is_not_called_when_value_is_not_change(self):
    #     value = {'value': 'value', 'type': 'type'}
    #     item = Group(value)
    #     f = Mock()

    #     item.change.subscribe(f)
    #     item.value = 'value'
    #     f.assert_not_called()
    
    

    

if __name__ == '__main__':
    unittest.main()