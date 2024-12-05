from app.messaging import consume_messages

def handle_message(message):
    """Process the received message."""
    print(f"Processing message: {message}")

if __name__ == "__main__":
    consume_messages(handle_message)    