from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receives webhook requests from Notion and triggers a script."""
    data = request.json  # Capture webhook data

    if data:
        print(f"✅ Webhook received: {data}")
        print("🚀 Running Python script...")
        os.system("python backend/main.py")  # Adjust the script path as needed
        return {"status": "success", "message": "Script executed!"}, 200
    else:
        return {"status": "failed", "message": "No data received."}, 400

if __name__ == "__main__":
    print("📌 Webhook server running on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)