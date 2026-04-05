from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    profile = {
        'name': 'Kevin Crowley',
        'title': 'Platform Engineer | SRE',
        'location': 'County Meath, Ireland',
        'company': 'Travelport',
        'email': 'kevincrowley@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/kevincrowleyin/',
        'summary': 'Platform Engineer specializing in cloud infrastructure automation using Terraform and Python. Building reliable, scalable systems with a focus on IaC, observability, and site reliability practices.',
    }
    
    experience = [
        {
            'title': 'Platform Engineer',
            'company': 'Travelport',
            'period': 'Present',
            'description': 'Designing and maintaining cloud infrastructure using Terraform. Building automation pipelines and Python tooling for infrastructure management. Implementing observability solutions and reliability engineering practices.'
        }
    ]
    
    education = [
        {
            'school': 'Munster Technological University (formerly CIT)',
            'period': '1998 - 2002',
            'description': 'BSc in Information Systems'
        }
    ]
    
    certifications = [
        {'name': 'HashiCorp Terraform Associate', 'issuer': 'HashiCorp', 'year': '2024'},
        {'name': 'AWS Solutions Architect', 'issuer': 'Amazon Web Services', 'year': '2023'},
        {'name': 'Certified Kubernetes Administrator', 'issuer': 'CNCF', 'year': '2023'},
    ]
    
    skills = {
        'Infrastructure as Code': ['Terraform', 'HCL', 'Terragrunt'],
        'Programming': ['Python', 'Bash'],
        'Cloud Platforms': ['AWS', 'Azure'],
        'Containers': ['Docker', 'Kubernetes'],
        'Observability': ['Prometheus', 'Grafana', 'ELK Stack'],
        'CI/CD': ['GitHub Actions', 'GitLab CI', 'Jenkins'],
        'Databases': ['PostgreSQL', 'Redis', 'MongoDB'],
    }
    
    projects = [
        {
            'title': 'Multi-Cloud Infrastructure Automation',
            'description': 'Built Terraform modules for reusable, production-ready infrastructure patterns across AWS and Azure environments.',
            'tech': ['Terraform', 'Python', 'AWS', 'Azure']
        },
        {
            'title': 'Infrastructure Testing Framework',
            'description': 'Developed Python-based testing framework for Terraform configurations using pytest and checkov.',
            'tech': ['Python', 'Terraform', 'Pytest']
        },
        {
            'title': 'GitOps Deployment Pipeline',
            'description': 'Implemented automated infrastructure deployments using GitHub Actions and Terraform Cloud.',
            'tech': ['Terraform Cloud', 'GitHub Actions', 'Kubernetes']
        },
        {
            'title': 'Monitoring & Alerting Dashboard',
            'description': 'Created Grafana dashboards and Prometheus alerting rules for infrastructure health monitoring.',
            'tech': ['Prometheus', 'Grafana', 'Python']
        }
    ]
    
    return render_template('index.html', 
                         profile=profile, 
                         experience=experience,
                         education=education,
                         certifications=certifications,
                         skills=skills,
                         projects=projects)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
