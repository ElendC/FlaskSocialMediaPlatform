import os
import re

ImgTypes = {'image/jpeg', 'image/png'}
MaxProfImgSiz = 2097152

MinLenUsrname = 1
MaxLenUsrname = 10
MinLenPass = 1
MaxLenPass = 10

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {'jpeg', 'png'}

def validate_file(file):
    if not allowed_file(file.filename):
        return "Invalid name 1"
    if file.mimetype not in ImgTypes:
        return "Invalid type 2"
    file.seek(0, os.SEEK_END)
    if file.tell() > MaxProfImgSiz:
        file.seek(0)
        return "file to large, max 2MB!"
    file.seek(0)
    return None

def registerCheck(username, password):
    if len(username) < MinLenUsrname or len(username) > MaxLenUsrname:
        return f"Username needs to be between {MinLenUsrname} and {MaxLenUsrname} characters"
    if len(password) < MinLenPass or len(password) > MaxLenPass:
        return f"Password should be between {MinLenPass} and {MaxLenPass} characters"
    if not re.match("^[a-zA-Z0-9_æøåÆØÅ]+$", username):
        return "Username can contain A-Å, a-å, 0-9"
    return None