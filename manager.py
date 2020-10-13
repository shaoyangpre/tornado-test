import logging
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line

from app.bootloader import settings
from app.lib.route import Route
from app.models import objects
from app.handler import user

define('cmd', default='runserver', metavar='runserver')
define('port', default=8080, type=int)
logging.basicConfig(level=logging.INFO)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [tornado.web.url(r"/upload/(.+)", tornado.web.StaticFileHandler, dict(path=settings['UPLOAD_PATH']), name='upload_path')
                   ] + Route.routes()
        tornado.web.Application.__init__(self, handlers, **settings, debug=True)


def runserver():
    app = Application()
    app.objects = objects
    http_server = HTTPServer(app, xheaders=True)
    http_server.listen(options.port)

    loop = tornado.ioloop.IOLoop.instance()

    logging.info('Servers running on http://0.0.0.0:%d' % (options.port))
    loop.start()


if __name__ == '__main__':
    parse_command_line()
    runserver()
