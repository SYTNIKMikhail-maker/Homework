"""Unit tests for enroll module."""

from datetime import datetime

import pytest
from pyspark.sql import SparkSession, Row
import pyspark.sql.functions as F
from dateutil.relativedelta import relativedelta
from pyspark.testing.utils import assertDataFrameEqual

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


@pytest.fixture
def parsed_df(raw_df):
    """Return DataFrame with visit_date column parsed from raw format."""
    return parse_dates(raw_df)


@pytest.fixture
def filtered_df(parsed_df):
    """Return DataFrame filtered to the last year before END_DATE."""
    return filter_last_year(parsed_df, END_DATE)


@pytest.fixture
def enriched_df(filtered_df):
    """Return DataFrame with year_month column added."""
    return add_year_month(filtered_df)


def test_parse_dates(raw_df):
    """Check that visit_date column is created and parsed correctly."""
    df = parse_dates(raw_df)

    assert "visit_date" in df.columns

    sample = df.filter(df.patient_id == "1").first()
    assert str(sample["visit_date"]) == "2016-09-01"


def test_filter_last_year(parsed_df, spark):
    """Verify only visits within one year before END_DATE are retained."""
    actual_df = filter_last_year(parsed_df, END_DATE)

    start_date = END_DATE - relativedelta(years=1)

    expected_df = parsed_df.filter(
        (F.col("visit_date") >= F.lit(start_date.date())) &
        (F.col("visit_date") <= F.lit(END_DATE.date()))
    )

    assertDataFrameEqual(actual_df, expected_df, checkRowOrder=False)


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

    assertDataFrameEqual(actual_df, expected_df, checkRowOrder=False)


def test_build_result(enriched_df, spark):
    """Verify build_result returns correct schema and consecutive enrollment flags per patient."""
    actual_df = build_result(enriched_df, END_DATE, MONTHS_ARRAY)

    expected_df = spark.createDataFrame([
        ("1", True, False, False),
        ("2", False, False, False),
        ("3", False, False, False),
        ("4", False, False, False),
    ], ["patient_id", "5months", "9months", "11months"])

    assertDataFrameEqual(actual_df, expected_df, checkRowOrder=False)
