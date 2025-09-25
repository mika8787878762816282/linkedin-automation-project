import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import logging

"""
Email Automation Module
=======================

This module provides functionality for sending automated emails.

Functions:
    - send_automated_email: Sends an automated email with specified recipient, subject, and body.

Dependencies:
    - smtplib
    - email
    - logging
    - os
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Templates d\"email standardisés
EMAIL_TEMPLATE = """
Bonjour {recipient_name},

{message_body}

Cordialement,
{sender_name}
"""

def send_automated_email(recipient, subject, body, sender_email, app_password, attachments=None):
    """
    Envoie un e-mail automatisé avec les paramètres spécifiés.

    Args:
        recipient (str): L\"adresse e-mail du destinataire.
        subject (str): Le sujet de l\"e-mail.
        body (str): Le corps de l\"e-mail.
        sender_email (str): L\"adresse e-mail de l\"expéditeur.
        app_password (str): Le mot de passe d\"application pour l\"authentification SMTP.
        attachments (list, optional): Une liste de chemins de fichiers à joindre. Par défaut à None.

    Raises:
        ValueError: Si des paramètres d\"e-mail requis sont manquants.
        Exception: Si l\"envoi de l\"e-mail échoue.
    """
    if not all([recipient, subject, body, sender_email, app_password]):
        raise ValueError("Missing required email parameters: recipient, subject, body, "
                         "sender_email, app_password")
    
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as attachment_file:
                    part = MIMEApplication(attachment_file.read(),
                                           Name=os.path.basename(file_path))
                part["Content-Disposition"] = f"attachment; filename=\"{os.path.basename(file_path)}\""
                msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        logging.info("E-mail envoyé avec succès à %s", recipient)
    except smtplib.SMTPAuthenticationError as e:
        logging.error("SMTP authentication failed: %s", e)
        raise
    except smtplib.SMTPServerDisconnected as e:
        logging.error("SMTP server disconnected unexpectedly: %s", e)
        raise
    except Exception as e:
        logging.error("Email sending failed: %s", e)
        raise

# Exemple d\"utilisation (pour les tests)
if __name__ == "__main__":
    SENDER_EMAIL_TEST = os.environ.get("GMAIL_ADDRESS")
    APP_PASSWORD_TEST = os.environ.get("GMAIL_APP_PASSWORD")
    RECIPIENT_EMAIL_TEST = "test@example.com"
    EMAIL_SUBJECT_TEST = "Candidature automatisée - [Votre Nom]"
    EMAIL_BODY_CONTENT_TEST = ("Votre offre d\"emploi a retenu toute mon attention. "
                               "Veuillez trouver ci-joint mon CV et un lien vers un "
                               "projet GitHub pertinent.")
    SENDER_NAME_TEST = "Votre Nom"

    if not SENDER_EMAIL_TEST or not APP_PASSWORD_TEST:
        logging.warning("GMAIL_ADDRESS or GMAIL_APP_PASSWORD environment variables not set. "
                        "Skipping email automation test.")
    else:
        test_attachment_path_var = "test_attachment.txt"
        with open(test_attachment_path_var, "w", encoding="utf-8") as f_test:
            f_test.write("Ceci est un fichier de test pour l\"attachement.")

        logging.info("\n--- Test d\"envoi sans attachement ---")
        try:
            formatted_body_test_var = EMAIL_TEMPLATE.format(recipient_name="Cher Recruteur",
                                                        message_body=EMAIL_BODY_CONTENT_TEST,
                                                        sender_name=SENDER_NAME_TEST)
            send_automated_email(RECIPIENT_EMAIL_TEST, EMAIL_SUBJECT_TEST, formatted_body_test_var,
                                 SENDER_EMAIL_TEST, APP_PASSWORD_TEST)
        except ValueError as e:
            logging.error("Erreur de validation: %s", e)
        except Exception as e:
            logging.error("Erreur lors de l\"envoi de l\"e-mail: %s", e)

        logging.info("\n--- Test d\"envoi avec attachement ---")
        try:
            formatted_body_test_var = EMAIL_TEMPLATE.format(recipient_name="Cher Recruteur",
                                                        message_body=EMAIL_BODY_CONTENT_TEST,
                                                        sender_name=SENDER_NAME_TEST)
            send_automated_email(RECIPIENT_EMAIL_TEST, EMAIL_SUBJECT_TEST, formatted_body_test_var,
                                 SENDER_EMAIL_TEST, APP_PASSWORD_TEST, attachments=[test_attachment_path_var])
        except ValueError as e:
            logging.error("Erreur de validation: %s", e)
        except Exception as e:
            logging.error("Erreur lors de l\"envoi de l\"e-mail: %s", e)

        os.remove(test_attachment_path_var)

