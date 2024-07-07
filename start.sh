#!/bin/sh

# 创建 crontab 文件
echo "$CRON_SCHEDULE cd /app && COS_SECRET_ID=\"$COS_SECRET_ID\" COS_SECRET_KEY=\"$COS_SECRET_KEY\" COS_BUCKET=\"$COS_BUCKET\" COS_REGION=\"$COS_REGION\" COS_UPLOAD_NAME=\"$COS_UPLOAD_NAME\" /usr/local/bin/python main.py >> /app/data/backup_log_\$(date +\"\\%Y-\\%m-\\%d\").log 2>&1" > /etc/cron.d/backup-job
chmod 0644 /etc/cron.d/backup-job
crontab /etc/cron.d/backup-job

# 启动 cron 服务
service cron start
mkdir -p /app/data
touch /app/data/backup_log_$(date +"%Y-%m-%d").log
# 防止容器退出
tail -f /app/data/backup_log_$(date +"%Y-%m-%d").log
