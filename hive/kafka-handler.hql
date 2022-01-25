create external table
stock_history (
  timestamp timestamp,
  open float,
  high float,
  low float,
  close float,
  volume int,
  name string
)
stored by
  'org.apache.hadoop.hive.kafka.KafkaStorageHandler'
tblproperties (
  "kafka.topic" = "live-stock-data",
  "kafka.bootstrap.servers" = "kafka:9092"
);
