from Cache import Cache
import shlex
import pickle
from os import path
filename = 'redis_cache'

def load(filename):
    file = open(filename, "rb")
    data = pickle.load(file)
    return data

cache = Cache()
if path.exists(filename):
    data = load(filename)
    cache.set_data(data['hash_map'], data['list_hash_map'], data['head'], data['end'])


while True:
    command = input('Enter command : ')
    command = shlex.split(command)
    option = command[0]
    command = command[1:]
    try:
        if option == "SET":
            if len(command) < 2:
                print("ERR ERR wrong number of arguments for 'set' command")
                continue
            key = command[0]
            attributes = {}
            for i in range(0, len(command), 2):
                attributes[command[i]] = command[i+1]

            # print(attributes)
            print(cache.set(key, attributes[key], attributes))

        elif option == "GET":
            if len(command) != 1:
                print("ERR ERR wrong number of arguments for 'get' command")
                continue
            key = command[0]
            print(cache.get(key))
    
        elif option == "EXPIRE":
            if len(command) != 2:
                print("ERR ERR wrong number of arguments for 'expire' command")
                continue
            key = command[0]
            time = int(command[1])
            print(cache.set_expire(key, time))
        
        elif option == "TTL":
            if len(command) != 1:
                print("ERR ERR wrong number of arguments for 'ttl' command")
                continue
            key = command[0]
            print(cache.get_TTL(key))

        elif option == "ZADD":
            if len(command) & 1 == 0:
                print("ERR ERR wrong number of arguments for 'zadd' command")
                continue

            key = command[0]
            typ = None
            x = 1
            if command[1] == "type":
                x += 2
                typ = command[2]
            values = []
            while x < len(command):
                values.append((int(command[x]), command[x+1]))
                x += 2

            # print(values)
        
            print(cache.ZADD(key, typ, values))

        elif option == "ZRANK":
            if len(command) != 2:
                print("ERR ERR wrong number of arguments for 'zrank' command")
                continue
            key = command[0]
            value = command[1]
            print(cache.ZRANK(key,value))
        
        elif option == "ZRANGE":
            if len(command) > 4 or len(command) < 3:
                print("ERR ERR wrong number of arguments for 'zrange' command")
                continue

            key = command[0]
            l = int(command[1])
            r = int(command[2])
            withscore = False
            if len(command) == 4:
                withscore = True

            print(cache.ZRANGE(key, l, r, withscore))

        elif option == "exit":
            break

        elif option == "DEL":
            keys = []
            for key in command:
                keys.append(key)
            
            print(cache.DEL(keys))

        elif opion == "GETSET":
            if len(command) > 2:
                print("ERR ERR wrong number of arguments for 'getset' command")
                continue

            key = command[0]
            value = command[1]
            print(cache.GETSET(key, value))

        elif option == "MSET":
            if len(command) & 1 != 0:
                print("ERR ERR wrong number of arguments for 'mset' command")
                continue
            pair = []
            for i in range(0, len(command),2):
                pair.append((command[i], command[i+1]))

            print(cache.MSET(pair))
            
    except:
        print('Error occured!! please recheck the command.')
    finally:
        cache.save(filename)


cache.save(filename)

