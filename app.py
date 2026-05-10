from flask import Flask, render_template, send_from_directory, abort
import os
import glob
import markdown

BLOG_DIR = os.path.join(os.path.dirname(__file__), "blog")


def get_config():
    return {
        "DEBUG": os.getenv("FLASK_DEBUG", "false").lower() == "true",
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev"),
    }


app = Flask(__name__)
app.config.update(get_config())


def get_blog_posts():
    posts = []
    pattern = os.path.join(BLOG_DIR, "*.md")
    for md_file in sorted(glob.glob(pattern), reverse=True):
        slug = os.path.splitext(os.path.basename(md_file))[0]
        with open(md_file) as f:
            lines = f.readlines()
        title = lines[0].strip("# \n") if lines else slug
        excerpt_lines = [l for l in lines[1:] if l.strip() and not l.startswith("```")]
        excerpt = excerpt_lines[0].strip()[:200] if excerpt_lines else ""
        posts.append({"slug": slug, "title": title, "excerpt": excerpt})
    return posts


def get_blog_post(slug):
    md_path = os.path.join(BLOG_DIR, f"{slug}.md")
    if not os.path.exists(md_path):
        return None
    with open(md_path) as f:
        content = f.read()
    lines = content.split("\n")
    title = lines[0].strip("# \n") if lines else slug
    html = markdown.markdown(content, extensions=["fenced_code"])
    return {"title": title, "html": html}


@app.route("/resume")
def resume():
    path = os.path.join(os.path.dirname(__file__), "kevin_crowley_resume.pdf")
    if not os.path.exists(path):
        abort(404)
    return send_from_directory(
        os.path.dirname(__file__), "kevin_crowley_resume.pdf", as_attachment=True
    )


@app.route("/")
def index():
    profile = {
        "name": "Kevin Crowley",
        "title": "Platform Engineer | SRE",
        "location": "Dublin, Ireland",
        "company": "Travelport",
        "email": "kevincrowley@gmail.com",
        "linkedin": "https://www.linkedin.com/in/kevincrowleyin/",
        "slack": "https://kevincrowleyworkspace.slack.com",
        "photo": "Photo.jpg",
        "summary": "Software development-led platform engineer with 20+ years of experience building infrastructure that makes engineering teams productive and reliable. I take a code-first approach to infrastructure — writing automation, tooling, and platforms so developers can own their services end-to-end without friction. Proven owner of technical projects from greenfield data center builds to large-scale cloud migrations on AWS and Azure, with deep expertise in Terraform, Kubernetes, Python, and CI/CD. Recently tasked with architecting AI infrastructure on AWS Bedrock, building observability with Datadog, defining SLOs, and establishing incident response practices for production systems. Security-conscious, experienced in on-call support, and committed to building platforms that teams trust and enjoy working with.",
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

    skills = [
        "AWS",
        "Azure",
        "Terraform",
        "Terragrunt",
        "Kubernetes",
        "Docker",
        "Ansible",
        "Puppet",
        "Python",
        "Bash",
        "Datadog",
        "Prometheus",
        "Grafana",
        "ELK Stack",
        "GitHub Actions",
        "Jenkins",
        "PostgreSQL",
        "Redis",
        "MongoDB",
        "Kafka",
    ]

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

    posts = get_blog_posts()

    return render_template(
        "index.html",
        profile=profile,
        experience=experience,
        education=education,
        certifications=certifications,
        skills=skills,
        projects=projects,
        posts=posts,
    )


@app.route("/blog/<slug>")
def blog_post(slug):
    post = get_blog_post(slug)
    if post is None:
        abort(404)
    return render_template("blog_post.html", post=post)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("404.html"), 500


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


if __name__ == "__main__":
    app.run(
        debug=app.config["DEBUG"], host="0.0.0.0", port=int(os.getenv("PORT", 5000))
    )
