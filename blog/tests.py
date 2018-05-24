from django.test import TestCase
import datetime
from collections import OrderedDict

# Create your tests here.

comment_list = [
    {'user_id': 1, 'content': '你猜我是谁', 'parent_comment': None},
    {'user_id': 2, 'content': '我怎么知道你是谁啊', 'parent_comment': None},
    {'user_id': 3, 'content': '你是谁关我什么事啊', 'parent_comment': 1},
    {'user_id': 4, 'content': '我是tom啊', 'parent_comment': 2},
    {'user_id': 5, 'content': '我是hurry啊', 'parent_comment': 3},
    {'user_id': 6, 'content': '我是hony啊', 'parent_comment': 1}
]

'''
1
    3
        5
    6    

2
    4
    
    
    {
    1: {'user_id': 1, 'content': '你猜我是谁', 'parent_comment': None, 'children_comment': []}, 
    2: {'user_id': 2, 'content': '我怎么知道你是谁啊', 'parent_comment': None, 'children_comment': []}, 
    3: {'user_id': 3, 'content': '你是谁关我什么事啊', 'parent_comment': 1, 'children_comment': []}, 
    4: {'user_id': 4, 'content': '我是tom啊', 'parent_comment': 2, 'children_comment': []}, 
    5: {'user_id': 5, 'content': '我是hurry啊', 'parent_comment': 3, 'children_comment': []}, 
    6: {'user_id': 6, 'content': '我是hony啊', 'parent_comment': 1, 'children_comment': []}}


    {1: {'user_id': 1, 'content': '你猜我是谁', 'parent_comment': None, 'children_comment': 
                            [{'user_id': 3, 'content': '你是谁关我什么事啊', 'parent_comment': 1, 'children_comment': [{'user_id': 5, 'content': '我是hurry啊', 'parent_comment': 3, 'children_comment': []}]}, {'user_id': 6, 'content': '我是hony啊', 'parent_comment': 1, 'children_comment': []}]}, 
    
    
    
    2: {'user_id': 2, 'content': '我怎么知道你是谁啊', 'parent_comment': None, 'children_comment': [{'user_id': 4, 'content': '我是tom啊', 'parent_comment': 2, 'children_comment': []}]}, 
    3: {'user_id': 3, 'content': '你是谁关我什么事啊', 'parent_comment': 1, 'children_comment': [{'user_id': 5, 'content': '我是hurry啊', 'parent_comment': 3, 'children_comment': []}]}, 
    4: {'user_id': 4, 'content': '我是tom啊', 'parent_comment': 2, 'children_comment': []}, 
    5: {'user_id': 5, 'content': '我是hurry啊', 'parent_comment': 3, 'children_comment': []}, 
    6: {'user_id': 6, 'content': '我是hony啊', 'parent_comment': 1, 'children_comment': []}}


'''

comment_order_comment = OrderedDict()

comment_dic = {}

for item in comment_list:
    item['children_comment'] = []
    comment_dic[item['user_id']] = item

    if item['parent_comment']:
        comment_dic[item['parent_comment']]['children_comment'].append(item)
    else:
        comment_order_comment[item['user_id']] = comment_dic[item['user_id']]


print(comment_order_comment)
