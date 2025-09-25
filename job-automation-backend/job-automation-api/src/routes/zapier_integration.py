
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import logging
import os
from datetime import datetime

from src.cv_generator import generate_cv_pdf
from src.github_project_creator import create_github_project
from src.email_automation import send_automated_response
from src.job_analyzer import analyze_job_offer
from src.application_tracker import track_application

zapier_bp = Blueprint("zapier", __name__)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Informations de profil et tokens (à charger depuis des variables d'environnement en production) ---
PROFILE_INFO = {
    "name": "Michaël Sibony",
    "email": "Michaelsibony0@gmail.com",
    "phone": "+33 6 12 34 56 78",
    "linkedin": "https://www.linkedin.com/in/michaelsibony/",
    "summary": "Développeur Full Stack passionné avec 5 ans d'expérience dans le développement web et mobile, spécialisé en React, Node.js et Python.",
    "skills": ["React", "Node.js", "Python", "Flask", "JavaScript", "HTML", "CSS", "SQL", "NoSQL", "AWS", "Docker"],
    "experience": "Développeur Senior chez Tech Solutions (2022-Présent) - Développement et maintenance d'applications web complexes. Développeur Junior chez Web Innovations (2020-2022) - Contribution au développement de nouvelles fonctionnalités.",
    "education": "Master en Informatique, Université de Paris (2019)"
}

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# -------------------------------------------------------------------------------------------------------

@zapier_bp.route("/zapier/webhook/linkedin-email", methods=["POST"])
@cross_origin()
def handle_linkedin_email_webhook():
    """
    Webhook pour recevoir les e-mails LinkedIn de Zapier.
    Orchestre le processus complet de candidature.
    """
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Webhook LinkedIn reçu sans données.")
            return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400
        
        email_subject = data.get("subject", "")
        email_body = data.get("body", "")
        sender = data.get("sender", "")
        
        logger.info(f"E-mail LinkedIn reçu de {sender}: {email_subject}")
        
        # 1. Analyse du type de poste et de l'offre
        job_type = analyze_job_type(email_subject, email_body) # Fonction du fichier zapier_integration.py
        job_details = analyze_job_offer({"subject": email_subject, "body": email_body})
        
        job_title = job_details.get("title", "Poste inconnu")
        company_name = job_details.get("company", "Entreprise inconnue")
        
        # Générer un ID unique pour la candidature
        job_id = f"app_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(email_subject) % 10000}"

        # 2. Suivi de la candidature (initialisation)
        track_application(job_id, company_name, job_title, "Reçue - En traitement", job_details)

        # 3. Génération du CV personnalisé (PDF)
        cv_filename = f"cv_{PROFILE_INFO['name'].replace(' ', '_')}_{company_name.replace(' ', '_')}.pdf"
        generate_cv_pdf(PROFILE_INFO, job_details, cv_filename)
        logger.info(f"CV PDF généré: {cv_filename}")

        # 4. Création d'un projet GitHub réel
        project_name = f"Projet_{job_title.replace(' ', '_')}_{company_name.replace(' ', '_')}"
        github_project_url = create_github_project({
            "name": project_name,
            "description": f"Projet de démonstration pour le poste de {job_title} chez {company_name}.",
            "private": False
        }, GITHUB_TOKEN)
        logger.info(f"Projet GitHub créé: {github_project_url}")

        # 5. Envoi de la réponse automatique
        response_subject = f"Candidature pour le poste de {job_title} chez {company_name}"
        response_body = f"""Bonjour,\n\nJe vous remercie pour l'opportunité de postuler au poste de {job_title} chez {company_name}.\n\nVous trouverez ci-joint mon CV personnalisé pour ce poste. Vous pouvez également consulter un projet pertinent sur GitHub : {github_project_url}\n\nJe suis très enthousiaste à l'idée de discuter de cette opportunité.\n\nCordialement,\n{PROFILE_INFO['name']}"""
        
        # Assurez-vous que l'expéditeur est une adresse valide pour envoyer la réponse
        # Pour l'instant, nous envoyons à l'expéditeur de l'e-mail LinkedIn
        send_success = send_automated_response(GMAIL_ADDRESS, GMAIL_APP_PASSWORD, sender, response_subject, response_body, attachments=[cv_filename])
        
        if send_success:
            track_application(job_id, company_name, job_title, "Envoyée - Réponse automatique", {"github_url": github_project_url, "cv_file": cv_filename})
            logger.info(f"Réponse automatique envoyée à {sender}.")
        else:
            track_application(job_id, company_name, job_title, "Échec envoi réponse", {"github_url": github_project_url, "cv_file": cv_filename})
            logger.error(f"Échec de l'envoi de la réponse automatique à {sender}.")

        # Nettoyage du fichier CV temporaire
        if os.path.exists(cv_filename):
            os.remove(cv_filename)

        return jsonify({
            "status": "success",
            "message": "Processus de candidature automatisé terminé.",
            "job_type": job_type,
            "job_details": job_details,
            "github_project_url": github_project_url,
            "email_sent": send_success
        })
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement du webhook LinkedIn: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"Erreur lors du traitement: {str(e)}"
        }), 500

def analyze_job_type(subject, body):
    """
    Analyse le contenu de l'e-mail pour déterminer le type de poste.
    """
    content = (subject + " " + body).lower()
    
    job_types = {
        "developpement_web": ["développeur web", "frontend", "backend", "full stack", "react", "angular", "vue", "javascript", "html", "css"],
        "data_science": ["data scientist", "machine learning", "ia", "intelligence artificielle", "python", "r", "tensorflow", "pytorch"],
        "devops": ["devops", "infrastructure", "cloud", "aws", "azure", "docker", "kubernetes", "ci/cd"],
        "mobile": ["développeur mobile", "android", "ios", "react native", "flutter", "swift", "kotlin"],
        "cybersecurite": ["cybersécurité", "sécurité informatique", "pentesting", "ethical hacking"],
        "gestion_projet": ["chef de projet", "scrum master", "product owner", "agile"],
        "general": []  # Type par défaut
    }
    
    scores = {}
    for job_type, keywords in job_types.items():
        score = sum(1 for keyword in keywords if keyword in content)
        scores[job_type] = score
    
    best_match = max(scores, key=scores.get)
    
    if scores[best_match] == 0:
        return "general"
    
    return best_match

def route_to_specialized_ai(job_type, email_data):
    """
    Simule le routage de l'e-mail vers l'IA spécialisée appropriée.
    Dans une implémentation réelle, cela ferait un appel HTTP vers un autre service.
    """
    ai_specialists = {
        "developpement_web": {
            "name": "WebDev AI Specialist",
            "endpoint": "/api/ai/webdev",
            "description": "IA spécialisée en développement web"
        },
        "data_science": {
            "name": "DataScience AI Specialist",
            "endpoint": "/api/ai/datascience",
            "description": "IA spécialisée en data science et ML"
        },
        "devops": {
            "name": "DevOps AI Specialist",
            "endpoint": "/api/ai/devops",
            "description": "IA spécialisée en DevOps et infrastructure"
        },
        "mobile": {
            "name": "Mobile AI Specialist",
            "endpoint": "/api/ai/mobile",
            "description": "IA spécialisée en développement mobile"
        },
        "cybersecurite": {
            "name": "CyberSec AI Specialist",
            "endpoint": "/api/ai/cybersec",
            "description": "IA spécialisée en cybersécurité"
        },
        "gestion_projet": {
            "name": "ProjectMgmt AI Specialist",
            "endpoint": "/api/ai/projectmgmt",
            "description": "IA spécialisée en gestion de projet"
        },
        "general": {
            "name": "General AI Specialist",
            "endpoint": "/api/ai/general",
            "description": "IA généraliste pour tous types de postes"
        }
    }
    
    specialist = ai_specialists.get(job_type, ai_specialists["general"])
    
    logger.info(f"Simulating routing to {specialist['name']} for job type {job_type}.")
    # Ici, on pourrait faire un appel HTTP vers l'IA spécialisée
    
    return {
        "specialist": specialist,
        "status": "routed",
        "message": f"E-mail routé vers {specialist['name']}"
    }

@zapier_bp.route("/zapier/webhook/test", methods=["POST", "GET"])
@cross_origin()
def test_webhook():
    """
    Webhook de test pour vérifier la connectivité avec Zapier
    """
    if request.method == "GET":
        return jsonify({
            "status": "success",
            "message": "Webhook de test opérationnel",
            "method": "GET"
        })
    
    data = request.get_json() or {}
    logger.info(f"Webhook de test reçu: {json.dumps(data)}")
    return jsonify({
        "status": "success",
        "message": "Webhook de test reçu",
        "method": "POST",
        "data_received": data
    })

@zapier_bp.route("/zapier/config", methods=["GET"])
@cross_origin()
def get_zapier_config():
    """
    Retourne la configuration pour l'intégration Zapier
    """
    config = {
        "webhooks": {
            "linkedin_email": "/api/zapier/webhook/linkedin-email",
            "test": "/api/zapier/webhook/test"
        },
        "ai_specialists": [
            "developpement_web",
            "data_science", 
            "devops",
            "mobile",
            "cybersecurite",
            "gestion_projet",
            "general"
        ],
        "supported_methods": ["POST"],
        "content_type": "application/json"
    }
    
    return jsonify(config)


