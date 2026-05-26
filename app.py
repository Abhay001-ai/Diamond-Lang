from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)  # 🔥 this must come after the app is defined

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route("/run", methods=["POST"])
def run_diamond_code():
    data = request.json
    code = data.get("code", "")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{file_id}.dia")

    with open(file_path, "w") as f:
        f.write(code)

    try:
        # Replace with your actual Diamond Lang interpreter command
        result = subprocess.run(
            ["python", "diamond.py", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)

    os.remove(file_path)
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True)
