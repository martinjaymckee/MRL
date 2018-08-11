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

@app.route('/')
def hello():
	return flask_mako.render_template('index.html', date=datetime.datetime.now())

@socketio.on('message', namespace='/test')
def echo(message):
	msg = {
		"user" : "Max",
		"text" : message['text']
	}
	return flask_socketio.emit('message', msg, broadcast=True)

@socketio.on('connect', namespace='/test')
def onConnect():
	print("*** Connected!")
	who = 'localhost'
	msg = { "text" : "{} Connected".format(who) }
	return flask_socketio.emit('message', msg, broadcast=True)

@socketio.on('disconnect', namespace='/test')
def onDisconnect():
	print("*** Disconnected")
	who = 'localhost'
	msg = { "text" : "{} Disconnected".format(who)}
	return flask_socketio.emit('message', msg, broadcast=True)

if __name__ == '__main__':
	http_server = wsgi.WSGIServer(('', 5000), app)
	http_server.serve_forever()
	#app.run(debug=True)
