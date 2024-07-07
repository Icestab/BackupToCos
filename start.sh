#!/bin/sh

# 创建 crontab 文件
echo "$CRON_SCHEDULE /usr/local/bin/python /app/main.py >> /app/data/backup_log_\$(date +\"\\%Y-\\%m-\\%d\").log 2>&1" > /etc/cron.d/backup-job
chmod 0644 /etc/cron.d/backup-job
crontab /etc/cron.d/backup-job

# 启动 cron 服务
service cron start
mkdir -p /app/data
touch /app/data/backup_log_$(date +"%Y-%m-%d").log
# 防止容器退出
tail -f /app/data/backup_log_$(date +"%Y-%m-%d").log
