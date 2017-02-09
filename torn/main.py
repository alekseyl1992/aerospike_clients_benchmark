import aerospike
import json
from aerospike import predicates as p
from datetime import datetime

import random
import tornado as tornado
from tornado import gen
from tornado import web

from torn.utils import parse_options

options, args = parse_options()


class MainHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.write("Hello world!" + str(random.randint(0, 100)))
        self.finish()


class GetUserHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        query = client.query('test', 'sessions')

        _from = random.randint(0, 100)
        to = 100
        query.where(p.between('expires', _from, to))

        results = []

        def each_session(t):
            session = t[2]
            nick = session['nick']

            t = client.get(('test', 'users', nick))
            user = t[2]
            if user is not None:
                results.append(user['email'])

        query.foreach(each_session)

        self.write(json.dumps({
            'data': results,
            'version': 1,
            'date': str(datetime.now()),
        }))
        self.finish()


if __name__ == "__main__":
    config = {
        'hosts': [(options.host, options.port)]
    }

    client = aerospike.client(config).connect(
        options.username, options.password)

    namespace = options.namespace if options.namespace and options.namespace != 'None' else None

    routes = [
        (r"/", MainHandler),
        (r"/user", GetUserHandler),
    ]

    application = tornado.web.Application(routes)

    port = 8080
    application.listen(port)

    print('Server started on port {}'.format(port))

    tornado.ioloop.IOLoop.current().start()

    client.close()
