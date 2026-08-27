import hashlib

def md5_encrypt(raw_password):
    """
    对原始明文密码做md5加密
    :param raw_password: 用户输入的明文密码字符串
    :return: md5加密后的字符串
    """
    obj = hashlib.md5()
    obj.update(raw_password.encode("utf-8"))
    return obj.hexdigest()