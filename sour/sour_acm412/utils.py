import bcrypt

def generatePasswordHash(password):  
    # converting password to array of bytes
    bytes = password.encode("utf-8")
  
    # generating the salt
    salt = bcrypt.gensalt()
  
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    return hash.decode("utf-8")

def checkPassword(password, hash):  
    # encoding user password
    password_bytes = password.encode('utf-8')
    hash_bytes = hash.encode('utf-8')
  
    # checking password
    result = bcrypt.checkpw(password_bytes, hash_bytes)
  
    return result
