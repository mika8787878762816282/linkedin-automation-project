
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import des blueprints
from src.routes.automation import automation_bp
from src.routes.zapier_integration import zapier_bp

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app) # Active CORS pour toutes les routes

# Enregistrement des blueprints
app.register_blueprint(automation_bp, url_prefix='/api')
app.register_blueprint(zapier_bp, url_prefix='/api')

# Route pour servir l'application React
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

# Route pour servir les autres fichiers statiques de React
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


