"""Create initial production schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("companies", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(), nullable=False, unique=True))
    op.create_table("jobs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("source", sa.String(), nullable=False), sa.Column("source_job_id", sa.String(), nullable=False), sa.Column("title", sa.String(), nullable=False), sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False), sa.Column("location", sa.String()), sa.Column("description", sa.Text()), sa.Column("url", sa.String()), sa.Column("salary_min", sa.Float()), sa.Column("salary_max", sa.Float()), sa.Column("salary_currency", sa.String()), sa.Column("experience_min", sa.Float()), sa.Column("experience_max", sa.Float()), sa.Column("work_type", sa.String()), sa.Column("employment_type", sa.String()), sa.Column("match_score", sa.Float()), sa.Column("matching_skills", sa.Text()), sa.Column("missing_skills", sa.Text()), sa.Column("is_emailed", sa.Boolean(), nullable=False), sa.Column("discovered_at", sa.DateTime(timezone=True), nullable=False), sa.Column("posted_at", sa.DateTime(timezone=True)), sa.Column("job_hash", sa.String(), nullable=False, unique=True), sa.Column("content_hash", sa.String()))
    op.create_index("ix_jobs_source_source_job_id", "jobs", ["source", "source_job_id"], unique=True)
    op.create_table("job_runs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("started_at", sa.DateTime(timezone=True), nullable=False), sa.Column("completed_at", sa.DateTime(timezone=True)), sa.Column("status", sa.String(), nullable=False), sa.Column("sources_attempted", sa.Integer()), sa.Column("sources_succeeded", sa.Integer()), sa.Column("sources_failed", sa.Integer()), sa.Column("jobs_fetched", sa.Integer()), sa.Column("jobs_unique", sa.Integer()), sa.Column("jobs_matched", sa.Integer()), sa.Column("jobs_notified", sa.Integer()), sa.Column("error_message", sa.Text()))
    op.create_table("source_runs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("job_run_id", sa.Integer(), sa.ForeignKey("job_runs.id"), nullable=False), sa.Column("source", sa.String(), nullable=False), sa.Column("status", sa.String(), nullable=False), sa.Column("jobs_found", sa.Integer()), sa.Column("duration_ms", sa.Integer()), sa.Column("error_message", sa.Text()))
    op.create_table("notifications", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("job_id", sa.Integer(), sa.ForeignKey("jobs.id"), nullable=False), sa.Column("recipient", sa.String(), nullable=False), sa.Column("status", sa.String(), nullable=False), sa.Column("sent_at", sa.DateTime(timezone=True)), sa.Column("error_message", sa.Text()))

def downgrade():
    op.drop_table("notifications")
    op.drop_table("source_runs")
    op.drop_table("job_runs")
    op.drop_table("jobs")
    op.drop_table("companies")
