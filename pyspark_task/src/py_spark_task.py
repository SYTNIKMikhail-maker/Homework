"""Module for processing patient enrollment data."""

from datetime import datetime
from dateutil.relativedelta import relativedelta

from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from pyspark.sql.types import StringType


END_DATE = datetime(2016, 9, 30)
INPUT_PATH = "data/input/enroll.csv"
OUTPUT_PATH = "data/output/result.csv"
CONSECUTIVE_MONTHS = [5, 9, 11]


def create_spark_session(app_name: str = "enroll") -> SparkSession:
    """Create and return a Spark session."""
    return SparkSession.builder.appName(app_name).getOrCreate()


def load_data(spark: SparkSession, path: str) -> DataFrame:
    """Load CSV data into a Spark DataFrame."""
    return spark.read.csv(path, header=True, inferSchema=True)


def parse_dates(df: DataFrame) -> DataFrame:
    """Parse effective_from_date column to date type."""
    return df.withColumn(
        "visit_date",
        F.to_date(F.col("effective_from_date").cast(StringType()), "MMddyyyy")
    )


def filter_last_year(df: DataFrame, end_date: datetime) -> DataFrame:
    """Filter records within one year before end_date."""
    start_date = end_date - relativedelta(years=1)
    return df.filter(
        (F.col("visit_date") >= F.lit(start_date.date())) &
        (F.col("visit_date") <= F.lit(end_date.date()))
    )


def add_year_month(df: DataFrame) -> DataFrame:
    """Add year_month column in format yyyy-MM."""
    return df.withColumn(
        "year_month",
        F.date_format(F.col("visit_date"), "yyyy-MM")
    )


def get_required_months(end_date: datetime, n_months: int) -> list:
    """Generate list of required year-month strings for last n months."""
    return [
        (end_date - relativedelta(months=i)).strftime("%Y-%m")
        for i in range(n_months - 1, -1, -1)
    ]


def check_consecutive(df: DataFrame, end_date: datetime, n_months: int) -> DataFrame:
    """
    Check if each patient visited every month
    in the last n_months window up to end_date.
    """
    required_months = get_required_months(end_date, n_months)
    col_name = f"{n_months}months"

    df_patient_months = df.groupBy("patient_id").agg(
        F.collect_set("year_month").alias("visited_months")
    )

    check_array = F.array(*[F.lit(m) for m in required_months])

    return df_patient_months.withColumn(
        col_name,
        F.forall(check_array, lambda m: F.array_contains(F.col("visited_months"), m))
    ).select("patient_id", col_name)


def build_result(df_months: DataFrame, end_date: datetime, months_list: list) -> DataFrame:
    """Join consecutive check results for all month windows."""
    all_patients = df_months.select("patient_id").distinct()

    result = all_patients
    for n in months_list:
        check = check_consecutive(df_months, end_date, n)
        result = result.join(check, on="patient_id", how="left")

    return result.fillna(False).orderBy("patient_id")


def save_result(df: DataFrame, path: str) -> None:
    """Save DataFrame to CSV."""
    df.coalesce(1).write.csv(path, header=True, mode="overwrite")


def main() -> None:
    """Main entry point."""
    spark = create_spark_session()

    df_raw = load_data(spark, INPUT_PATH)
    df_parsed = parse_dates(df_raw)
    df_filtered = filter_last_year(df_parsed, END_DATE)
    df_months = add_year_month(df_filtered)
    result = build_result(df_months, END_DATE, CONSECUTIVE_MONTHS)
    save_result(result, OUTPUT_PATH)


if __name__ == "__main__":
    main()

