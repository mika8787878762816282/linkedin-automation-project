import imaplib
import email
from email.header import decode_header
import logging
import os

"""
LinkedIn Email Monitor Module
=============================

This module provides functionality to monitor LinkedIn-related emails
and extract job offers from them.

Functions:
    - monitor_linkedin_emails: Connects to an IMAP server, searches for LinkedIn job offer emails,
      and extracts relevant information.

Dependencies:
    - imaplib
    - email
    - logging
    - os
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def monitor_linkedin_emails(email_address, app_password):
    """
    Surveille les e-mails LinkedIn et extrait les offres d'emploi.

    Args:
        email_address (str): L'adresse e-mail à surveiller.
        app_password (str): Le mot de passe d'application pour l'authentification IMAP.

    Returns:
        list: Une liste de dictionnaires, chaque dictionnaire représentant une offre d'emploi.
    """
    job_offers = []
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, app_password)
        mail.select("inbox")

        # Rechercher les e-mails de LinkedIn
        search_criteria = 'FROM "linkedin.com" SUBJECT "offre d\\'emploi"'
        _, email_ids = mail.search(None, search_criteria)
        email_ids = email_ids[0].split()

        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Décoder le sujet
                    decoded_header = decode_header(msg["Subject"])[0]
                    subject = decoded_header[0]
                    encoding = decoded_header[1]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    # Extraire le corps de l'e-mail
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            cdisposition = str(part.get("Content-Disposition"))
                            if ctype == "text/plain" and "attachment" not in cdisposition:
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    job_offers.append({
                        "subject": subject,
                        "body": body,
                        "sender": msg["From"]
                    })
        mail.logout()
    except imaplib.IMAP4.error as e:
        logging.error("IMAP error during email monitoring: %s", e)
    except Exception as e:
        logging.error("Unexpected error during email monitoring: %s", e)
    return job_offers

# Exemple d'utilisation (pour les tests)
if __name__ == '__main__':
    # Ces informations sont sensibles et ne devraient pas être codées en dur en production.
    # Elles sont ici à titre d'exemple pour le test.
    EMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
    APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

    if not EMAIL_ADDRESS or not APP_PASSWORD:
        logging.warning("GMAIL_ADDRESS or GMAIL_APP_PASSWORD environment variables not set. Skipping email monitoring test.")
    else:
        logging.info("Surveillance des e-mails LinkedIn...")
        offers = monitor_linkedin_emails(EMAIL_ADDRESS, APP_PASSWORD)
        if offers:
            logging.info("%d offres d'emploi LinkedIn trouvées.", len(offers))
            for i, offer in enumerate(offers):
                logging.info("\n--- Offre %d ---", i+1)
                logging.info("Sujet: %s", offer["subject"])
                logging.info("Expéditeur: %s", offer["sender"])
                logging.info("Extrait du corps: %s...", offer["body"][:200])
        else:
            logging.info("Aucune offre d'emploi LinkedIn trouvée.")

