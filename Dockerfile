FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-openssl \
        ca-certificates \
    && \
    rm -rf /var/lib/apt/lists/*

COPY ssl_expiry_check.py /

EXPOSE 8080
ENTRYPOINT ["python3", "/ssl_expiry_check.py"]
