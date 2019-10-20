import hashlib
def encrypt(pwd):
    md5 = hashlib.md5()
    salt = '尼斯都想不到加密的密码会是什么'

    md5.update(salt.encode('utf-8'))
    md5.update(pwd.encode('utf-8'))
    return md5.hexdigest()



