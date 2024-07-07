FROM python:3.11.9-slim   

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ /app

RUN apt-get update && apt-get install -y cron
COPY start.sh /start.sh
RUN chmod +x /start.sh

ENV COS_SECRET_ID=""
ENV COS_SECRET_KEY=""
ENV COS_BUCKET=""
ENV COS_REGION=""
ENV COS_UPLOAD_NAME=""
ENV CRON_SCHEDULE="0 * * * *"

CMD ["/start.sh"]

