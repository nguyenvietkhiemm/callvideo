from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pyngrok import ngrok
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép CORS

# Mở một ngrok tunnel
ngrok.set_auth_token("2pIXCMwoh5HrCE7cV6bKETCLZkY_6eU9Nz5W37cUeRkyFwjfz")
public_url = ngrok.connect(5000)

print(f"Ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")
CORS(app, resources={r"/*": {"origins": "*"}})  # Cho phép tất cả nguồn gốc

# Trang chủ của ứng dụng
@app.route('/')
def index():
    return render_template(f'index.html')

# Sự kiện cho việc trao đổi tín hiệu WebRTC
@socketio.on('offer')
def handle_offer(data):
    print("OFFER", data)
    emit('offer', data, broadcast=True, include_self=False)  # Loại trừ chính sender

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True, include_self=False)  # Loại trừ chính sender

@socketio.on('data')
def handle_data(data):
    print("DATA", data)
    emit('data', data, broadcast=True, include_self=False)  # Loại trừ chính sender

@socketio.on('candidate')
def handle_candidate(data):
    emit('candidate', data, broadcast=True, include_self=False)  # Loại trừ chính sender

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
