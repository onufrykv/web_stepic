def wsgi_app(environ, start_response):
    params = '\n'.join(environ['QUERY_STRING'].split('&'))
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [params]
