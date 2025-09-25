import logging
import requests

"""
Zapier Integration Module
=========================

This module provides functionality to send data to Zapier webhooks.

Functions:
    - send_to_zapier: Sends a JSON payload to a configured Zapier webhook.

Dependencies:
    - requests
    - logging
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Configuration des endpoints
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def send_to_zapier(data):
    """
    Envoie des données à un webhook Zapier.
    
    Args:
        data (dict): Les données à envoyer au webhook Zapier.
        
    Returns:
        dict: La réponse JSON de Zapier si la requête est réussie, sinon None.
    """
    try:
        response = requests.post(ZAPIER_WEBHOOK, json=data, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Lève une exception pour les codes d\"état HTTP d\"erreur
        logging.info("Data successfully sent to Zapier. Response: %s", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Zapier integration error: %s", e)
        return None
    except Exception as e: # Catching a more specific exception if possible, or re-raising
        logging.error("An unexpected error occurred while sending data to Zapier: %s", e)
        raise # Re-raising the exception to avoid broad-exception-caught if it's not handled here

# Exemple d\"utilisation (pour les tests)
if __name__ == "__main__":
    sample_data = {
        "event": "new_job_offer",
        "job_title": "Développeur Python",
        "company": "Example Corp",
        "location": "Remote"
    }
    logging.info("Envoi de données d\"exemple à Zapier...")
    try:
        zapier_response = send_to_zapier(sample_data)
        if zapier_response:
            logging.info("Réponse de Zapier reçue.")
        else:
            logging.error("Échec de l\"envoi des données à Zapier.")
    except Exception as e:
        logging.error("Test failed due to an unexpected error: %s", e)

