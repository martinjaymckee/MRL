import datetime

import flask
import flask_bootstrap
import flask_mako
import flask_socketio

import gevent
import gevent.pywsgi as wsgi

import camera_source

app = flask.Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'

bootstrap = flask_bootstrap.Bootstrap(app)
mako = flask_mako.MakoTemplates(app)
socketio = flask_socketio.SocketIO(app)

@app.route('/')
def index():
	return flask_mako.render_template('index.html', date=datetime.datetime.now())

@socketio.on('move', namespace='/mrl')
def move(cmd):
	msg = {
		'cmd' : 'move', # NOTE: THIS CAN BE SET
		'id' : 0, # NOTE: THIS SHOULD BE BASED UPON THE ID IN THE COMMAND
		'completed' : True # TODO: BUILD A SIMULATED ROBOT AND ONLY RETURN COMPLETED STATUS ON SUCCESS
	}
	print('Move Command -> {}'.format(cmd))
	return flask_socketio.emit('status', msg, broadcast=True)

@socketio.on('connect', namespace='/mrl')
def onConnect():
	pass

@socketio.on('disconnect', namespace='/mrl')
def onDisconnect():
	pass

def gen(camera):
	"""Video streaming generator function."""
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\nContent-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
	"""Video streaming route. Put this in the src attribute of an img tag."""
	files = ['static/images/frame_{}.png'.format(i) for i in range(1,8)]
	camera = camera_source.EmulatedCamera(files, 1.0/25.0)
	while camera.get_frame() is None:
		time.sleep(0)
	return flask.Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	http_server = wsgi.WSGIServer(('', 5000), app)
	http_server.serve_forever()
