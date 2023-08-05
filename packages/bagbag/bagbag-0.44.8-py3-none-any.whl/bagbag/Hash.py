import hashlib

def Md5sum(data:str|bytes) -> str:
    return hashlib.md5(data).hexdigest()

if __name__ == "__main__":
    print(Md5sum("abc"))
