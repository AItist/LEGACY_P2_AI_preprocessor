import websocket

# Define the WebSocket URL
websocket_url = "ws://localhost:8080/"

# Define the WebSocket message handler
def on_message(ws, message):
    print("Received message: ", message)

# Define the WebSocket error handler
def on_error(ws, error):
    print("Error: ", error)

# Define the WebSocket connection closed handler
def on_close(ws):
    print("Connection closed")

# Define the WebSocket open handler
def on_open(ws):
    print("Connection opened")
    # Send a message to the server
    ws.send("Hello, server!")

# Create the WebSocket client and assign the handlers
ws = websocket.WebSocketApp(websocket_url,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)

# Assign the open handler separately
ws.on_open = on_open

# Start the WebSocket client
ws.run_forever()
