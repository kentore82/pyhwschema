import json
from pyspark.sql.types import StructType


def avro_to_spark_schema(pyspark_session, avro_schema_string, spark_version='2.4.0'):
    """Takes an avro-schema string as input and returns pyspark struct-type

      For Spark version < 2.4.0:
      The spark package com.databricks.spark.avro needs to be on sparks classpath.
      E.g.:
          --packages com.databricks:spark-avro_2.11:4.0.0

          or in spark-defaults.conf

          spark.jars.packages=com.databricks:spark-avro_2.11:4.0.0

      This function uses sparks Py4j gateway to access com.databricks.spark.avro.SchemaConverters
      and serializes back to Python as a Json string. PySparks StructType.fromJson() is then used to
      convert the schema into a valid pyspark df schema (StructType)

        Args:

          pyspark_session (pyspark.sql.SparkSession): A spark session
          avro_schema_string (str): Input Avro schema
          spark_version (str): default '2.4.0'

      Returns:
          pyspark_struct_type (pyspark.sql.types.StructType): A pyspark StructType schema
    """

    java_avro_schema = pyspark_session._jvm.org.apache.avro.Schema.parse(avro_schema_string)

    if (spark_version != '2.4.0') or (spark_version != u'2.4.0'):
        pyspark_struct_type_json = pyspark_session._jvm.com.databricks.spark.avro.SchemaConverters\
            .toSqlType(java_avro_schema).dataType().json()
    else:
        pyspark_struct_type_json = pyspark_session._jvm.org.apache.spark.sql.avro.SchemaConverters\
            .toSqlType(java_avro_schema).dataType().json()

    pyspark_struct_type = StructType.fromJson(json.loads(pyspark_struct_type_json))

    return pyspark_struct_type
