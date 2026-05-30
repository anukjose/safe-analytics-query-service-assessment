"""
Tests validation logic, suppression behaviour and filtering behaviour
"""

import pandas as pd
import pytest

from fastapi import HTTPException

from app.query_engine import (
    validate_groupby,
    apply_filters,
    validate_filters,
    apply_suppression,
)


def test_validate_groupby_invalid():
    df = pd.DataFrame({"department": ["Engineering"]})

    with pytest.raises(HTTPException):
        validate_groupby(df, "unknown")


def test_validate_filters_invalid():

    df = pd.DataFrame({"location": ["London"]})

    with pytest.raises(HTTPException):
        validate_filters(df, {"unknown_column": "London"})


def test_apply_single_filter():

    df = pd.DataFrame({"location": ["London", "London", "Manchester"]})

    filtered_df = apply_filters(df, {"location": "London"})

    assert len(filtered_df) == 2


def test_apply_list_filter():

    df = pd.DataFrame({"location": ["London", "Manchester", "Birmingham"]})

    filtered_df = apply_filters(df, {"location": ["London", "Manchester"]})

    assert len(filtered_df) == 2


def test_apply_suppression():

    counts = {"Engineering": 5, "Executive": 2}

    results = apply_suppression(counts, threshold=3)

    assert results == {"Engineering": 5, "Executive": "suppressed"}
