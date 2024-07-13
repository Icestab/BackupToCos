<h1 align="center">Backup To Cos</h1>

<p align="center">A simple backup tool for your data to Cos</p>

## 项目简介

本项目是一个简单的备份工具，可以将本地文件备份到腾讯云对象存储（COS）中。由于部署了一些项目，虽然已经本地备份，但仍然担心数据丢失，于是便有了这个项目。

## 功能

- 支持指定文件备份（单文件）
- 支持备份时检测文件是否已经修改
- 支持检测文件 crc64 判断备份文件的完整性
- 支持备份日志记录
- 目前，仅支持腾讯云对象存储（COS）
- 每次同步覆盖 cos 中的文件
- 新增容器时间环境变量默认上海时间，确保 cron 准确执行
- 本地文件上传时检验 sha256，防止本地文件未打包压缩完成时被上传

## 开发计划

- 支持指定目录备份（多文件）
- 支持断点续传
- 支持增量备份
- 支持其他云存储服务
- 支持版本控制（~~cos 原生具有版本控制功能，后续可能不会开发~~）

## 注意事项

- 本项目仅用于学习交流，请勿用于非法用途
- 本项目中的代码仅供参考，请勿直接使用
- 本项目中的代码可能存在安全漏洞，请自行评估风险

## 使用方法

> 本项目使用 python3.11 开发其余版本未经测试，使用前请确保已安装 python3.11

1. 拉取项目，安装依赖：`pip install -r requirements.txt`
2. 配置腾讯云对象存储（COS），建议使用子账号（保存 id 和 key，后续 key 不可获取）[参考文档](https://cloud.tencent.com/document/product/436/11714)，创建用于备份是存储桶，授予子账号数据读取和写入权限满足[最小权限原则说明](https://cloud.tencent.com/document/product/436/38618)
3. 配置参数，采用环境变量的方式调用，保证安全和适配 docker

- `COS_SECRET_ID`：腾讯云对象存储（COS）的 SecretId
- `COS_SECRET_KEY`：腾讯云对象存储（COS）的 SecretKey
- `COS_BUCKET`：腾讯云对象存储（COS）的存储桶名称
- `COS_REGION`：腾讯云对象存储（COS）的存储桶所在地域
- `COS_UPLOAD_NAME`：备份文件名和腾讯云对象存储（COS）的存储桶文件名（建议使用`/脚本绝对路径/data/backup.tar.gz`方便管理）

4. 将备份文件放入`data`中运行脚本：`python main.py`测试：

   如果出现`INFO:cos:crc64校验成功,文件上传成功`恭喜你，备份成功！

5. 结合[Linux 利用 rsync 实现全自动备份](https://flysch.top/study/questions/docker_backup.html)实现文件自动备份到指定目录，并通过本脚本备份到 COS

6. 配置定时任务，每天定时备份，结合上面的脚本时间，脚本时间定时到后几个小时，以免影响备份文件上传

## Docker

使用项目中`Dockerfile`构建镜像或直接拉取我构建的镜像`docker pull icestab/backup-to-cos`，运行容器，并挂载`data`目录，加入上面的环境变量和定时任务环境变量即可

docker-compose.yml

```yaml
services:
  backuptocos:
    image: icestab/backup-to-cos
    container_name: backuptocos
    volumes:
      - ./data:/app/data
    environment:
      COS_SECRET_ID: ''
      COS_SECRET_KEY: ''
      COS_BUCKET: ''
      COS_REGION: ''
      COS_UPLOAD_NAME: './data/backup.tar.gz'
      CRON_SCHEDULE: '0 * * * *'
      TZ: 'Asia/Shanghai'
```

TIPS:
`CRON_SCHEDULE: '0 * * * *'`
`TZ: 'Asia/Shanghai'`
这两项为镜像默认值，可不使用，如需修改请加上
