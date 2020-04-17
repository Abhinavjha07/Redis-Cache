from Cache import Cache
import shlex


cache = Cache()
while True:
    option = int(input('Enter:\n1 to set\n2 to get\n3 to set expire time\n4 to get TTL\n5 for ZADD\n6 for ZRANK\n'))
    if option == 1:
        line = input('Enter the key, value and its attributes : ')
        line = shlex.split(line)
        
        attributes = {}
        key = line[0]
        for i in range(0, len(line), 2):
            attributes[line[i]] = line[i+1]

        print(attributes)
        print(cache.set(key, attributes[key], attributes))
    elif option == 2:
        key = input('Input : ')
        print(cache.get(key))

    elif option == 3:
        key, expire_time = input('Enter the key and expire time : ').split()

        print(cache.set_expire(key, int(expire_time)))
    elif option == 4:
        key = input('Enter the key : ')
        print(cache.get_TTL(key))

    elif option == 5:
        line = input('Input : ')
        line = shlex.split(line)
        key = line[0]
        ty = None
        x = 1
        if line[1] == "type":
            x += 2
            ty = line[2]
        values = []
        while x < len(line):
            values.append((int(line[x]), line[x+1]))
            x += 2

        print(values)
        
        print(cache.ZADD(key, ty, values))

    elif option == 6:
        line = input('Enter key and value : ')
        key, value = shlex.split(line)
        print(cache.ZRANK(key,value))
    




