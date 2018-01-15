# -*- coding: UTF-8 -*-

import tornado.web
from tornado.ioloop import IOLoop
from init_bot import init_facebook
from handlers import MainHandler
from settings import TORNADO_PORT

application = tornado.web.Application([
    ('/', MainHandler)
])

application.listen(TORNADO_PORT)
init_facebook()
IOLoop.instance().start()
