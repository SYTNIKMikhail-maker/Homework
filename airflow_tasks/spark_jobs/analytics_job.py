from pyspark.sql import SparkSession
import os

def main():

    login = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    url = os.getenv("POSTGRES_URL")

    spark = SparkSession.builder.appName("covid_countries_join").getOrCreate()

    covid = spark.read.format("jdbc") \
        .option("url", url) \
        .option("dbtable", "warehouse.covid_data") \
        .option("user", login) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .load()

    countries = spark.read.format("jdbc") \
        .option("url", url) \
        .option("dbtable", "warehouse.countries_data") \
        .option("user", login) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .load()

    df = covid.join(countries, covid.country == countries.country_name, "left")

    final_df = df.select(
        covid["country"],
        covid["date"],
        covid["cases"].alias("covid_cases"),
        covid["deaths"],
        covid["recovered"],
        covid["active"],
        countries["region"],
        countries["income_level"]
    )

    final_df.write.format("jdbc") \
        .option("url", url) \
        .option("dbtable", "warehouse.covid_countries_data") \
        .option("user", login) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()


if __name__ == "__main__":
    main()