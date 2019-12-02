import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    UPLOAD_FOLDER = "app/static"
    ALLOWED_EXTENSIONS = {'jpg'}