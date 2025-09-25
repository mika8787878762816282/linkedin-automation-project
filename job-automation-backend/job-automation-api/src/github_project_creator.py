
import requests
import json
import base64

def create_github_project(project_details, github_token):
    """
    Crée un dépôt GitHub et y pousse un fichier README.md.
    """
    repo_name = project_details.get("name", "new-project")
    description = project_details.get("description", "Projet généré automatiquement.")
    homepage = project_details.get("homepage", "")
    private = project_details.get("private", False)

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Créer le dépôt
    create_repo_url = "https://api.github.com/user/repos"
    repo_data = {
        "name": repo_name,
        "description": description,
        "homepage": homepage,
        "private": private,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    
    try:
        response = requests.post(create_repo_url, headers=headers, data=json.dumps(repo_data))
        response.raise_for_status() # Lève une exception pour les codes d'état HTTP d'erreur
        
        repo_info = response.json()
        print(f"Repository \'{repo_name}\' created successfully: {repo_info["html_url"]}")
        
        # 2. Créer un fichier README.md
        readme_content = f"# {repo_name}\n\n{description}\n\nCe projet a été généré automatiquement pour démontrer des compétences.\n"
        create_file_url = f"https://api.github.com/repos/{repo_info["owner"]["login"]}/{repo_name}/contents/README.md"
        file_data = {
            "message": "Initial commit: Add README.md",
            "content": base64.b64encode(readme_content.encode()).decode()
        }
        file_response = requests.put(create_file_url, headers=headers, data=json.dumps(file_data))
        file_response.raise_for_status()
        
        print("README.md created successfully.")
        return repo_info["html_url"]
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to create GitHub project: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        return None

# Exemple d'utilisation (pour les tests)
if __name__ == "__main__":
    sample_project_details = {
        "name": "MonSuperProjetPython",
        "description": "Un projet Python pour démontrer mes compétences en développement web.",
        "homepage": "https://monsuperprojet.com",
        "private": False
    }
    github_token = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN_HERE") # Utiliser une variable d'environnement ou un placeholder
    project_url = create_github_project(sample_project_details, github_token)
    if project_url:
        print(f"Projet GitHub créé avec succès: {project_url}")
    else:
        print("Échec de la création du projet GitHub.")


