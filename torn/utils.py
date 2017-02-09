from optparse import OptionParser

import random
from random_words import RandomWords
from random_words import RandomEmails

rw = RandomWords()
re = RandomEmails()


def generate_nick():
    return rw.random_word() + str(random.randint(10000000, 90000000))


def generate_user_record():
    tiles_count = random.randint(20, 100)
    tiles = []
    for i in range(tiles_count):
        tiles.append({
            'url': rw.random_word(),
            'name': rw.random_word()
        })

    nick = generate_nick()
    record = {
        'nick': nick,
        'first_name': rw.random_word(),
        'last_name': rw.random_word(),
        'age': random.randint(10, 100),
        'email': re.randomMail(),
        'tiles': tiles
    }

    return record


def generate_session_record(user):
    record = {
        'nick': user['nick'],
        'expires': random.randint(0, 100)
    }

    _id = random.randint(10000000, 90000000)

    return _id, record


def fill_db(client, ns):
    # remove all data
    scan = client.scan(ns, 'users')
    scan.foreach(lambda t: client.remove(t[0]))

    scan = client.scan(ns, 'sessions')
    scan.foreach(lambda t: client.remove(t[0]))

    # populate DB
    users_count = 10000
    for i in range(users_count):
        if i % 1000 == 0:
            progress = float(i) / users_count * 100
            print('Progress: {}%'.format(int(progress)))

        user = generate_user_record()
        key = (ns, 'users', user['nick'])
        client.put(key, user)

        if random.randint(0, 100) > 50:
            _id, record = generate_session_record(user)
            key = (ns, 'sessions', _id)
            client.put(key, record)


def parse_options():
    usage = "usage: %prog [options] key"

    optparser = OptionParser(usage=usage, add_help_option=False)

    optparser.add_option(
        "-U", "--username", dest="username", type="string", metavar="<USERNAME>",
        help="Username to connect to database.")

    optparser.add_option(
        "-P", "--password", dest="password", type="string", metavar="<PASSWORD>",
        help="Password to connect to database.")

    optparser.add_option(
        "-h", "--host", dest="host", type="string", default="127.0.0.1", metavar="<ADDRESS>",
        help="Address of Aerospike server.")

    optparser.add_option(
        "-p", "--port", dest="port", type="int", default=3000, metavar="<PORT>",
        help="Port of the Aerospike server.")

    optparser.add_option(
        "-n", "--namespace", dest="namespace", type="string", default="test", metavar="<NS>",
        help="Port of the Aerospike server.")

    optparser.add_option(
        "-s", "--set", dest="set", type="string", default="demo", metavar="<SET>",
        help="Port of the Aerospike server.")

    optparser.add_option(
        "--gen", dest="gen", type="int", default=5, metavar="<GEN>",
        help="Generation of the record being written.")

    optparser.add_option(
        "--ttl", dest="ttl", type="int", default=1000, metavar="<TTL>",
        help="TTL of the record being written.")

    return optparser.parse_args()
