import hashlib

def get_md5(password):
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()
