from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Stock Streaming") \
    .getOrCreate()

lines = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "live-stock-data") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

q = lines.writeStream.outputMode('append').format('console').start()
q.awaitTermination()
