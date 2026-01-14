# Architecture

This project is built around a simple flow:

1. An API request creates a Job record in PostgreSQL.
2. A background task runs in-process (single worker) to fetch Places Text Search results.
3. For each result, Place Details is fetched to normalize fields and optionally store reviews.
4. Records are persisted and can be exported as JSON or CSV.

## Notes

- For production use with multiple workers, replace the in-process task registry with a queue (e.g., Redis + RQ/Celery).
- Use conservative rate limits. Your quota and billing settings should guide the defaults.
