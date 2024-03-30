def md5(text: str):
    import hashlib
    return hashlib.md5(text.encode()).hexdigest()
