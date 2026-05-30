# Safe Analytics Query Service

## Overview

The Safe Analytics Query Service provides aggregate analytics over an employee dataset while protecting privacy through small-number suppression.

Features:

- Aggregate records by a specified field
- Apply optional filters
- Suppress counts below a configured threshold
- Generate audit logs for traceability
- Expose a REST API using FastAPI

---

## Architecture

### API Layer (`api.py`)

Responsible for:

- Request validation using Pydantic
- Exposing the `/query` endpoint
- Loading the dataset
- Returning API responses

### Query Engine (`query_engine.py`)

Responsible for:

- Validation logic
- Filtering
- Aggregation
- Suppression logic
- Audit logging

### Audit Logger (`logger.py`)

Responsible for:

- Recording query activity
- Tracking suppression events
- Writing audit records

---

## API Usage

```http
POST /query
```
Aggregate records by a specified field.

### Request

```json
{
  "group_by": "department"
}
```

### Request With Filter

```json
{
  "group_by": "department",
  "filter": {
    "location": "London"
  }
}
```

### Successful Response

```json
{
  "Engineering": 9,
  "Finance": 3,
  "Research": 4,
  "Executive": "suppressed"
}
```

### Validation Error

```json
{
  "error": "Invalid group_by field: unknown_column"
}
```

---

## Audit Logging

Each query execution generates an audit record.

Example:

```json
{
  "timestamp": "2026-05-29T11:27:22Z",
  "group_by": "department",
  "filters": {
    "location": "London"
  },
  "suppression_triggered": true
}
```

---

## Running Locally

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Application

```bash
uvicorn app.api:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

Execute all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

Current results:

```text
9 passed
96% coverage
```

---

## Running with Docker

### Build Image

```bash
docker build -t safe-analytics-query-service .
```

### Run Container

```bash
docker run -p 8000:8000 safe-analytics-query-service
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Project Structure

```text
safe-analytics-query-service/
│
├── app/
│   ├── api.py
│   ├── query_engine.py
│   ├── logger.py
│   └── __init__.py
│
├── data/
│   └── employees.csv
│
├── tests/
│   ├── test_api.py
│   └── test_query_engine.py
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── README.md
└── audit.log*
```

\* Generated automatically during execution and excluded from source control.

---

## Assumptions

- The suppression threshold is fixed at 3.
- The dataset is loaded into memory at application startup.
- Only aggregation queries are supported.
- Filter values may be provided as either a single value or a list.
- Invalid query fields return HTTP 400 responses.
- Validation exceptions are converted into a consistent JSON error response format using the API layer.
- Audit logs are written to a local file (`audit.log`).

---

## Notes

- Audit records are written to `audit.log`.
- The solution includes unit and API tests.
- Docker support is provided via the included Dockerfile.
- Swagger documentation is available at `/docs`.
- The solution was verified using both Swagger UI and Docker.

---

## Future Improvements

Potential production enhancements:

- Environment-based configuration
- Structured JSON application logging
- Persistent audit log storage
- Authentication and authorisation
- CI/CD pipeline integration
- Kubernetes deployment
- Enhanced monitoring and observability