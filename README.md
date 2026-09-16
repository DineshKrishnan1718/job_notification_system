# 🚀 Automated Job Notification Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)
![Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins-red.svg)
![PyTest](https://img.shields.io/badge/Testing-PyTest-yellow.svg)

An enterprise-grade Python automation system designed to scrape, score, deduplicate, and email highly relevant job postings every day. 

Built as a portfolio project to demonstrate **Backend Development, System Design, Automated Testing (SDET), and CI/CD pipelines.**

## 🌟 Key Features
* **Pluggable Source Adapters:** Designed using the Strategy pattern. Easily add APIs, RSS feeds, or Playwright DOM scrapers without modifying core logic.
* **Intelligent Match Engine:** Parses job descriptions against user-defined mandatory/optional skills using Regex word boundaries to calculate a mathematical match score (0-100%).
* **Cryptographic Deduplication:** Generates a SHA-256 hash of `Title+Company+Location` to ensure jobs found across multiple platforms are merged and never emailed twice.
* **Automated Daily Reports:** Uses Jinja2 to generate color-coded HTML email summaries delivered via SMTP.
* **Fully Containerized:** Runs seamlessly in a Docker network with a persistent PostgreSQL database.
* **CI/CD Ready:** Includes a `Jenkinsfile` for automated PyTest validation and Docker deployments.

## 🏗️ System Architecture

```text
                  ┌───────────────────┐
                  │ User Configuration│ (.env)
                  └─────────┬─────────┘
                            ↓
                     ┌──────────────┐
                     │   Scheduler  │ (Python schedule / Docker)
                     └──────┬───────┘
                            ↓
                  ┌───────────────────┐
                  │ Job Source Manager│ (Adapter Pattern)
                  └─────────┬─────────┘
                            ↓
       ┌────────────┬───────┼────────┬─────────────┐
  LinkedIn API  Naukri HTML  Indeed API     Company Page 
       └────────────┴───────┼────────┴─────────────┘
                            ↓
                    Normalize & Deduplicate
                            ↓
                      Match Engine (Score > 70%)
                            ↓
                    PostgreSQL Database
                            ↓
               Jinja2 HTML Report Generator
                            ↓
                    Email Notification
```

## 📁 Project Structure

```text
├── app/                        # Application Source Code
│   ├── adapters/               # API / Web Scraper integrations
│   ├── config/                 # Pydantic environment configurations
│   ├── core/                   # Match Engine & Deduplication algorithms
│   ├── database/               # SQLAlchemy models and CRUD
│   ├── notifications/          # Jinja2 templating and SMTP sender
│   └── scheduler/              # Daily cron loop
├── deploy/                     # Infrastructure as Code
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── Jenkinsfile
├── templates/email/            # HTML Email templates
├── tests/                      # PyTest suite (Unit & Integration)
├── .env.example                # Template for environment variables
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start (Docker)

1. Clone the repository and configure your environment:

```bash
git clone [https://github.com/yourusername/job-notification-pipeline.git](https://github.com/yourusername/job-notification-pipeline.git)
cd job-notification-pipeline
cp .env.example .env
```

2. Update the .env file:

   - Add your target JOB_ROLES and LOCATIONS.
   - Generate an App Password if using Gmail for EMAIL_PASSWORD.

3. Launch the infrastructure:

```bash
docker-compose -f deploy/docker-compose.yml up --build -d
```

4. View the live logs:
```bash
docker-compose logs -f app
```

## 🧪 Running Tests

The project features a comprehensive PyTest suite covering API parsing (via mocking), algorithm validation, and database duplicate protection using in-memory SQLite.

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the test suite
pytest
```

## 🛠️ Tech Stack
- Language: Python 3.11

- Database: PostgreSQL / SQLite

- Libraries: SQLAlchemy (ORM), Pydantic (Data validation), Requests, Jinja2, Schedule

- Testing: PyTest, unittest.mock

- DevOps: Docker, Docker Compose, Jenkins










