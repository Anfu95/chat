from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # return 'Hello world'
    data = {
        'titulo': 'index',
        'bienvenida': 'Saludos'
    }
    return render_template('index.html', data=data)

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room )
    else:
        return redirect(url_for('home'))

# users = {}
# @socketio.on('disconnect')
# def on_disconnect():
#     users.pop(request.sid,'No user found')
#     socketio.emit('current_users', users)
#     print("User disconnected!\nThe users are: ", users)

# @socketio.on('sign_in')
# def user_sign_in(user_name, methods=['GET', 'POST']):
#     users[request.sid] = user_name['name']
#     socketio.emit('current_users', users)
#     print("New user sign in!\nThe users are: ", users)

# @socketio.on('message')
# def messaging(message, methods=['GET', 'POST']):
#     print('received message: ' + str(message))
#     message['from'] = request.sid
#     socketio.emit('message', message, room=request.sid)
#     socketio.emit('message', message, room=message['to']
@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} ha enviado un mensaje a la sala {}".format(data['username'],
                                                                   data['room'],
                                                                   data['message']
                                                                   ))
    socketio.emit('receive_message', data, room=data["room"])

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} alguien se ha unido a la sala {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    socketio.run(app, debug=True)