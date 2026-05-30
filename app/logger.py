"""
Audit logging utilities.
Records query activity and suppression events
for compliance and traceability.
"""

from datetime import datetime, UTC
import json


def log_audit_event(group_by, filters, results):
    """
    Write an audit record for a query execution.

    Records query parameters and whether
    suppression was triggered.

    Args:
        group_by (str): Aggregation column.
        filters (dict | None): Filter criteria applied
            to the query.
        results (dict): Query results after suppression.
    """
    suppression_triggered = "suppressed" in results.values()

    audit_record = {
        "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "group_by": group_by,
        "filters": filters,
        "suppression_triggered": suppression_triggered,
    }

    with open("audit.log", "a") as audit_file:
        audit_file.write(
            json.dumps(audit_record) + "\n"  #    json.dumps(audit_record, indent=2)
        )
