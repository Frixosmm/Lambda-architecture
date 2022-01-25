'''
Generate stock data and send to kafka.
'''

import datetime as dt
import random
import time
import csv
import os
import sys
import pickle
import configparser
import json
from kafka import KafkaProducer

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore


cache_file = 'cache.pckl'
ticker_symbols_file = 'all_stocks_5yr.csv'
kafka_host = 'localhost:1234'
kafka_channel = 'live-stock-data'
gen_interval = 5

ticker_symbols = []
last = {}

producer = None

class Last:
    close = round(random.uniform(30 * 0.95, 30 * 1.05), 2)
    volume = round(random.randint(round(4320000 * 0.75), round(4320000 * 1.25)))


# Inspired by https://github.com/chartjs/chartjs-chart-financial/blob/master/docs/index.js
def random_stock_data(last_close, last_volume):
    open = round(random.uniform(last_close * 0.95, last_close * 1.05), 2)
    close = round(random.uniform(open * 0.95, open * 1.05), 2)
    high = round(random.uniform(max(open, close), max(open, close) * 1.1), 2)
    low = round(random.uniform(min(open, close) * 0.9, min(open, close)), 2)
    volume = round(random.randint(round(last_volume * 0.75), round(last_volume * 1.25)))
    volume = -volume if volume < 0 else volume
    return {'open': open, 'close': close, 'high': high, 'low': low, 'volume': volume}


# Load example names (ticker symbols) from a data set.
#
# Could be expanded to determine properties about this set,
# then extrapolate for slightly more probable artificial data.
#
def get_ticker_symbols(filename, cache_filename):
    ticker_symbols = []

    if os.path.exists(cache_filename):
        with open(cache_filename, 'rb') as cache_file:
            found_company_names = pickle.load(cache_file)
        return found_company_names

    with open(filename) as csv_file:
        stock_reader = csv.reader(csv_file, delimiter=',')
        headers = next(stock_reader)
        idx = [h.lower() for h in headers].index('name')
        for row in stock_reader:
            if row[idx] not in ticker_symbols:
                ticker_symbols.append(row[idx])

    with open(cache_filename, 'wb') as cache_file:
        pickle.dump(ticker_symbols, cache_file)

    return ticker_symbols


def send_new_data():
    global ticker_symbols, last, producer
    date = dt.datetime.now()

    entries = []

    for ts in ticker_symbols:
        entry = random_stock_data(last[ts].close, last[ts].volume)
        entry |= {'name': ts, 'date': date.strftime("%Y-%m-%d %T")}
        last[ts].close = entry['close']
        last[ts].volume = entry['volume']
        entries.append(entry)

    if producer:
        producer.send(kafka_channel, entries)


# Interval in seconds
def generate_live_data(interval=5):
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores={'default': MemoryJobStore()},
                        executors={'default': {'type': 'threadpool', 'max_workers': 5}},
                        job_defaults={'coalesce': False, 'max_instances': 3}, timezone=utc)
    job = scheduler.add_job(send_new_data, 'interval', seconds=interval)

    scheduler.start()

    # Keep busy for now
    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


# TODO
# def generate_fake_historical_data():
#     data = []
#     date = dt.datetime(2021, 1, 1)
#     # datetime.datetime.now()
#     date_string = date.strftime("%Y-%m-%d")
#     data.append(random_stock_data(30, 4320000))
#
#     date += dt.timedelta(days=1)
#     if date.weekday() <= 5:
#         last_close = data[len(data)-1]['close']
#         last_volume = data[len(data)-1]['volume']
#         data.append({'date': date_string} | random_stock_data(last_close, last_volume))


def read_config(config_file):
    global ticker_symbols_file, cache_file, kafka_host, kafka_channel, gen_interval
    if os.path.exists(config_file):
        c = configparser.ConfigParser()
        c.read(config_file)
        ticker_symbols_file = c['main'].get('stock_example', fallback=ticker_symbols_file)
        cache_file = c['main'].get('cache_file', fallback=cache_file)
        kafka_host = c['main'].get('kafka_host', fallback=kafka_host)
        kafka_channel = c['main'].get('kafka_channel', fallback=kafka_channel)
        gen_interval = c['main'].get('interval', fallback=gen_interval)


def read_config_env():
    global ticker_symbols_file, cache_file, kafka_host, kafka_channel, gen_interval

    se = os.environ.get('GENSTOCK_TICKER_NAMES_FILE')
    cf = os.environ.get('GENSTOCK_CACHE_FILE')
    kh = os.environ.get('GENSTOCK_KAFKA_HOST')
    kc = os.environ.get('GENSTOCK_KAFKA_CHANNEL')
    iv = os.environ.get('GENSTOCK_INTERVAL')

    if se:
        ticker_symbols_file = se
    if cf:
        cache_file = cf
    if kh:
        kafka_host = kh
    if kc:
        kafka_channel = kc
    if iv:
        gen_interval = iv


def main():
    global ticker_symbols, last, producer

    read_config('config.ini')
    read_config_env()

    if len(sys.argv) > 1:
        ticker_symbols = sys.argv[1:]
    else:
        ticker_symbols = get_ticker_symbols(ticker_symbols_file, cache_file)

    for ts in ticker_symbols:
        last[ts] = Last()

    producer = KafkaProducer(bootstrap_servers=kafka_host,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    generate_live_data(interval=gen_interval)


if __name__ == '__main__':
    main()
