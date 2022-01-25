FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

# Based on bde2020/hive

ARG HIVE_VERSION
ENV HIVE_VERSION=${HIVE_VERSION:-3.1.2}

ENV HIVE_HOME /opt/hive
ENV PATH $HIVE_HOME/bin:$PATH
ENV HADOOP_HOME /opt/hadoop-$HADOOP_VERSION

WORKDIR /opt

ARG APACHE_MIRROR=https://ftp.nluug.nl/internet/apache

RUN apt-get update && apt-get install -y wget procps && \
	wget $APACHE_MIRROR/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-bin.tar.gz && \
	tar -xzvf apache-hive-$HIVE_VERSION-bin.tar.gz && \
	mv apache-hive-$HIVE_VERSION-bin hive && \
	wget https://jdbc.postgresql.org/download/postgresql-42.2.19.jar -O $HIVE_HOME/lib/postgresql-jdbc.jar && \
	wget https://repository.cloudera.com/artifactory/libs-release-local/org/apache/hive/kafka-handler/3.1.3000.7.2.7.2-1/kafka-handler-3.1.3000.7.2.7.2-1.jar -P $HIVE_HOME/lib/ && \
	rm -f $HIVE_HOME/lib/log4j-slf4j-impl-2.10.0.jar && \
    rm -f $HIVE_HOME/lib/guava-19.0.jar && \
	cp $HADOOP_HOME/share/hadoop/common/lib/guava-27.0-jre.jar $HIVE_HOME/lib/ && \
	rm apache-hive-$HIVE_VERSION-bin.tar.gz && \
	apt-get --purge remove -y wget && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

ADD conf/hive-site.xml $HIVE_HOME/conf
ADD conf/beeline-log4j2.properties $HIVE_HOME/conf
ADD conf/hive-env.sh $HIVE_HOME/conf
ADD conf/hive-exec-log4j2.properties $HIVE_HOME/conf
ADD conf/hive-log4j2.properties $HIVE_HOME/conf
ADD conf/ivysettings.xml $HIVE_HOME/conf
ADD conf/llap-daemon-log4j2.properties $HIVE_HOME/conf

COPY startup.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/startup.sh

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 10000
EXPOSE 10002

ENTRYPOINT ["entrypoint.sh"]
CMD startup.sh
