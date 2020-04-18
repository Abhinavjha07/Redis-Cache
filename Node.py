from datetime import datetime, timedelta
from sortedcontainers import SortedList

class Node:
    def __init__(self, key, value, exp_time = 600):
        self.key = key
        self.value = value
        self.expire_time = datetime.now() + timedelta(seconds = int(exp_time))
        self.prev = None
        self.next = None

    def __str__(self):
        return "(%s, %s, %s)" %(self.key, self.value, self.expire_time)


class ListNode:
    def __init__(self, key, value, score = 0):
        self.key = key
        self.values = SortedList()
        self.values.add(score)
        self.index_map = {}
        self.value_map = {}
        self.index_map[value] = 0
        self.value_map[0] = value
        self.prev = None
        self.next = None
    
    def __str__(self):
        return "(%s, %s)" %(self.key, self.values)