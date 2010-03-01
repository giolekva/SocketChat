import os

import tornado.httpserver
import tornado.ioloop
import tornado.web

import views

settings = {
	'static_path': os.path.join(os.path.dirname(__file__), 'static'),
	'template_path': os.path.dirname(__file__),
}

application = tornado.web.Application([
	(r'/message$', views.MessageHandler),
	(r'/$', views.MainHandler),
], **settings)

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8000)
	
	tornado.ioloop.IOLoop.instance().start()
