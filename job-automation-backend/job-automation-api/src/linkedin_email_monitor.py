
import imaplib
import email
from email.header import decode_header
import re

def monitor_linkedin_emails(email_address, app_password):
    """
    Surveille les e-mails LinkedIn et extrait les offres d'emploi.
    Cette fonction est principalement destinée à être appelée par Zapier via un webhook,
    mais elle contient la logique d'extraction si nécessaire pour une utilisation directe.
    """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, app_password)
        mail.select("inbox")

        # Rechercher les e-mails de LinkedIn
        status, email_ids = mail.search(None, 
                                        f'FROM "linkedin.com" OR FROM "linkedin.com"',
                                        f'SUBJECT "offre d\'emploi" OR SUBJECT "poste" OR SUBJECT "recrutement"')
        email_ids = email_ids[0].split()

        job_offers = []
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Décoder le sujet
                    subject, encoding = decode_header(msg["Subject"])[0]
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
        return job_offers
    except Exception as e:
        print(f"Erreur lors de la surveillance des e-mails LinkedIn: {e}")
        return []

# Exemple d'utilisation (pour les tests)
if __name__ == '__main__':
    # Ces informations sont sensibles et ne devraient pas être codées en dur en production.
    # Elles sont ici à titre d'exemple pour le test.
    EMAIL_ADDRESS = "Michaelsibony0@gmail.com"
    APP_PASSWORD = "jglx umnj uzgx itld"

    print("Surveillance des e-mails LinkedIn...")
    offers = monitor_linkedin_emails(EMAIL_ADDRESS, APP_PASSWORD)
    if offers:
        print(f"{len(offers)} offres d'emploi LinkedIn trouvées.")
        for i, offer in enumerate(offers):
            print(f"\n--- Offre {i+1} ---")
            print(f"Sujet: {offer['subject']}")
            print(f"Expéditeur: {offer['sender']}")
            print(f"Extrait du corps: {offer['body'][:200]}...")
    else:
        print("Aucune offre d'emploi LinkedIn trouvée.")


