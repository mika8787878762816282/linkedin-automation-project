
from fpdf import FPDF
import json

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Curriculum Vitae", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, body)
        self.ln(5)

def generate_cv_pdf(profile_info, job_description, output_filename="cv.pdf"):
    """
    Génère un CV personnalisé au format PDF en fonction des informations de profil
    et de la description du poste, avec une rédaction IA pour le résumé et les compétences.
    """
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Informations personnelles
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, profile_info.get("name", "N/A"), 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, f"Email: {profile_info.get("email", "N/A")}", 0, 1, "C")
    pdf.cell(0, 5, f"Téléphone: {profile_info.get("phone", "N/A")}", 0, 1, "C")
    pdf.cell(0, 5, f"LinkedIn: {profile_info.get("linkedin", "N/A")}", 0, 1, "C")
    pdf.ln(10)

    # Résumé (rédaction IA)
    pdf.chapter_title("Résumé Professionnel")
    ai_summary = f"Développeur expérimenté avec une expertise avérée en {", ".join(profile_info.get("skills", []))} et une passion pour l\"innovation. Capable de transformer des exigences complexes en solutions logicielles robustes et évolutives. Fortement motivé par les défis techniques et l\"apprentissage continu, je suis prêt à apporter une contribution significative à des projets ambitieux, notamment dans des environnements dynamiques comme celui décrit pour le poste de {job_description.get("title", "Développeur")}."
    pdf.chapter_body(ai_summary)

    # Compétences (rédaction IA)
    pdf.chapter_title("Compétences Techniques")
    ai_skills_description = f"Maîtrise approfondie des technologies front-end (React, JavaScript, HTML, CSS) et back-end (Python, Flask, Node.js). Expertise en gestion de bases de données (SQL, NoSQL) et déploiement cloud (AWS, Docker). Capacité à s\"adapter rapidement aux nouvelles technologies et à résoudre des problèmes complexes avec créativité et efficacité. Je suis particulièrement intéressé par les aspects de {", ".join(job_description.get("skills", []))} mentionnés dans l\"offre."
    pdf.chapter_body(ai_skills_description)

    # Expérience
    pdf.chapter_title("Expérience Professionnelle")
    pdf.chapter_body(profile_info.get("experience", "N/A"))

    # Éducation
    pdf.chapter_title("Formation")
    pdf.chapter_body(profile_info.get("education", "N/A"))

    pdf.output(output_filename)
    return output_filename

# Exemple d\"utilisation (pour les tests)
if __name__ == \"__main__\":
    sample_profile = {
        \"name\": \"Michaël Sibony\",
        \"email\": \"Michaelsibony0@gmail.com\",
        \"phone\": \"+33 6 12 34 56 78\",
        \"linkedin\": \"https://www.linkedin.com/in/michaelsibony/\",
        \"summary\": \"Développeur Full Stack passionné avec 5 ans d\\\"expérience dans le développement web et mobile, spécialisé en React, Node.js et Python.\",
        \"skills\": [\"React\", \"Node.js\", \"Python\", \"Flask\", \"JavaScript\", \"HTML\", \"CSS\", \"SQL\", \"NoSQL\", \"AWS\", \"Docker\"],
        \"experience\": \"Développeur Senior chez Tech Solutions (2022-Présent) - Développement et maintenance d\\\"applications web complexes. Développeur Junior chez Web Innovations (2020-2022) - Contribution au développement de nouvelles fonctionnalités.\",
        \"education\": \"Master en Informatique, Université de Paris (2019)\"
    }
    sample_job_description = {
        \"title\": \"Développeur Full Stack\",
        \"company\": \"TechCorp\",
        \"skills\": [\"React\", \"Python\", \"Cloud\"],
        \"raw_content\": \"Poste de Développeur Full Stack avec expérience en React et Python. Compétences en Cloud sont un plus.\"
    }
    cv_pdf_file = generate_cv_pdf(sample_profile, sample_job_description, \"cv_test.pdf\")
    print(f\"CV PDF généré: {cv_pdf_file}\")


