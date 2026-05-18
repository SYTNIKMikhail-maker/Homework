"""Unit tests for enroll module."""

import pytest
from pyspark_task.src.py_spark_task import (
    parse_dates,
    filter_last_year,
    add_year_month,
    get_required_months,
    check_consecutive,
    build_result,
)

from pyspark.sql import functions as F
from dateutil.relativedelta import relativedelta

END_DATE = datetime(2016, 9, 30)


@pytest.fixture(scope="session")
def spark():
    """Create a shared Spark session for tests."""
    return (
        SparkSession.builder
        .master("local[1]")
        .appName("test_enroll")
        .getOrCreate()
    )


@pytest.fixture
def raw_df(spark):
    """Sample raw input data."""
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
    """Test that dates are parsed correctly."""
    df = parse_dates(raw_df)
    assert "visit_date" in df.columns
    sample = df.filter(df.patient_id == "1").first()
    assert str(sample["visit_date"]) == "2016-09-01"


def test_filter_last_year(raw_df):
    """Test that records older than 1 year are removed."""
    df = parse_dates(raw_df)
    df_filtered = filter_last_year(df, END_DATE)
    count = df_filtered.count()
    assert count > 0

    start = END_DATE - relativedelta(years=1)
    out_of_range = df_filtered.filter(
        F.col("visit_date") < F.lit(start.date())
    ).count()
    assert out_of_range == 0


def test_get_required_months():
    """Test required months list generation."""
    months = get_required_months(END_DATE, 5)
    assert months == ["2016-05", "2016-06", "2016-07", "2016-08", "2016-09"]


def test_check_consecutive_5months(raw_df):
    """Patient 1 should pass 5months check, others should not."""
    df = parse_dates(raw_df)
    df = filter_last_year(df, END_DATE)
    df = add_year_month(df)
    result = check_consecutive(df, END_DATE, 5)

    rows = {r["patient_id"]: r["5months"] for r in result.collect()}
    assert rows["1"] is True
    assert rows["2"] is False
    assert rows["3"] is False
    assert rows["4"] is False


def test_build_result_schema(raw_df):
    """Result DataFrame should have correct columns and types."""
    df = parse_dates(raw_df)
    df = filter_last_year(df, END_DATE)
    df = add_year_month(df)
    result = build_result(df, END_DATE, [5, 9, 11])

    assert set(result.columns) == {"patient_id", "5months", "9months", "11months"}
    schema_map = {f.name: f.dataType.simpleString() for f in result.schema}
    assert schema_map["5months"] == "boolean"
    assert schema_map["9months"] == "boolean"
    assert schema_map["11months"] == "boolean"


def test_build_result_values(raw_df):
    """Check final result values match expected output."""
    df = parse_dates(raw_df)
    df = filter_last_year(df, END_DATE)
    df = add_year_month(df)
    result = build_result(df, END_DATE, [5, 9, 11])

    rows = {r["patient_id"]: r for r in result.collect()}
    assert rows["1"]["5months"] is True
    assert rows["1"]["9months"] is False
    assert rows["1"]["11months"] is False
    assert rows["2"]["5months"] is False
