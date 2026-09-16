# Job Notification System Architecture

## Pipeline

Scheduler -> Source Adapters -> Normalize -> Match -> Deduplicate -> PostgreSQL -> HTML Report -> SMTP -> Notification History

## Source adapters

Adapters implement BaseJobSource. Add integrations only through permitted public APIs, feeds, or public career pages. Platform-specific authentication, rate limits, and terms must be respected.

## Matching

Required skills contribute 60%, preferred skills 20%, and configured location 20%. A banned keyword produces a zero score. The result is deterministic and explainable.

## Persistence

SQLAlchemy models track companies, jobs, pipeline runs, source runs, and notifications. Alembic owns schema migrations.

## Deployment

Docker Compose runs PostgreSQL and the scheduler. The container runs as a non-root user and applies migrations before starting the scheduler.

## CI

GitHub Actions validates pull requests with Ruff, Black, and pytest. Jenkins performs the same quality gates and builds the Docker image on master.
