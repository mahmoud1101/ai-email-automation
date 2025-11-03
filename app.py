$code = @'
from flask import Flask, request, jsonify
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Load environment variables (set in Render environment settings)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route('/')
def home():
    return "✅ AI Email Automation is running!"

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        recipient = data.get('to')
        subject = data.get('subject')
        body = data.get('body')

        if not recipient or not subject or not body:
            return jsonify({"error": "Missing required fields"}), 400

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP server and send
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "✅ Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
'@

Set-Content -Path .\app.py -Value $code -Encoding UTF8
