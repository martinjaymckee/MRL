import datetime

import flask
import flask_bootstrap
import flask_mako
import flask_socketio

import gevent
import gevent.pywsgi as wsgi

app = flask.Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'

bootstrap = flask_bootstrap.Bootstrap(app)
mako = flask_mako.MakoTemplates(app)
socketio = flask_socketio.SocketIO(app)

counter = 0

@app.route('/')
def index():
	return flask_mako.render_template('index.html', date=datetime.datetime.now())

@socketio.on('move', namespace='/mrl')
def move(cmd):
	global counter
	msg = {
		'cmd' : 'move', # NOTE: THIS CAN BE SET
		'id' : counter%3, # NOTE: THIS SHOULD BE BASED UPON THE ID IN THE COMMAND
		'completed' : True # TODO: BUILD A SIMULATED ROBOT AND ONLY RETURN COMPLETED STATUS ON SUCCESS
	}
	counter += 1
	return flask_socketio.emit('status', msg, broadcast=True)

@socketio.on('connect', namespace='/mrl')
def onConnect():
	pass

@socketio.on('disconnect', namespace='/mrl')
def onDisconnect():
	pass

if __name__ == '__main__':
	http_server = wsgi.WSGIServer(('', 5000), app)
	http_server.serve_forever()
