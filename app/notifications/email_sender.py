import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.config.settings import settings
from app.config.logging_config import logger


class EmailService:
    def __init__(self):
        self.logger = logger.getChild("EmailService")
        template_dir = Path(__file__).resolve().parents[2] / "templates" / "email"
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html", "xml"]))

    def send_daily_report(self, jobs):
        if not jobs:
            return
        if not all([settings.email_host, settings.email_username, settings.email_password, settings.email_to]):
            raise RuntimeError("Email configuration is incomplete")

        date_str = datetime.now().strftime("%d %B %Y")
        formatted_jobs = [{
            "match_score": job.match_score,
            "title": job.title,
            "company_name": job.company.name,
            "location": job.location,
            "source": job.source,
            "url": job.url,
            "matching_skills": job.matching_skills,
        } for job in sorted(jobs, key=lambda x: x.match_score, reverse=True)]

        template = self.env.get_template("daily_report.html")
        html_content = template.render(date_str=date_str, total_jobs=len(jobs), jobs=formatted_jobs)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Daily Job Notification - {date_str} - {len(jobs)} Matching Jobs"
        msg["From"] = settings.email_username
        msg["To"] = settings.email_to
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        with smtplib.SMTP(settings.email_host, settings.email_port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.email_username, settings.email_password)
            server.sendmail(settings.email_username, [settings.email_to], msg.as_string())
        self.logger.info("Daily job report sent successfully")
