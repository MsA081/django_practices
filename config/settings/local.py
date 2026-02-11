from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# پایگاه داده محلی (SQLite)
DATABASES["default"]["NAME"] = BASE_DIR / "db.sqlite3"

# کلید توسعه
SECRET_KEY = "dev-secret-key"
