"""Unit tests for enroll module."""

from datetime import datetime

import pytest
from pyspark.sql import SparkSession, Row
import pyspark.sql.functions as F
from dateutil.relativedelta import relativedelta
from chispa.dataframe_comparer import assert_df_equality

from pyspark_task.src.py_spark_task import (
    parse_dates,
    filter_last_year,
    add_year_month,
    get_required_months,
    check_consecutive,
    build_result,
)

END_DATE = datetime(2016, 9, 30)
MONTHS_ARRAY = [5, 9, 11]


@pytest.fixture(scope="session")
def spark():
    """Create shared SparkSession for all tests."""
    return (
        SparkSession.builder
        .master("local[1]")
        .appName("test_enroll")
        .getOrCreate()
    )


@pytest.fixture
def raw_df(spark):
    """Return raw DataFrame with patient visits in MMddyyyy format."""
    data = [
        ("1", "09012016"),
        ("2", "09012016"),
        ("3", "09012016"),
        ("4", "09012016"),
        ("1", "08012016"),
        ("3", "08012016"),
        ("4", "08012016"),
        ("1", "07012016"),
        ("1", "06012016"),
        ("1", "05012016"),
        ("2", "03012016"),
        ("2", "01012016"),
        ("4", "01012016"),
    ]
    return spark.createDataFrame(data, ["patient_id", "effective_from_date"])


def test_parse_dates(raw_df):
    """Check that visit_date column is created and parsed correctly."""
    df = parse_dates(raw_df)

    assert "visit_date" in df.columns

    sample = df.filter(df.patient_id == "1").first()
    assert str(sample["visit_date"]) == "2016-09-01"


def test_filter_last_year(raw_df):
    """Verify no records exist before the one-year cutoff date."""
    df = parse_dates(raw_df)
    df_filtered = filter_last_year(df, END_DATE)

    start = END_DATE - relativedelta(years=1)

    out_of_range = df_filtered.filter(
        F.col("visit_date") < F.lit(start.date())
    ).count()

    assert out_of_range == 0


def test_get_required_months():
    """Ensure correct list of 5 months ending at END_DATE is generated."""
    actual = get_required_months(END_DATE, 5)

    expected = ["2016-05", "2016-06", "2016-07", "2016-08", "2016-09"]

    assert actual == expected


def test_check_consecutive_5months(spark):
    """Check consecutive visit logic for a 5-month window."""
    df_for_test = spark.createDataFrame(
        [
            ("1", "2016-05"), ("1", "2016-06"), ("1", "2016-07"),
            ("1", "2016-08"), ("1", "2016-09"),
            ("2", "2016-05"), ("2", "2016-06"),
            ("3", "2016-01"), ("3", "2016-02"), ("3", "2016-03"),
            ("3", "2016-04"), ("3", "2016-05"),
        ],
        ["patient_id", "year_month"],
    )

    actual_df = check_consecutive(df_for_test, END_DATE, 5)

    expected_df = spark.createDataFrame([
        Row(patient_id="1", **{"5months": True}),
        Row(patient_id="2", **{"5months": False}),
        Row(patient_id="3", **{"5months": False}),
    ])

    assert_df_equality(actual_df, expected_df, ignore_row_order=True)


def test_build_result_schema(raw_df):
    """Confirm result has correct columns and all flags are boolean type."""
    df = parse_dates(raw_df)
    df = filter_last_year(df, END_DATE)
    df = add_year_month(df)

    result = build_result(df, END_DATE, MONTHS_ARRAY)

    assert set(result.columns) == {
        "patient_id", "5months", "9months", "11months"
    }

    schema_map = {f.name: f.dataType.simpleString() for f in result.schema}

    assert schema_map["5months"] == "boolean"
    assert schema_map["9months"] == "boolean"
    assert schema_map["11months"] == "boolean"


def test_build_result_values(raw_df):
    """Verify patient 1 visited 5 months in a row but not 9 or 11."""
    df = parse_dates(raw_df)
    df = filter_last_year(df, END_DATE)
    df = add_year_month(df)

    result = build_result(df, END_DATE, MONTHS_ARRAY)

    rows = {r["patient_id"]: r for r in result.collect()}

    assert rows["1"]["5months"] is True
    assert rows["1"]["9months"] is False
    assert rows["1"]["11months"] is False
