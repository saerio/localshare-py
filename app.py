import os
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory, make_response, redirect
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


# Create a share endpoint to create a share using a POST request, and return the share UUID
@app.route("/new-share", methods=["POST"])
def newshare():
    try:
        # Get the text data from the request body
        text_data = request.get_data(as_text=True)

        # Input validation (check if data is not empty and within acceptable limits)
        if not text_data.strip():
            return jsonify({"error": "Data cannot be empty"}), 400
        if len(text_data) > 100:  # Adjust the limit to your requirements
            return jsonify({"error": "Data exceeds the maximum allowed length"}), 400

        if not os.path.exists("/shares"):
            os.makedirs("/shares")

        share_uuid = str(uuid.uuid4())
        file_path = os.path.join("/shares", f"{share_uuid}.txt")  # Use '.txt' extension for plain text data

        # File Path Sanitization
        if not file_path.startswith("/shares"):
            return jsonify({"error": "Invalid share ID"}), 400

        with open(file_path, 'w', encoding='utf-8') as file:  # Specify encoding for writing as UTF-8
            file.write(text_data)  # Write the UTF-8 plain text data to the file

        return jsonify({"share_uuid": share_uuid}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define the share endpoint with shareid parameter
@app.route("/share/<shareid>")
def share(shareid):
    share_file_path = os.path.join("/shares", f"{shareid}.txt")

    if not os.path.exists(share_file_path):
        return jsonify({"error": "Share not found"}), 404

    with open(share_file_path, 'r', encoding='utf-8') as file:  # Read the file as UTF-8
        share_content = file.read()

    return share_content

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
