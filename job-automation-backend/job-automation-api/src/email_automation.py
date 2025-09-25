
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

def send_automated_response(sender_email, app_password, recipient_email, subject, body, attachments=None):
    """
    Envoie une réponse automatique par e-mail.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                part["Content-Disposition"] = f"attachment; filename=\"{os.path.basename(file_path)}\""
                msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print(f"E-mail envoyé avec succès à {recipient_email}")
        return True
    except Exception as e:
        print(f"Erreur lors de l\"envoi de l\"e-mail: {e}")
        return False

# Exemple d\"utilisation (pour les tests)
if __name__ == \"__main__\":
       SENDER_EMAIL = os.environ.get("GMAIL_ADDRESS")
    APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") # Utiliser le mot de passe d\"application
    RECIPIENT_EMAIL = \"test@example.com\" # Remplacez par une adresse e-mail valide pour les tests
    EMAIL_SUBJECT = \"Candidature automatisée - [Votre Nom]\"
    EMAIL_BODY = \"Bonjour,\n\nVotre offre d\"emploi a retenu toute mon attention. Veuillez trouver ci-joint mon CV et un lien vers un projet GitHub pertinent.\n\nCordialement,\n[Votre Nom]\"
    
    # Créer un fichier de test pour l\"attachement
    with open(\"test_attachment.txt\", \"w\") as f:
        f.write(\"Ceci est un fichier de test pour l\"attachement.\")

    # Test d\"envoi sans attachement
    print(\"\n--- Test d\"envoi sans attachement ---\")
    send_automated_response(SENDER_EMAIL, APP_PASSWORD, RECIPIENT_EMAIL, EMAIL_SUBJECT, EMAIL_BODY)

    # Test d\"envoi avec attachement
    print(\"\n--- Test d\"envoi avec attachement ---\")
    send_automated_response(SENDER_EMAIL, APP_PASSWORD, RECIPIENT_EMAIL, EMAIL_SUBJECT, EMAIL_BODY, attachments=[\"test_attachment.txt\"])

    os.remove(\"test_attachment.txt\")


