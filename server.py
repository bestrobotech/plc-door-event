from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from opcua import Client
from opcua import ua

app = Flask(__name__, template_folder='client')
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

client = Client("opc.tcp://192.168.1.11:4840")

@app.route('/')
def index():
    return render_template('door.html')


up_event = ua.DataValue(ua.Variant([True, False, False], ua.VariantType.Boolean))
down_event = ua.DataValue(ua.Variant([False, True, False], ua.VariantType.Boolean))
stop_event = ua.DataValue(ua.Variant([False, False, True], ua.VariantType.Boolean))

@socketio.on('door_event')
def door_event(message):
    try:
        client.connect()

        plc_array = client.get_node("ns=4;s=PLC_ARRAY")

        if message == "up":
            plc_array.set_value(up_event)
        if message == "down":
            plc_array.set_value(down_event)
        if message == "stop":
            plc_array.set_value(stop_event)

        status_array = plc_array.get_value()
        if status_array[0]:
            emit('door_status', 'Up')
        if status_array[1]:
            emit('door_status', 'Down')
        if status_array[2]:
            emit('door_status', 'Stoped')
    except Exception as e:
        emit('door_status', str(e))
    finally:
        try:
            client.disconnect()
        except:
            pass

if __name__ == '__main__':
    socketio.run(app, port=80)
