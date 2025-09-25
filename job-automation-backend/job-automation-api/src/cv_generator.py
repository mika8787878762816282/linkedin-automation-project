import logging
from fpdf import FPDF

"""
CV Generator Module
===================

This module provides functions to generate personalized CVs in PDF format.

Functions:
    - generate_cv_pdf: Generates a PDF CV based on profile information and job description.

Dependencies:
    - fpdf
    - logging
"""

class PDF(FPDF):
    """Custom PDF class for CV generation."""
    def header(self):
        """Adds a header to each page of the PDF."""
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Curriculum Vitae", 0, 1, "C")
        self.ln(10)

    def footer(self):
        """Adds a footer with page numbers to each page of the PDF."""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")

    def chapter_title(self, title):
        """Adds a chapter title to the PDF."""
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)

    def chapter_body(self, body):
        """Adds body text to the PDF."""
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, body)
        self.ln(5)

TEMPLATE = """
Nom: {name}
Email: {email}
Téléphone: {phone}
LinkedIn: {linkedin}

Résumé Professionnel:
{summary}

Compétences Techniques:
{skills_description}

Expérience Professionnelle:
{experience}

Formation:
{education}
"""

def generate_cv_pdf(profile_info, job_description, output_filename="cv.pdf"):
    """
    Génère un CV personnalisé au format PDF en fonction des informations de profil
    et de la description du poste, avec une rédaction IA pour le résumé et les compétences.
    """
    try:
        # Ensure all required profile_info keys are present
        required_profile_keys = ["name", "email", "phone", "linkedin", "skills",
                                 "experience", "education"]
        for key in required_profile_keys:
            if key not in profile_info:
                raise KeyError(f"Missing required profile information: {key}")

        # Ensure all required job_description keys are present
        required_job_keys = ["title", "skills"]
        for key in required_job_keys:
            if key not in job_description:
                raise KeyError(f"Missing required job description information: {key}")

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()

        # AI-generated summary and skills description
        ai_summary = (
            f"Développeur expérimenté avec une expertise avérée en "
            f"{', '.join(profile_info['skills'])} et une passion pour l'innovation. "
            f"Capable de transformer des exigences complexes en solutions logicielles "
            f"robustes et évolutives. Fortement motivé par les défis techniques et "
            f"l'apprentissage continu, je suis prêt à apporter une contribution "
            f"significative à des projets ambitieux, notamment dans des environnements "
            f"dynamiques comme celui décrit pour le poste de {job_description['title']}."
        )
        ai_skills_description = (
            f"Maîtrise approfondie des technologies front-end (React, JavaScript, HTML, "
            f"CSS) et back-end (Python, Flask, Node.js). Expertise en gestion de bases "
            f"de données (SQL, NoSQL) et déploiement cloud (AWS, Docker). Capacité à "
            f"s'adapter rapidement aux nouvelles technologies et à résoudre des problèmes "
            f"complexes avec créativité et efficacité. Je suis particulièrement intéressé "
            f"par les aspects de {', '.join(job_description['skills'])} mentionnés dans "
            f"l'offre."
        )

        # Populate template data
        template_data = {
            "name": profile_info["name"],
            "email": profile_info["email"],
            "phone": profile_info["phone"],
            "linkedin": profile_info["linkedin"],
            "summary": ai_summary,
            "skills_description": ai_skills_description,
            "experience": profile_info["experience"],
            "education": profile_info["education"]
        }

        # Use the template for the main content structure
        formatted_cv_content = TEMPLATE.format(**template_data)

        # Add content to PDF (simplified for template integration)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, formatted_cv_content)

        pdf.output(output_filename)
        return output_filename
    except KeyError as e:
        logging.error("Missing required field in profile data or job description: %s", e)
        raise ValueError(f"Profile data or job description incomplete: {e}") from e
    except Exception as e:
        logging.error("An unexpected error occurred during CV generation: %s", e)
        raise

# Exemple d'utilisation (pour les tests)
if __name__ == "__main__":
    sample_profile = {
        "name": "Michaël Sibony",
        "email": "Michaelsibony0@gmail.com",
        "phone": "+33 6 12 34 56 78",
        "linkedin": "https://www.linkedin.com/in/michaelsibony/",
        "skills": ["React", "Node.js", "Python", "Flask", "JavaScript", "HTML", "CSS",
                   "SQL", "NoSQL", "AWS", "Docker"],
        "experience": ("Développeur Senior chez Tech Solutions (2022-Présent) - "
                       "Développement et maintenance d'applications web complexes. "
                       "Développeur Junior chez Web Innovations (2020-2022) - "
                       "Contribution au développement de nouvelles fonctionnalités."),
        "education": "Master en Informatique, Université de Paris (2019)"
    }
    sample_job_description = {
        "title": "Développeur Full Stack",
        "company": "TechCorp",
        "skills": ["React", "Python", "Cloud"],
        "raw_content": ("Poste de Développeur Full Stack avec expérience en React et Python. "
                        "Compétences en Cloud sont un plus.")
    }
    try:
        CV_PDF_FILE = generate_cv_pdf(sample_profile, sample_job_description, "cv_test.pdf")
        logging.info("CV PDF généré: %s", CV_PDF_FILE)
    except ValueError as e:
        logging.error("Erreur lors de la génération du CV: %s", e)


