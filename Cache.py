from Node import Node, ListNode
from datetime import datetime, timedelta
import bisect
from sortedcontainers import SortedList
import pickle

class Cache(object):
    def __init__(self):
        self.hash_map = {}
        self.list_hash_map = {}
        self.head = None
        self.end = None

    def save(self, filename):
        data = {
            "hash_map" : self.hash_map,
            "list_hash_map": self.list_hash_map,
            "head": self.head,
            "end": self.end
        }

        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def set_data(self, hash_map, list_hash_map, head, end):
        self.hash_map = hash_map
        self.list_hash_map = list_hash_map
        self.head = head
        self.end = end

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
            return "(nil)"
        else:
            return self.hash_map[key].value

    def insert(self, key, value, expire):
        if key in self.hash_map:
            node = self.hash_map[key]
            node.expire_time = datetime.now() + timedelta(seconds= expire)
            node.value = value
            return "OK"
        else:
            node = Node(key, value, expire)
            self.set_head(node)
            self.hash_map[key] = node
            return "OK"


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
                        node.expire_time = datetime.now() + timedelta(seconds= expire)
                        node.value = value
                        return "OK"
                
                return "NULL"
            else:
                return "Unrecognized type!!"

        else:
            self.insert(key, value,expire)
            return "OK"


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
            return -2
        else:
            node = self.hash_map[key]
            if self.isExpired(node):
                self.delete_node(key)

                return -2

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
                    del node.value_map[node.index_map[value]]
                    node.index_map[value] = bisect.bisect(node.values, score)
                    node.values.add(score)
                    node.value_map[node.index_map[value]] = value

            return 0

        elif type == "NX":
            if key not in self.list_hash_map:
                node = ListNode(key, '',0)
                node.values = SortedList()
                node.index_map = {}
                node.value_map = {}
                self.list_hash_map[key] = node
            else:
                node = self.list_hash_map[key]
            ans = 0
            for score, value in values:
                if value not in node.index_map:
                    if(len(node.values) == 0):
                        self.set_head(node)

                    del node.value_map[node.index_map[value]]
                    node.index_map[value] = bisect.bisect(node.values, score)
                    node.values.add(score)
                    node.value_map[node.index_map[value]] = value
                    ans += 1
            

            return ans

        else:
            if key not in self.list_hash_map:
                node = ListNode(key, '',0)
                node.values = SortedList()
                node.index_map = {}
                node.value_map = {}
                self.list_hash_map[key] = node
            else:
                node = self.list_hash_map[key]
            ans = 0
            for score, value in values:
                if value in node.index_map:
                    del node.value_map[node.index_map[value]]
                    node.values.pop(node.index_map[value])
                else:
                    if(len(node.values) == 0):
                        self.set_head(node)
                    ans += 1
                
                node.index_map[value] = bisect.bisect(node.values, score)
                node.value_map[node.index_map[value]] = value
                node.values.add(score)
            
            return ans


    def ZRANK(self, key, value):
        if key not in self.list_hash_map:
            return "(nil)"

        node = self.list_hash_map[key]
        if value in node.index_map:
            return node.values[node.index_map[value]]
        return "(nil)"

    # def all_node(self):
    #     node = self.head
    #     while node != None:
    #         print(node)
    #         node = node.next

    
    def ZRANGE(self, key, l, r, withScore = False):
        if key not in self.list_hash_map:
            return "(nil)"

        node = self.list_hash_map[key]
        res = []
        if l < 0:
            l = len(node.values) + l 
        if r < 0:
            r = len(node.values) + r + 1

        

        for i in range(l, r):
            res.append(node.value_map[i])
            if withScore:
                res.append(node.values[i])

        return res


    def DEL(self, keys):
        ans = 0
        for key in keys:
            if key in self.hash_map:
                if self.delete_node(key) == 1:
                    ans += 1

        
        return ans


    def GETSET(self, key, value):
        if key not in self.hash_map:
            return "(nil)"

        node = self.hash_map[key]
        ans = node.value
        if self.isExpired(node):
            self.delete_node(key)
            return "(nil)"
        else:
            node.value = value
        return ans

    def MSET(self, pairs):
        for key, value in pairs:
            if key in self.hash_map:
                
                node = self.hash_map[key]
                node.value = value
                node.expire_time = datetime.now() + timedelta(seconds=600)
            else:
                node = Node(key, value)
                self.set_head(node)
                self.hash_map[key] = node

        return "OK"


        
            


                



