"""
FastAPI application exposing the lightweight analytics service
Allows users to query aggregate information from datasets in a safe and reproducible way.

Responsibilities:
- Load employee dataset
- Expose query endpoint
- Delegate query execution to query engine
- Return aggregated query results
"""

import pandas as pd
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
from app.query_engine import execute_query


class QueryRequest(BaseModel):
    """
    Request model for analytics queries.

    Attributes:
        group_by (str): Column used for aggregation.
        filter (dict | None): Optional filter criteria.
    """

    group_by: str
    filter: Optional[Dict[str, Any]] = None


# Create end point for Safe Analytics Query Service
app = FastAPI(title="Safe Analytics Query Service", version="1.0.0")

# load data
try:
    employees_df = pd.read_csv("data/employees.csv")
    logging.info(f"Loaded dataset with {len(employees_df)} records")
except Exception as error:
    logging.error(f"Failed to load dataset: {error}")
    raise


@app.post("/query")
def query(request: QueryRequest) -> dict:
    """
    Execute an analytics query.

    Args:
        request : QueryRequest containing the
        aggregation column and optional filters.

    Returns:
        dict: Aggregated query results with suppression
            applied where required.
    """

    logging.info("Received query request")
    # extract group by field
    group_by = request.group_by
    logging.info(f"Query requested for group_by field={group_by}")

    # extract filter columns
    filters = request.filter
    logging.info("Passing request to query engine")

    try:
        results = execute_query(df=employees_df, group_by=group_by, filters=filters)
        logging.info("Query processed successfully")
        return results
    # Translate validation exceptions into API responses.
    except HTTPException as error:
        return JSONResponse(
            status_code=error.status_code, content={"error": error.detail}
        )
