# Stock data generator

Script that generates (not so realistic) stock data and sets up a Kafka producer to publish messages.

## Configuration
Can be done either via `config.ini` or environment variables:

* `GENSTOCK_TICKER_NAMES`: Path to a file that provides example ticker symbols, seperated by newlines. See [ticker_symbols](ticker_symbols_small) for an example.
* `GENSTOCK_KAFKA_HOST`: Kafka bootstrap server hostname.
* `GENSTOCK_KAFKA_CHANNEL`: Name of the Kafka channel name to publish messages to.
* `GENSTOCK_INTERVAL`: Interval of a new stock update. Effectively increases 'the speed of time', i.e. no adjustments are made to make shorter intervals more realistic.