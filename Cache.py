from Node import Node, ListNode
from datetime import datetime, timedelta
import bisect

class Cache(object):
    def __init__(self):
        self.hash_map = {}
        self.list_hash_map = {}
        self.head = None
        self.end = None

    def remove(self, node):

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.end = node.prev

    def isExpired(self, node):
        if node.expire_time <= datetime.now():
            return True

        return False

    def delete_node(self, key):
        node = self.hash_map[key]
        del self.hash_map[key]
        self.remove(node)
        return 1


    def set_head(self, node):
        node.next = self.head
        node.prev = None
        if(self.head):
            self.head.prev = node

        self.head = node
        if not self.end:
            self.end = self.head


    def get(self, key):
        if key not in self.hash_map:
            return "(nil)"

        node = self.hash_map[key]

        if self.isExpired(node):
            self.delete_node(key)
        else:
            return self.hash_map[key]

    def set(self, key, value, attributes = None):
        print(attributes)
        expire = 600

        if(attributes.__contains__("expire")):
            expire = int(attributes["expire"])

        if attributes.__contains__("type"):
            if attributes["type"] == "XX":
                if key in self.hash_map:
                    node = self.hash_map[key]
                    if self.isExpired(node):
                        self.delete_node(key)
                        return "NULL"
                        

                    else:
                        node.expire_time = datetime.now() + timedelta(seconds = expire)

                        node.value = value
                        return "OK"

                else:
                    return "NULL"

            
            elif attributes["type"] == "NX":
                if key not in self.hash_map:
                    node = Node(key, value, expire)
                    self.set_head(node)
                    self.hash_map[key] = node

                    return "OK"
                else:
                    node = self.hash_map[key]
                    if self.isExpired(node):
                        node.value = value
                        return "OK"
                
                return "NULL"


    def set_expire(self, key, expire_time):
        if key in self.hash_map:
            node = self.hash_map[key]
            if self.isExpired(node):
                self.delete_node(key)

                return 0
            else:
                node.expire_time = datetime.now() + timedelta(seconds=expire_time)
            
                return 1
        return 0

    def get_TTL(self, key):
        if key not in self.hash_map:
            return -1
        else:
            node = self.hash_map[key]
            if self.isExpired(node):
                self.delete_node(key)

                return -1

            time_remaining = node.expire_time - datetime.now()

            return time_remaining

    
    def ZADD(self, key, type, values):

        if type == "XX":
            if key not in self.list_hash_map:
                return "(nil)"
            
            node = self.list_hash_map[key]
            for score, value in values:
                if value in node.index_map:
                    node.values.pop(node.index_map[value])
                    node.index_map[value] = bisect.bisect((score, value))
                    bisect.insort(node.values, (score, value))

            return 0

        elif type == "NX":
            if key not in self.list_hash_map:
                node = ListNode(key, '',0)
                node.values = []
                self.list_hash_map[key] = node
            else:
                node = self.list_hash_map[key]
            ans = 0
            for score, value in values:
                if value not in node.index_map:
                    if(len(node.values) == 0):
                        self.set_head(node)
                    node.index_map[value] = bisect.bisect(node.values,(score, value))
                    bisect.insort(node.values, (score, value))
                    ans += 1
            

            return ans

        else:
            if key not in self.list_hash_map:
                node = ListNode(key, '',0)
                node.values = []
                self.list_hash_map[key] = node
            else:
                node = self.list_hash_map[key]
            ans = 0
            for score, value in values:
                if value in node.index_map:
                    node.values.pop(node.index_map[value])
                else:
                    if(len(node.values) == 0):
                        self.set_head(node)
                    ans += 1
                
                node.index_map[value] = bisect.bisect(node.values,(score, value))
                bisect.insort(node.values, (score, value))
            
            return ans


    def ZRANK(self, key, value):
        if key not in self.list_hash_map:
            return "(nil)"

        node = self.list_hash_map[key]
        if value in node.index_map:
            return node.values[node.index_map[value]][0]
        return -1

                



