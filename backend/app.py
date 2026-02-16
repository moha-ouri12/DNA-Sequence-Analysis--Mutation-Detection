from flask import Flask, render_template, request, jsonify, send_from_directory
import os



BASE = os.path.dirname(os.path.abspath(__file__))
FRONT = os.path.join(BASE, "..", "frontend")

app = Flask(__name__, template_folder=FRONT, static_folder=FRONT)

from dna_utils import analyze_sequence , compare_sequences_dna

@app.route("/")
def home():
    return render_template("index.html")

# AJOUTE CES ROUTES pour servir les fichiers CSS/JS
@app.route("/style.css")
def serve_css():
    return send_from_directory(app.static_folder, "style.css")

@app.route("/script.js")
def serve_js():
    return send_from_directory(app.static_folder, "script.js")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json()  # json --> dictionnaire
    seq = data.get("sequence", "")
    result = analyze_sequence(seq)
    return jsonify(result)

@app.route("/api/compare", methods=['POST'])
def api_compare():
    data = request.get_json()
    seqA = data.get("sequenceA", "")
    seqB = data.get("sequenceB", "")
    
    # Appel de la nouvelle fonction dans dna_utils
    result = compare_sequences_dna(seqA, seqB)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8191)