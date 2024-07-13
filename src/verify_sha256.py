import hashlib
import argparse
import os
import logging

logger = logging.getLogger(__name__)


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_file_with_sha256sum(file_path):
    sha256_file_path = file_path + ".sha256"

    if not os.path.exists(sha256_file_path):
        logger.error(f"错误: 找不到 .sha256 文件: {sha256_file_path}")
        return False

    with open(sha256_file_path, "r") as f:
        expected_sha256 = f.readline().split()[0]

    calculated_sha256 = calculate_sha256(file_path)

    if calculated_sha256 == expected_sha256:
        logger.info("文件完整性验证通过")
        return True
    else:
        logger.error("文件完整性验证失败")
        logger.error(f"预期的SHA-256: {expected_sha256}")
        logger.error(f"计算得到的SHA-256: {calculated_sha256}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify the SHA-256 hash of a file against its .sha256 file."
    )
    parser.add_argument("file_path", help="Path to the file to verify.")

    args = parser.parse_args()
    verify_file_with_sha256sum(args.file_path)


if __name__ == "__main__":
    main()
