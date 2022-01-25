from pyspark.sql import SparkSession
from pyspark.sql import Row

sharedPrefixes = "org.slf4j,org.apache.log4j,org.apache.logging.log4j,org.apache.spark,scala,com.google,java.,javax.sql"

spark = SparkSession \
    .builder \
    .master("spark://spark-master:7077") \
    .appName("Stock data") \
    .enableHiveSupport() \
    .config("spark.sql.hive.metastore.version", "3.1.2") \
    .config("spark.sql.hive.metastore.jars", "maven") \
    .getOrCreate()

    # .config("spark.sql.hive.metastore.jars", "/app/hivelibs-3.1.2") \
    # .config("spark.sql.hive.metastore.sharedPrefixes", sharedPrefixes) \

# .config("spark.sql.hive.metastore.version", "2.3.2") \
# .config("spark.sql.hive.metastore.jars", "maven") \

# .config("spark.sql.hive.metastore.jars", "/app/hivelibs-3.1.2") \
# .config("spark.sql.hive.metastore.sharedPrefixes", sharedPrefixes) \

spark.sql("select * from Stock where name == 'AAPL'").show()

# sqlDF = spark.sql("select * from Stock where name == 'AAPL'")
#
# sqlDF.groupBy("name").avg("volume").collect()
#
# for avg in sqlDF:
#     print(avg)
