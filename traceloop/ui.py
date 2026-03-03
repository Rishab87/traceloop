from flask import Flask, render_template, jsonify
from .storage import list_runs, get_run

# Flask will automatically look for 'templates' in the same folder as this module
app = Flask(__name__)

@app.route("/")
def index():
    runs = list_runs()
    return render_template("index.html", runs=runs)

@app.route("/api/runs/<run_id>")
def run_detail(run_id):
    run = get_run(run_id)
    if not run:
        return jsonify({"error": "Not found"}), 404
    return jsonify(run)

def run_server():
    app.run(port=4999, debug=False)

if __name__ == "__main__":
    run_server()
