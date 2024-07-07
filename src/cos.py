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


class Cos:
    def __init__(self):
        # 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
        self.secret_id = os.environ[
            "COS_SECRET_ID"
        ]  # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        self.secret_key = os.environ[
            "COS_SECRET_KEY"
        ]  # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        self.region = os.environ[
            "COS_REGION"
        ]  # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
        # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
        self.token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
        self.scheme = (
            "https"  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        )

        self.config = CosConfig(
            Region=self.region,
            SecretId=self.secret_id,
            SecretKey=self.secret_key,
            Token=self.token,
            Scheme=self.scheme,
        )
        self.client = CosS3Client(self.config)
        self.uploadName = os.environ["COS_UPLOAD_NAME"]
        self.Bucket = os.environ["COS_BUCKET"]
        self.crc64 = crc64.CRC64(self.uploadName)
        self.local_crc64ecma = self.crc64.calculate_crc64()

    def upload(self):
        if not os.path.exists(self.uploadName):
            logger.info("文件不存在")
            exit()
        try:
            with open("../.env", "r") as f:
                previous_crc64 = f.read().strip()
        except FileNotFoundError:
            previous_crc64 = None

        if self.local_crc64ecma != previous_crc64:
            logger.info("文件有变化，开始上传")
            response = self.client.upload_file(
                Bucket=self.Bucket,
                Key=self.uploadName,
                LocalFilePath=self.uploadName,
                EnableMD5=False,
                progress_callback=None,
            )
            self.cos_crc64ecma = response["x-cos-hash-crc64ecma"]
            logger.info("cos crc64ecma: %s", self.cos_crc64ecma)
            self.check()
        else:
            logger.info("文件无变化，无需上传")

    def check(self):
        logger.info("local crc64ecma: %s", self.local_crc64ecma)
        if self.local_crc64ecma == self.cos_crc64ecma:
            logger.info("crc64校验成功,文件上传成功")
            with open("../.env", "w") as f:
                f.write(self.cos_crc64ecma)
        else:
            logger.info("crc64校验失败,文件上传失败")


if __name__ == "__main__":
    cos = Cos()
    cos.upload()
