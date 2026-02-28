import os
from urllib.parse import urlparse

def get_database_config():
   
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        
        return {
            "ENGINE": "mysql",
            "HOST": "localhost",
            "PORT": 3306,
            "USER": "root",
            "PASSWORD": "",
            "NAME": "internship_portal"
        }

    parsed = urlparse(db_url)

    engine = parsed.scheme  
    return {
        "ENGINE": engine,
        "HOST": parsed.hostname,
        "PORT": parsed.port or 3306,
        "USER": parsed.username,
        "PASSWORD": parsed.password,
        "NAME": parsed.path.lstrip("/")
    }