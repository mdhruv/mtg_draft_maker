import os
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from magic_set import Card
from magic_set import Normal_Mythic_Rare_Set
from magic_set_library import Magic_Set_Library

class Server(object):

	def __init__(self, config):
		self.url_map = Map([
			Rule('/', endpoint='generate_buy_list'),
		])
		self.magic_set_library = Magic_Set_Library()
	
	def generate_buy_list(self, request):
		params = self._parse_query_string(request.query_string)
		boosters = []
		for magic_set, booster_count in params.iteritems():
			for i in range(int(booster_count)):
				boosters.append(self.magic_set_library.make_booster(magic_set))
		card_map = {}
		for booster in boosters:
			for card in booster:
				card_map[card] = card_map.get(card, 0) + 1
		ret_str = ""
		for card, count in sorted(card_map.iteritems(), key=lambda x:x[0]):
			ret_str += "%s %s\n" %(count, card.name)
		return Response(ret_str)
	
	def _parse_query_string(self, query_string):
		if not query_string:
			return {}
		return dict(map(lambda x:(x.split('=')[0], x.split('=')[1]), query_string.strip().split('&')))

	def dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, endpoint)(request, **values)
		except HTTPException, e:
			return e

	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request)
		return response(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)


def create_app(with_static=True):
	app = Server({})
	if with_static:
		app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
			'/static':  os.path.join(os.path.dirname(__file__), 'static')
		})
	return app

if __name__ == '__main__':
	from werkzeug.serving import run_simple
	app = create_app()
	run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
