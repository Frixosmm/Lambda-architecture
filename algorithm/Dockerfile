FROM bde2020/spark-submit:3.0.2-hadoop3.2

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/streaming.py
ENV SPARK_SUBMIT_ARGS --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.2
ENV ENABLE_INIT_DAEMON false

COPY requirements.txt /app/
RUN cd /app && pip3 install -r requirements.txt
COPY . /app

#RUN curl -L http://10.0.0.33:8000/hive/hivelibs-3.1.2.tar.gz | tar zxf -

COPY hive-site.xml /spark/conf/

CMD ["/bin/bash", "/submit.sh"]
