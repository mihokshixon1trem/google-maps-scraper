# API Reference

All endpoints require `X-API-Key` matching `API_KEY` in your `.env`.

## Create a job

POST /jobs

Body:
- query (string)
- location (optional string)
- max_results (optional int)
- max_pages (optional int)
- include_reviews (bool)
- language (optional string)

## Get job status

GET /jobs/{job_id}

## List businesses

GET /businesses?job_id={job_id}

## List reviews

GET /reviews?job_id={job_id}&place_id={place_id}

## Export JSON

GET /exports/json?job_id={job_id}

## Export CSV

GET /exports/csv?job_id={job_id}
