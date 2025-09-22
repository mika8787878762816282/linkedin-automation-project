
import re
import json

def analyze_job_offer(email_content):
    """
    Analyse le contenu d\'une offre d\'emploi (sujet et corps de l\'e-mail)
    et extrait les informations pertinentes comme le titre du poste, l\'entreprise,
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
    title_match = re.search(r"(poste de|offre d\'emploi|recrute).*?(développeur|ingénieur|data scientist|chef de projet|consultant|architecte|manager|spécialiste|expert).*?(?=\s*chez|à|pour|en|avec|\n|$)", full_text, re.IGNORECASE)
    if title_match:
        job_details["title"] = title_match.group(0).strip()
    else:
        # Fallback: utiliser le sujet si pas de match précis
        job_details["title"] = subject.replace("Nouvelle offre d\'emploi : ", "").strip()

    # Extraction de l\'entreprise
    company_match = re.search(r"chez\s+([A-Z][a-zA-Z0-9\s&.-]+)", full_text, re.IGNORECASE)
    if company_match:
        job_details["company"] = company_match.group(1).strip()
    else:
        company_match_alt = re.search(r"par\s+([A-Z][a-zA-Z0-9\s&.-]+)", full_text, re.IGNORECASE)
        if company_match_alt:
            job_details["company"] = company_match_alt.group(1).strip()

    # Extraction des compétences (liste non exhaustive, à affiner)
    common_skills = [
        "Python", "Java", "JavaScript", "React", "Angular", "Vue.js", "Node.js",
        "Flask", "Django", "Spring Boot", "Docker", "Kubernetes", "AWS", "Azure",
        "GCP", "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Git", "CI/CD",
        "Machine Learning", "Deep Learning", "Data Science", "Big Data", "Spark",
        "Hadoop", "Agile", "Scrum", "DevOps", "Cloud", "API REST", "Microservices"
    ]
    found_skills = [skill for skill in common_skills if re.search(r\'\\b\' + re.escape(skill) + r\'\\b\', full_text, re.IGNORECASE)]
    job_details["skills"] = list(set(found_skills)) # Supprimer les doublons

    # Résumé de la description (premières phrases ou paragraphe)
    description_sentences = re.split(r\'\
(?<=[.!?])\\s+\', body)
    job_details["description_summary"] = " ".join(description_sentences[:3]) if description_sentences else body[:500]

    return job_details

# Exemple d\'utilisation (pour les tests)
if __name__ == \"__main__\":
    sample_email_content = {
        \"subject\": \"Nouvelle offre d\'emploi : Développeur Full Stack chez TechCorp\",
        \"body\": \"Bonjour,\n\nNous recherchons un Développeur Full Stack passionné pour rejoindre notre équipe innovante chez TechCorp. Vous travaillerez sur des projets stimulants utilisant React, Node.js et Python. Une expérience avec Docker et AWS serait un plus. Le poste est basé à Paris. Nous offrons un environnement de travail dynamique et des opportunités de croissance.\n\nCordialement,\nL\'équipe de recrutement de TechCorp.\"
    }
    
    analyzed_job = analyze_job_offer(sample_email_content)
    print(json.dumps(analyzed_job, indent=2))

    sample_email_content_2 = {
        \"subject\": \"Opportunité : Ingénieur Machine Learning chez InnovateLab\",
        \"body\": \"Salut,\n\nInnovateLab est à la recherche d\'un Ingénieur Machine Learning talentueux. Vous aurez l\'occasion de développer des modèles d\'IA de pointe en utilisant Python, TensorFlow et PyTorch. Connaissance de Kubernetes et du déploiement cloud appréciée. Rejoignez-nous à Lyon !\"
    }
    analyzed_job_2 = analyze_job_offer(sample_email_content_2)
    print(json.dumps(analyzed_job_2, indent=2))


