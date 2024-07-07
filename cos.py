# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import logging
import crc64

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = os.environ[
    "COS_SECRET_ID"
]  # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
secret_key = os.environ[
    "COS_SECRET_KEY"
]  # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
region = "ap-chongqing"  # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
# COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = "https"  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

config = CosConfig(
    Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme
)
client = CosS3Client(config)
uploadName = os.environ["uploadName"]
response = client.upload_file(
    Bucket=os.environ["Bucket"],
    Key=uploadName,
    LocalFilePath=uploadName,
    EnableMD5=False,
    progress_callback=None,
)

cos_crc64ecma = response["x-cos-hash-crc64ecma"]
logger.info("cos crc64ecma: %s", cos_crc64ecma)
crc64 = crc64.CRC64(uploadName)
local_crc64ecma = crc64.calculate_crc64()
logger.info("local crc64ecma: %s", local_crc64ecma)
if local_crc64ecma == cos_crc64ecma:
    logger.info("crc64校验成功,文件上传成功")
    with open(".env", "w") as f:
        f.write(cos_crc64ecma)
else:
    logger.info("crc64校验失败,文件上传失败")
