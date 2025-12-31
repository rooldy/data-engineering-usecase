FROM apache/airflow:3.1.5

USER root

# Installe Java (requis pour Spark)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure JAVA_HOME pour ARM64 (Mac M1/M2/M3)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$PATH:$JAVA_HOME/bin

USER airflow

# Installe les providers Python avec retry et timeout plus long
RUN pip install --no-cache-dir --timeout=1000 --retries=10 \
    apache-airflow-providers-apache-spark || \
    pip install --no-cache-dir --timeout=1000 --retries=10 \
    apache-airflow-providers-apache-spark