
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from src.application_tracker import get_all_applications

automation_bp = Blueprint("automation", __name__)

# Variable d'état simple pour l'automatisation (à remplacer par une base de données ou un système plus robuste)
automation_running = False

@automation_bp.route("/automation/status", methods=["GET"])
@cross_origin()
def get_automation_status():
    """Obtenir le statut du système d'automatisation"""
    global automation_running
    status = "active" if automation_running else "stopped"
    message = "Système d'automatisation opérationnel" if automation_running else "Le système est en pause"
    return jsonify({"status": status, "message": message})

@automation_bp.route("/automation/start", methods=["POST"])
@cross_origin()
def start_automation():
    """Démarrer le processus d'automatisation"""
    global automation_running
    automation_running = True
    return jsonify({"status": "started", "message": "Automatisation démarrée avec succès"})

@automation_bp.route("/automation/stop", methods=["POST"])
@cross_origin()
def stop_automation():
    """Arrêter le processus d'automatisation"""
    global automation_running
    automation_running = False
    return jsonify({"status": "stopped", "message": "Automatisation arrêtée avec succès"})

@automation_bp.route("/automation/applications", methods=["GET"])
@cross_origin()
def get_applications():
    """Obtenir la liste des candidatures"""
    applications = get_all_applications()
    # Adapter le format pour le frontend si nécessaire
    formatted_applications = []
    for app in applications:
        formatted_applications.append({
            "id": app["job_id"],
            "company": app["company"],
            "position": app["position"],
            "status": app["status"],
            "date": app["date_applied"].split("T")[0] # Format YYYY-MM-DD
        })
    return jsonify(formatted_applications)

@automation_bp.route("/automation/webhook", methods=["POST"])
@cross_origin()
def webhook_handler():
    """Gestionnaire de webhook pour Zapier (sera géré par zapier_integration.py)"""
    return jsonify({
        "status": "info",
        "message": "Ce webhook est maintenant géré par /api/zapier/webhook/linkedin-email"
    }), 200


