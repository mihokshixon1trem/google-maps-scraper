# Google Maps Scraper

>Google Maps Scraper is a production-ready data extraction service that collects business listings and review metadata from Google Maps search results using Google’s official Places APIs. It helps teams replace repetitive copy/paste work with a structured pipeline for exporting consistent records (names, categories, locations, ratings, and reviews where available).

If you’re searching for a google map scraper tool or a google maps data scraper you can run reliably, this project focuses on compliance, stability, and repeatable exports rather than brittle HTML parsing.

<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/Z786ZA/Footer-test/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/Bitbash333" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>   <p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Google Maps Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>

## Introduction

A lot of people try to scrape google maps because they need a clean dataset: local businesses, categories, review signals, and basic contact details for internal ops. The problem is that “scrape data from google maps” workflows often become fragile fast—UI changes, captchas, inconsistent fields, and unpredictable run failures.

This repository provides a safer approach to scrape google maps data by using supported endpoints (Places API) and a rate-limited job runner. For anyone asking “how to scrape data from google maps,” the short answer here is: don’t automate the UI—use the API to extract the same intent-focused dataset with better reliability and fewer breakages.

### Where this helps in practice

- Standardizes exports from Google Maps search results into a consistent schema
- Improves scale and repeatability with paging, retries, and checkpoints
- Enables controlled collection of reviews and ratings for analysis and QA
- Reduces operational churn caused by UI changes and scraping instability

## Core Features

| Feature | Description |
|---|---|
| Query-to-Results Pipeline | Converts a location + keyword query into structured records, similar to what users expect when they scrape google maps search results, but using official API pagination. |
| Business Profile Extraction | Collects business name, place_id, categories, address, coordinates, phone (when available), and website fields into a normalized dataset. |
| Review Metadata Capture | Supports a google maps reviews scraper style workflow by fetching review summaries and available review details via API fields and endpoints. |
| Dedupe & Enrichment | Deduplicates by place_id and can enrich existing rows with missing fields across reruns without duplicating entries. |
| Rate Limiting & Backoff | Implements pacing, exponential backoff, and retry caps to protect API stability and reduce job failure cascades. |
| Exporter (CSV/JSON) | Generates portable exports for downstream workflows; ideal for teams looking for a google maps easy scrape experience in a controlled pipeline. |
| Service Interface | Exposes a google maps scraper api with clear endpoints for starting jobs, polling status, and retrieving exports. |

## How It Works

| Step | Trigger / Input | Core Automation Logic | Output / Action | Safety Controls |
|---|---|---|---|---|
| 1 | Search job request | Validates query (keyword, region, limits) and initializes a job | Job created with id | Input validation, max page caps |
| 2 | Places search loop | Calls Places search endpoints with pagination tokens | Candidate place_ids | Rate limiting, retry caps, backoff |
| 3 | Details fetch | Fetches business details per place_id and normalizes fields | Business records | Concurrency limits, circuit breaker |
| 4 | Reviews fetch (optional) | Collects available review metadata/details | Review dataset linked to place_id | Throttling, partial-failure tolerance |
| 5 | Persist & export | Writes to PostgreSQL and generates CSV/JSON exports | Export artifacts | Checkpointing, idempotent writes |

## Tech Stack

- FastAPI (REST service and job control)
- PostgreSQL (storage for jobs, businesses, and review metadata)
- Docker (repeatable local/self-hosted deployment)

## Directory Structure Tree

    google-maps-business-data-extractor-api/
        README.md
        LICENSE
        docker-compose.yml
        .env.example
        app/
            main.py
            api/
                routes/
                    health.py
                    jobs.py
                    businesses.py
                    reviews.py
                    exports.py
                deps.py
            core/
                config.py
                logging.py
                rate_limit.py
                security.py
            db/
                session.py
                migrations/
                    versions/
                        0001_init_tables.py
            models/
                job.py
                business.py
                review.py
            services/
                places_client.py
                job_service.py
                business_service.py
                review_service.py
                export_service.py
            utils/
                validation.py
                pagination.py
        tests/
            test_jobs.py
            test_businesses.py
            test_exports.py
            test_rate_limit.py
        docs/
            api_reference.md
            architecture.md

## Sample JSON Output

Below is an example response showing what a single exported business record can look like after running a search job (including optional review metadata).

    {
        "job": {
            "id": "job_01J9Q2X8F2J9Z7K0A1B2C3D4E5",
            "query": "coffee shops in Manhattan",
            "status": "completed",
            "created_at": "2026-01-14T10:22:11Z",
            "completed_at": "2026-01-14T10:24:48Z",
            "results_count": 25
        },
        "business": {
            "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
            "name": "Brew & Bean Coffee",
            "primary_category": "coffee_shop",
            "categories": ["coffee_shop", "cafe", "bakery"],
            "rating": 4.3,
            "reviews_count": 187,
            "address": {
                "formatted": "123 Broadway, New York, NY 10006, United States",
                "city": "New York",
                "state": "NY",
                "country": "US",
                "postal_code": "10006"
            },
            "location": {
                "lat": 40.709845,
                "lng": -74.011213
            },
            "phone": "+1 212-555-0199",
            "website": "https://brewbean.example",
            "google_maps_url": "https://www.google.com/maps?cid=1234567890123456789",
            "last_updated_at": "2026-01-14T10:24:41Z"
        },
        "reviews": {
            "summary": {
                "average_rating": 4.3,
                "total_reviews": 187
            },
            "items": [
                {
                    "author_name": "Alex R.",
                    "rating": 5,
                    "text": "Fast service and great espresso. The croissants were fresh too.",
                    "relative_time_description": "2 weeks ago",
                    "language": "en"
                },
                {
                    "author_name": "Sam K.",
                    "rating": 4,
                    "text": "Nice place to work for an hour. Seating can get tight at peak times.",
                    "relative_time_description": "1 month ago",
                    "language": "en"
                }
            ]
        }
    }

## Use Cases

Growth teams use it to scrape google maps data for targeted regions, so they can build a clean prospect list without manual copying.
Analysts use a google map reviews scraper workflow to collect review signals, so they can measure reputation trends over time.
Operations teams use it as a google maps scraper tool to standardize listings, so they can keep internal directories accurate and deduplicated.
Researchers use a scraper google maps pipeline to export structured datasets, so they can run repeatable experiments across locations.
Developers use the google maps scraper github service as an internal dependency, so they can integrate listings into CRMs and internal systems.

## FAQs

**Is this a “free google maps scraper”?**  
It can be run for free locally, but data access depends on Google’s Places API usage and quotas in your Google Cloud project. If you’re looking for a free google map scraper experience, start with small limits and the API’s available free usage where applicable.

**Does it scrape the Google Maps website UI?**  
No. This is designed to avoid brittle UI automation. It uses official APIs, which is more reliable than trying to scrape google maps directly from the web interface.

**What environments are supported?**  
Docker-based local or self-hosted deployment on macOS, Linux, and Windows (Docker Desktop). The service exposes HTTP endpoints and can be used from any client.

**Can it extract emails (google maps email scraper)?**  
This project does not attempt to scrape emails from webpages or profiles. It only stores fields returned by official API responses (for example, phone and website when available). If you need contact enrichment, do it with explicit consent and compliant data sources.

## Performance & Reliability Benchmarks

- Typical job throughput (moderate limits): 120–260 businesses/minute with conservative pacing and details fetch enabled
- Review fetch throughput (optional): 40–90 businesses/minute depending on fields requested and quota limits
- End-to-end success rate: 90–94% on stable networks with retries enabled (varies by quota, query density, and transient API errors)
- Practical scale per single-node deployment: 25,000–60,000 business records/day with checkpointing and rollups
- Resource usage (idle, Docker): ~150–300 MB RAM for API + DB (varies by DB cache), CPU near-idle outside active jobs
- Recovery behavior: capped exponential backoff, per-job checkpoints, partial result persistence, and resumable pagination token handling


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/Z786ZA/Footer-test/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        "Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time."
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/Z786ZA/Footer-test/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        "Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on."
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/m-dRE1dj5-k?si=5kZNVlKsGUhg5Xtx" target="_blank">
        <img src="https://github.com/Z786ZA/Footer-test/blob/main/media/review3.gif" alt="Review 3" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        "Exceptional results, clear communication, and flawless delivery. <br>Bitbash nailed it."
      </p>
      <p style="margin:1px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
