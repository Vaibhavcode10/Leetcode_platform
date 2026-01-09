from flask import Flask, request, jsonify
import os
import re

app = Flask(__name__)

STUDENT_ROOT = "/data/studentlist"

def sanitize_email(email):
    return re.sub(r'[^a-z0-9]', '_', email.lower())

@app.route("/student/login", methods=["POST"])
def student_login():
    data = request.get_json()
    email = data.get("email")

    if not email or "@" not in email:
        return jsonify({"error": "invalid email"}), 400

    student_id = sanitize_email(email)
    student_path = os.path.join(STUDENT_ROOT, student_id)

    if os.path.exists(student_path):
        return jsonify({
            "status": "old",
            "message": f"hello {email}"
        })

    os.makedirs(student_path)
    return jsonify({
        "status": "new",
        "message": f"folder created for {email}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
