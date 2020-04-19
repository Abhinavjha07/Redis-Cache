# Redis-Cache

* Implemented two types of nodes to store the key, value pair. In some of the commands we needed to keep only one value corresponding to a key, while in some we needed to have multiple values with scores and sorted based on score. So, chose two different implementation of node.

**Definition of Node containing single value corresponding to a key.**
*  Class Node: {key, value, expire_time, prev, next}
* key => stores the key.
* value => stores value corresponding to the key
* expire_time: stores the expire time of the node in seconds.
* prev => to store the pointer to previous node, next => to store the pointer to next node

**Definition of Node containg list of values corresponding to a key.**
* Class ListNode: {key, values, scores, index_map, value_map, prev, next}
* key => key value
* values => stores the score of the values in sorted order
* index_map => stores the index of score in the values list, of a value
* value_map => stores the value corresponding to index in values array.


**Functionalities**

**Utility functions**
* *save(filename)*
* It saves(pickles) the cache object in the filename provided

* *set_data(hash_map, list_hash_map, head, end)*
* It sets the attribues of cache object

* *remove(node)*
* It removes the node and sets the pointer of its previous and next node

* *isExpired(node)*
* It checks whether the node has expired by comparing its expire time with the current time, return true if expired else False

* *delete_node(key)*
* It deletes the key from the hash map and calls  *remove* to remove the node from the list.

* *set_head(node)*
* It sets the currently inserted node as the head of the list of nodes.


**GET**
* *Input* - It takes input a key (GET key)
* *Output* - returns the value associated to key, if it exists, else returns nil

**SET**
* *Input* - It takes input a key, value, type-(NX/XX) and expire time(in seconds) (SET key value type NX/XX expire time)
* Expire time is attached to key and by default it is 10 minutes
* *Output* - It returns "OK" if success else returns "NULL"

**EXPIRE**
* *set_expire(key, expire_time)* It takes input the key and expire time. (EXPIRE key expire_time)
* *Output* - returns 1 if successful else 0 if key doesn't exist

**TTL**
* *get_TTL(key)* It takes input the key (TTL key)
* *Output* It returns the TTL of the key, if exists else returns -2 if it doesn't.

**ZADD**
* *Input* - It takes input key, type - (NX/XX), score value (ZADD key type (NX/XX/nothing) score value score value...)
* *Output* - Based on the type chosen it returns 0 or the number of keys added.

**ZRANK**
* *Input* - It takes input the key and value (ZRANK key value)
* *Output* - It returns the rank of the value in the sorted list based on scores

**ZRANGE**
* *Input* - It takes input the key, range values, and an WITHSCORES flag (ZRANGE key start end WITHSCORES(optional))
* *Output* - It returns the node values within the range and score, if flag is set.

**DEL**
* *Input* - It takes input the keys to delete (DEL key1 key2 ...)
* *Ouput* - It returns the number of deleted keys.

**GETSET**
* *Input* - It takes input the key, value (GETSET key value)
* *Output* - It returns the value set previously to that key

**MSET**
* *Input* - It takes input the key value pairs. (MSET key value key value ...)
* *Output* - It returns "OK"

**MGET**
* *Input* - It takes input the keys (MGET key1 key2 ...)
* *Output* - It return the value associated with the key else "(NIL)" if key doesn't exist




