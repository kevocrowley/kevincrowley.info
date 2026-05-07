from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    profile = {
        "name": "Kevin Crowley",
        "title": "Platform Engineer | SRE",
        "location": "County Meath, Ireland",
        "company": "Travelport",
        "email": "kevincrowley@gmail.com",
        "linkedin": "https://www.linkedin.com/in/kevincrowleyin/",
        "summary": "Platform Engineer specializing in cloud infrastructure automation using Terraform and Python. Building reliable, scalable systems with a focus on IaC, observability, and site reliability practices.",
    }

    experience = [
        {
            "title": "Platform Engineer",
            "company": "Travelport",
            "period": "Present",
            "description": "Designing and maintaining cloud infrastructure using Terraform. Building automation pipelines and Python tooling for infrastructure management. Implementing observability solutions and reliability engineering practices.",
        }
    ]

    education = [
        {
            "school": "Munster Technological University (formerly CIT)",
            "period": "1998 - 2002",
            "description": "BSc in Information Systems",
        }
    ]

    certifications = [
        {
            "name": "HashiCorp Terraform Associate",
            "issuer": "HashiCorp",
            "year": "2024",
        },
        {
            "name": "AWS Solutions Architect",
            "issuer": "Amazon Web Services",
            "year": "2023",
        },
        {
            "name": "Certified Kubernetes Administrator",
            "issuer": "CNCF",
            "year": "2023",
        },
    ]

    skills = {
        "Infrastructure as Code": ["Terraform", "HCL", "Terragrunt"],
        "Programming": ["Python", "Bash"],
        "Cloud Platforms": ["AWS", "Azure"],
        "Observability": ["Prometheus", "Grafana", "ELK Stack", "Datadog"],
        "CI/CD": ["GitHub Actions", "Jenkins"],
        "Databases": ["PostgreSQL", "Redis", "MongoDB"],
    }

    projects = [
        {
            "title": "MongoDB to MongoDB Atlas Migration",
            "company": "Travelport",
            "period": "2024",
            "description": "Led end-to-end migration of on-premises MongoDB clusters to MongoDB Atlas, implementing SSO integration via SAML, VPC peering for private network access, and full infrastructure automation using Terraform. Achieved zero-downtime migration with automated rollback capabilities.",
            "tech": ["MongoDB Atlas", "Terraform", "SSO/SAML", "VPC Peering"],
        },
        {
            "title": "DNS Infrastructure Migration to AWS Route53",
            "company": "Travelport",
            "period": "2024",
            "description": "Migrated DNS hosting from on-premises BIND servers to AWS Route53 using Terraform. Developed Python script to transform BIND zone files (txt records) into YAML format for Terraform consumption. Successfully migrated thousands of DNS records with validation and automated testing.",
            "tech": ["AWS Route53", "Terraform", "Python", "BIND DNS"],
        },
        {
            "title": "Junior Team Guidance & Mentoring",
            "company": "Travelport",
            "period": "2023 - Present",
            "description": "Provided technical guidance and mentorship to junior team members, conducting regular code reviews, pairing sessions, and technical workshops. Developed onboarding materials and established best practices documentation for infrastructure as code workflows.",
            "tech": ["Mentorship", "Technical Leadership", "Documentation"],
        },
        {
            "title": "AI Tiger Team - Amazon Bedrock Platform",
            "company": "Travelport",
            "period": "2024 - Present",
            "description": "Served as Tech Lead on AI tiger team to drive AI adoption across the organization. Built and maintained Infrastructure as Code for AWS Bedrock integration, providing development teams with ready-to-use agents, agentcore, knowledge bases, identity management, observability, and vector databases (OpenSearch, Pinecone).",
            "tech": [
                "AWS Bedrock",
                "Terraform",
                "AgentCore",
                "Knowledge Bases",
                "Vector Databases",
                "OpenSearch",
            ],
        },
    ]

    return render_template(
        "index.html",
        profile=profile,
        experience=experience,
        education=education,
        certifications=certifications,
        skills=skills,
        projects=projects,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
