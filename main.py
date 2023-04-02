# python websocket client
import websocket

# Define the WebSocket URL
websocket_url = 'ws://localhost:3000/websocket/websocket'

# Define the callback function for receiving messages
def on_message(ws, message):
    print(f'Received message: {message}')

# Create a WebSocket instance and connect to the server
ws = websocket.ws(websocket_url, on_message=on_message)
ws.run_forever()
