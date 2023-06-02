import bcrypt
from pathlib import Path
import os
from time import time

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

def profilePicturePath(filename):
    current_dir = Path(__file__).resolve().parent
    
    # remove the old image in static directory
    for file in os.listdir(os.path.join(current_dir, "static")):
        if file.startswith(filename):
            try:
                os.remove(os.path.join(current_dir, "static", file))
            except:
                pass

    timestamp = str(int(time()))
    filename = filename + "_" + timestamp + ".png"
    pp_path = os.path.join(current_dir, "static", filename)

    return pp_path, filename
