FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV GEOIP2_DB=/app/geodb/GeoLite2-City.mmdb

CMD ["python", "main.py"]

VOLUME /app/geodb

