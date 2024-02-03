import os
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory, make_response, redirect
import base64
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


# Create a share endpoint to create a share using a POST request, and return the share UUID
@app.route("/new-share", methods=["POST"])
def newshare():
    try:
        # Get the JSON data from the request body
        request_json = request.get_json()

        # Input validation
        if not request_json or not isinstance(request_json, dict):
            return jsonify({"error": "Invalid JSON data"}), 400

        text_data = request_json.get("text", "")
        name = request_json.get("name", "")
        is_public = request_json.get("public", False)

        # Additional input validation (customize as needed)
        if not text_data.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        if len(text_data) > 1000:  # Adjust the limit to your requirements
            return jsonify({"error": "Text exceeds the maximum allowed length"}), 400

        if not os.path.exists("/shares"):
            os.makedirs("/shares")

        share_uuid = str(uuid.uuid4())
        file_path = os.path.join("/shares", f"{share_uuid}.json")

        # File Path Sanitization
        if not file_path.startswith("/shares"):
            return jsonify({"error": "Invalid share ID"}), 400

        # Save data as JSON
        json_data = {"text": text_data, "name": name, "public": is_public}
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False)

        return jsonify({"share_uuid": share_uuid}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Define the share endpoint with shareid parameter
@app.route("/share/<shareid>")
def share(shareid):
    share_file_path = os.path.join("/shares", f"{shareid}.json")

    if not os.path.exists(share_file_path):
        return jsonify({"error": "Share not found"}), 404

    try:
        with open(share_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        share_content = json_data.get("text", "")
        return share_content

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/public-shares")
def public_shares():
    public_shares_list = []

    shares_directory = "/shares"
    for filename in os.listdir(shares_directory):
        file_path = os.path.join(shares_directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)

                if json_data.get("public", False):
                    public_shares_list.append({
                        "share_uuid": filename.split(".")[0],  # Extract share_uuid from filename
                        "name": json_data.get("name", ""),
                        "text": json_data.get("text", "")
                    })

            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return jsonify(public_shares_list), 200


# Define the endpoint to render the shared text visualizer HTML for the given shareid parameter (UUID)
@app.route("/vis/shares/<shareid>")
def visualize_share(shareid):
    # Ensure that the UUID is valid before rendering the template
    try:
        uuid.UUID(shareid)
    except ValueError:
        return redirect("/404/shares")

    # Render the share_visualizer.html template
    return render_template("share_visualizer.html")

@app.route('/main.js')
def serve_js():
    return send_from_directory(os.path.join(app.root_path, 'Static'), 'mainjs.js', mimetype='application/javascript')

@app.route('/main.js')
def serve_css():
    return send_from_directory(os.path.join(app.root_path, 'Static'), 'styles.css', mimetype='text/css')

@app.route('/sharesmain.css')
def serve_shares_css():
    return send_from_directory(os.path.join(app.root_path, 'Static'), 'sharesmain.css', mimetype='text/css')

@app.route('/404/shares')
def serve_404_error():
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
