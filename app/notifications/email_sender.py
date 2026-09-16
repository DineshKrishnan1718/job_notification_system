import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from typing import List

from app.config.settings import settings
from app.config.logging_config import logger
from app.models.db_models import Job

class EmailService:
    def __init__(self):
        self.logger = logger.getChild("EmailService")
        # Load the directory where our HTML templates live
        self.env = Environment(loader=FileSystemLoader('templates/email'))

    def _categorize_job(self, score: float) -> tuple:
        """Returns the Category Name and Icon based on the match score."""
        if score >= 90:
            return "Excellent", "🔥"
        elif score >= 75:
            return "Strong", "⭐"
        elif score >= 60:
            return "Relevant", "👍"
        else:
            return "Low", "❌"

    def send_daily_report(self, jobs: List[Job]):
        if not jobs:
            self.logger.info("No new jobs to report today. Skipping email.")
            return

        date_str = datetime.now().strftime("%d %B %Y")
        
        # 1. Prepare data for the template
        formatted_jobs = []
        excellent_count = 0
        strong_count = 0

        for job in jobs:
            category, icon = self._categorize_job(job.match_score)
            
            if category == "Excellent": excellent_count += 1
            if category == "Strong": strong_count += 1

            formatted_jobs.append({
                "match_score": job.match_score,
                "category": category,
                "icon": icon,
                "title": job.title,
                "company_name": job.company.name, # Accessing relation
                "location": job.location,
                "source": job.source,
                "url": job.url,
                "matching_skills": job.matching_skills
            })

        # Sort jobs so 🔥 Excellent matches are at the top of the email
        formatted_jobs.sort(key=lambda x: x["match_score"], reverse=True)

        # 2. Render the HTML
        template = self.env.get_template('daily_report.html')
        html_content = template.render(
            date_str=date_str,
            total_jobs=len(jobs),
            excellent_count=excellent_count,
            strong_count=strong_count,
            jobs=formatted_jobs
        )

        # 3. Construct the Email structure
        subject = f"Daily Job Notification – {date_str} – {len(jobs)} Matching Jobs"
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_USERNAME
        msg["To"] = settings.EMAIL_TO
        
        msg.attach(MIMEText(html_content, "html"))

        # 4. Send the Email via SMTP
        try:
            self.logger.info(f"Connecting to SMTP server {settings.EMAIL_HOST}...")
            # We use SMTP (port 587) with TLS encryption
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls() 
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            
            server.sendmail(settings.EMAIL_USERNAME, settings.EMAIL_TO, msg.as_string())
            server.quit()
            
            self.logger.info("Successfully sent the daily job report email!")
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            raise e # Reraise to handle in the main workflow