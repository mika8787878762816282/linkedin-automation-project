
import json
import os
from datetime import datetime

APPLICATION_FILE = "applications.json"

def _load_applications():
    if os.path.exists(APPLICATION_FILE):
        with open(APPLICATION_FILE, "r") as f:
            return json.load(f)
    return []

def _save_applications(applications):
    with open(APPLICATION_FILE, "w") as f:
        json.dump(applications, f, indent=4)

def track_application(job_id, company, position, status, details=None):
    """
    Suit l\"état des candidatures.
    Ajoute une nouvelle candidature ou met à jour une candidature existante.
    """
    applications = _load_applications()
    
    # Vérifier si la candidature existe déjà pour ce job_id
    for app in applications:
        if app["job_id"] == job_id:
            app["status"] = status
            app["last_updated"] = datetime.now().isoformat()
            if details:
                app["details"].update(details)
            _save_applications(applications)
            print(f"Candidature {job_id} mise à jour au statut: {status}")
            return app

    # Nouvelle candidature
    new_app = {
        "job_id": job_id,
        "company": company,
        "position": position,
        "status": status,
        "date_applied": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "details": details if details else {}
    }
    applications.append(new_app)
    _save_applications(applications)
    print(f"Nouvelle candidature enregistrée pour {position} chez {company} avec le statut: {status}")
    return new_app

def get_all_applications():
    """
    Retourne toutes les candidatures suivies.
    """
    return _load_applications()

# Exemple d\"utilisation (pour les tests)
if __name__ == "__main__":
    # Nettoyer le fichier pour un test propre
    if os.path.exists(APPLICATION_FILE):
        os.remove(APPLICATION_FILE)

    print(\"--- Test de suivi de candidature ---\")
    app1 = track_application(\"job_123\", \"TechCorp\", \"Développeur Full Stack\", \"Envoyée\", {\"cv_url\": \"http://cv.com/123\"})
    app2 = track_application(\"job_456\", \"InnovateLab\", \"Ingénieur IA\", \"En cours\")
    app3 = track_application(\"job_789\", \"StartupX\", \"Chef de Projet\", \"Brouillon\")

    print(\"\n--- Toutes les candidatures ---\")
    all_apps = get_all_applications()
    print(json.dumps(all_apps, indent=4))

    print(\"\n--- Mise à jour d\"une candidature ---\")
    updated_app1 = track_application(\"job_123\", \"TechCorp\", \"Développeur Full Stack\", \"Entretien programmé\", {\"interview_date\": \"2025-02-01\"})
    print(json.dumps(updated_app1, indent=4))

    print(\"\n--- Toutes les candidatures après mise à jour ---\")
    all_apps_after_update = get_all_applications()
    print(json.dumps(all_apps_after_update, indent=4))


