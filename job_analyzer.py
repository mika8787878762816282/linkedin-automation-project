import re
import json

def analyze_job_offer(email_content):
    """
    Analyse le contenu d'une offre d'emploi (sujet et corps de l'e-mail)
    et extrait les informations pertinentes comme le titre du poste, l'entreprise,
    les compétences requises, et une description sommaire.
    """
    subject = email_content.get("subject", "")
    body = email_content.get("body", "")
    full_text = subject + "\n" + body

    job_details = {
        "title": "",
        "company": "",
        "location": "",
        "skills": [],
        "description_summary": "",
        "raw_content": full_text
    }

    # Extraction du titre du poste (heuristique simple)
    title_match = re.search(r"(poste de|offre d'emploi|recrute).*?(développeur|ingénieur|data scientist|chef de projet|consultant|architecte|manager|spécialiste|expert).*?(?=\s*chez|à|pour|en|avec|\n|$)", full_text, re.IGNORECASE)
    if title_match:
        job_details["title"] = title_match.group(0).strip()
    else:
        # Fallback: utiliser le sujet si pas de match précis
        job_details["title"] = subject.replace("Nouvelle offre d'emploi : ", "").strip()