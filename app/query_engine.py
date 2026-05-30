"""
Core query processing logic for the Safe Analytics Query Service.
Responsibilities:
- Validate query parameters
- Apply dataset filters
- Aggregate record counts
- Apply suppression rules
- Generate audit log entries
"""

import logging
from fastapi import HTTPException
from app.logger import log_audit_event

SUPPRESSION_THRESHOLD = 3


def execute_query(df, group_by, filters=None, threshold=SUPPRESSION_THRESHOLD):
    """
    Execute an analytics query.

    Validates input, applies filters, aggregates results
    and applies suppression.

    Args:
        df (pandas.DataFrame): Source dataset.
        group_by (str): Aggregation column.
        filters (dict | None): Optional filter criteria.
        threshold (int): Suppression threshold.

    Returns:
        dict: Aggregated query results.
    """

    logging.info("Executing query")
    validate_groupby(df, group_by)
    validate_filters(df, filters)
    logging.info("Applying filters")
    filtered_df = apply_filters(df, filters)
    logging.info("Aggregating results")
    counts = aggregate_counts(filtered_df, group_by)
    logging.info("Applying suppression")
    suppressed_results = apply_suppression(counts, threshold)
    log_audit_event(group_by, filters, suppressed_results)
    logging.info("Query completed successfully")
    return suppressed_results


def validate_groupby(df, group_by):
    """
    Validate that the group_by column exists.

    Args:
        df (pandas.DataFrame): Source dataset.
        group_by (str): Aggregation column.

    Raises:
        HTTPException: If the group_by column does not exist.
    """

    if group_by not in df.columns:
        logging.error(f"Invalid group_by field: {group_by}")
        raise HTTPException(
            status_code=400, detail=f"Invalid group_by field: {group_by}"
        )


def validate_filters(df, filters):
    """
    Validate that all filter columns exist.

    Args:
        df (pandas.DataFrame): Source dataset.
        filters (dict | None): Optional filter criteria.

    Raises:
        HTTPException: If a filter column does not exist.
    """
    if filters is None:
        return
    for column in filters.keys():
        if column not in df.columns:
            logging.error(f"Invalid filter column: {column}")
            raise HTTPException(
                status_code=400, detail=f"Invalid filter column: {column}"
            )


def apply_filters(df, filters):
    """
    Apply query filters to the dataset.

    Supports both single-value and multi-value filters.

    Args:
        df (pandas.DataFrame): Source dataset.
        filters (dict | None): Optional filter criteria.

    Returns:
        pandas.DataFrame: Filtered dataset.
    """
    if not filters:
        return df
    for column, value in filters.items():
        if isinstance(value, list):
            df = df[df[column].isin(value)]
        else:
            df = df[df[column] == value]

    return df


def aggregate_counts(df, group_by):
    """
    Aggregate record counts by the specified column.

    Args:
        df (pandas.DataFrame): Source dataset.
        group_by (str): Aggregation column.

    Returns:
        dict: Aggregated counts by group.
    """

    return df.groupby(group_by).size().to_dict()


def apply_suppression(counts, threshold=SUPPRESSION_THRESHOLD):
    """
    Suppress counts below the configured threshold.

    Args:
        counts (dict): Aggregated counts by group.
        threshold (int): Suppression threshold.

    Returns:
        dict: Results with counts below the threshold
            replaced by "suppressed".
    """
    results = {}
    for group, count in counts.items():
        if count < threshold:
            results[group] = "suppressed"
        else:
            results[group] = count
    return results
