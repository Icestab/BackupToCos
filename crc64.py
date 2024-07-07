import crcmod
# COS 返回的 CRC64-ECMA 校验和
cos_crc64ecma = "15038935904765862205"  

def calculate_crc64(file_path):
    # 初始化CRC64 ECMA-182的多项式
    crc64_ecma = crcmod.mkCrcFun(0x142F0E1EBA9EA3693, initCrc=0, xorOut=0xffffffffffffffff, rev=True)
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    crc_value = crc64_ecma(data)
    return str(crc_value)

# 计算本地文件的 CRC64-ECMA 校验和
local_crc64ecma = calculate_crc64("test.zip")  # 将 "test.zip" 替换为你的文件名
print("本地文件的 CRC64-ECMA 校验和：", local_crc64ecma)
# 对比两个校验和
if local_crc64ecma == cos_crc64ecma:
  print("文件完整性校验成功！")
else:
  print("文件完整性校验失败！")