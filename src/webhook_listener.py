# Webhook listener for Apify actor runs
from flask import Flask, request, jsonify
import json
import threading
from queue import Queue

app = Flask(__name__)

# Queue to hold webhook data
webhook_queue = Queue()

@app.route('/webhook/apify', methods=['POST'])
def webhook():
    """Receive webhook from Apify when an actor run finishes"""
    data = request.get_json()
    if data:
        webhook_queue.put(data)
        print(f"Received webhook: {data}")
        return jsonify({"status": "received"}), 200
    return jsonify({"error": "No data"}), 400

def run_webhook_server(port=5000):
    """Run the webhook server in a separate thread"""
    def run_app():
        app.run(host='0.0.0.0', port=port, debug=False)

    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()
    return thread

def get_webhook_data():
    """Get data from webhook queue"""
    if not webhook_queue.empty():
        return webhook_queue.get()
    return None
