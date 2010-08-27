# This is Python example on how to use Mongoose embeddable web server,
# http://code.google.com/p/mongoose
#
# Before using the mongoose module, make sure that Mongoose shared library is
# built and present in the current (or system library) directory

import mongoose
import sys

# Handle /show and /form URIs.
def uri_handler(conn, info):
	if info.uri == '/show':
		conn.printf('%s', 'HTTP/1.0 200 OK\r\n')
		conn.printf('%s', 'Content-Type: text/plain\r\n\r\n')
		conn.printf('%s %s\n', info.request_method, info.uri)
		if info.request_method == 'POST':
			content_len = conn.get_header('Content-Length')
			post_data = conn.read(int(content_len))
			my_var = conn.get_var(post_data, 'my_var')
		else:
			my_var = conn.get_qsvar(info, 'my_var')
		conn.printf('my_var: %s\n', my_var or '<not set>')
		conn.printf('HEADERS: \n')
		for header in info.http_headers[:info.num_headers]:
			conn.printf('  %s: %s\n', header.name, header.value)
		return mongoose.MG_SUCCESS
	elif info.uri == '/form':
		conn.write('HTTP/1.0 200 OK\r\n'
			   'Content-Type: text/html\r\n\r\n'
			   'Use GET: <a href="/show?my_var=hello">link</a>'
			   '<form action="/show" method="POST">'
			   'Use POST: type text and submit: '
			   '<input type="text" name="my_var"/>'
			   '<input type="submit"/>'
			   '</form>')
		return mongoose.MG_SUCCESS
	else:
		return mongoose.MG_ERROR

# Invoked each time HTTP error is triggered.
def error_handler(conn, info):
	conn.printf('%s', 'HTTP/1.0 200 OK\r\n')
	conn.printf('%s', 'Content-Type: text/plain\r\n\r\n')
	conn.printf('HTTP error: %d\n', info.status_code)
	return mongoose.MG_SUCCESS

# Create mongoose object, and register '/foo' URI handler
# List of options may be specified in the contructor
server = mongoose.Mongoose(document_root='/tmp',
			   new_request_handler=uri_handler,
			   http_error_handler=error_handler,
			   listening_ports='8080')

print 'Starting Mongoose server, press enter to quit'
sys.stdin.read(1)

# Deleting server object stops all serving threads
print 'Stopping server.'
del server
